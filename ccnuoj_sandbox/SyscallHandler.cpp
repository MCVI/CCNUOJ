#include <unistd.h>
#include <fcntl.h>

#include <sys/user.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>

#include <climits>

#include <experimental/filesystem>

#include "common.h"
#include "SyscallHandler.h"
#include "ProgramTerminated.h"

using namespace std;
namespace fs = std::experimental::filesystem;
using File = SandboxConfig::File;

class GetSymlinkTargetFailed{};
class ChildStringTooLong{};

SyscallHandler::SyscallHandler(const SandboxConfig &config):
		config(config),
		fileMap(_fileMap),
		wildcardFileList(_wildcardFileList),
		syscallMap(_syscallMap)
{
	for(const File &file: config.fileList){
		if(*(file.filename.rbegin())=='*'){
			File f;
			f.filename = file.filename.substr(0, file.filename.length()-1);
			f.permission = file.permission;
			this->_wildcardFileList.push_back(move(f));
		}else{
			// not ends with '*'
			this->_fileMap[file.filename] = file.permission;
		}
	}

	this->_syscallMap.clear();
	this->_syscallMap.resize((*(config.allowedSyscall.crbegin()))+1, false);
	for(const uint64_t id: config.allowedSyscall){
		this->_syscallMap[id] = true;
	}
}

inline static string ReadChildString(ChildProcess &child, char *addr, size_t maxLength){
	ostringstream tmp;
	size_t i=0;

	while(true){
		char buffer[sizeof(long)+1];

		*((long *)&buffer) = ptrace(PTRACE_PEEKDATA, child.pid, addr+i, nullptr);

		size_t j;
		for(j=0;j<sizeof(long);j++){
			if(buffer[j]=='\0'){
				break;
			}
		}
		buffer[j] = '\0';

		tmp<<buffer;
		if(i+j>maxLength){
			throw ChildStringTooLong();
		}else{
			i += j;
			if(j<sizeof(long)){
				return tmp.str();
			}
		}
	}
}

inline static void checkPermission(
		uint64_t syscall_id,
		const fs::path &filePath,
		const int oflags,
		const mode_t mode,
		const SandboxConfig::File::Permission &permission
){
	const int accessMode = oflags&O_ACCMODE;
	switch(accessMode){
		case O_RDONLY:
			if(!permission.read){
				throw DangerousFileOperation(filePath);
			}
			break;
		case O_WRONLY:
			if(!permission.write){
				throw DangerousFileOperation(filePath);
			}
			break;
		case O_RDWR:
			if(!(permission.read&&permission.write)){
				throw DangerousFileOperation(filePath);
			}
			break;
		default:
			throw DangerousSyscall(syscall_id);
			break;
	}
	if(oflags&O_CREAT){
		if(exists(filePath)){
			// do nothing
		}else{
			if(!permission.create){
				throw DangerousFileOperation(filePath);
			}
		}
	}

	// Notice: Linux kernel (testing version: 4.19.1) allow truncating even if the access mode is O_RDONLY
	// So the sandbox has to check manually
	if(oflags&O_TRUNC){
		if(!permission.write){
			throw DangerousFileOperation(filePath);
		}
	}

	// currently ignoring mode
}

inline static void checkOpenFile(
		const SyscallHandler &handler,
		ChildProcess &child,
		uint64_t syscall_id,
		string workDirSymlinkPath,
		string _relPath,
		int oflags,
		mode_t mode
){
	string pathStr;
	fs::path relPath(move(_relPath));

	if(relPath.is_absolute()){
		pathStr = move(relPath);
	}else{
		if(fs::exists(workDirSymlinkPath)&&fs::is_symlink(workDirSymlinkPath)){
			const fs::path workDir = fs::read_symlink(move(workDirSymlinkPath));
			pathStr = absolute(relPath, workDir);
		}else{
			throw GetSymlinkTargetFailed();
		}
	}

	map<string, File::Permission>::const_iterator iti = handler.fileMap.find(pathStr);
	if(iti==handler.fileMap.cend()){
		for(const File &file: handler.wildcardFileList){
			size_t len = file.filename.size();
			if(pathStr.size()<len){
				continue;
			}else{
				if(pathStr.substr(0, len)==file.filename){
					checkPermission(syscall_id, pathStr, oflags, mode, file.permission);
					return;
				}
			}
		}
		throw DangerousFileOperation(pathStr);
	}else{
		checkPermission(syscall_id, pathStr, oflags, mode, iti->second);
		return;
	}
}

void SyscallHandler::HandleSyscall_open(ChildProcess &child)const{
	try{
		struct user_regs_struct &regs = child.regs;

		string relPath;
		try{
			relPath = ReadChildString(child, reinterpret_cast<char *>(regs.rdi), PATH_MAX);
		}catch(ChildStringTooLong){
			throw GetSymlinkTargetFailed();
		}

		fs::path symlinkPath = "/proc/"+to_string(child.pid)+"/cwd";

		const int oflags = static_cast<int>(regs.rsi);
		const mode_t mode = static_cast<mode_t>(regs.rdx);
		checkOpenFile(*this, child, SYS_open, move(symlinkPath), move(relPath), oflags, mode);

	}catch(GetSymlinkTargetFailed){
		throw DangerousSyscall(SYS_openat);
	}
}

void SyscallHandler::HandleSyscall_openat(ChildProcess &child)const{
	try{
		struct user_regs_struct &regs = child.regs;
		int dirfd = static_cast<int>(regs.rdi);

		string relPath;
		try{
			relPath = ReadChildString(child, reinterpret_cast<char *>(regs.rsi), PATH_MAX);
		}catch(ChildStringTooLong){
			throw GetSymlinkTargetFailed();
		}

		fs::path symlinkPath;
		if(dirfd==AT_FDCWD){
			symlinkPath = "/proc/"+to_string(child.pid)+"/cwd";
		}else{
			symlinkPath = "/proc/"+to_string(child.pid)+"/fd/"+to_string(dirfd);
		}

		const int oflags = static_cast<int>(regs.rdx);
		const mode_t mode = static_cast<mode_t>(regs.r10);
		checkOpenFile(*this, child, SYS_openat, move(symlinkPath), move(relPath), oflags, mode);

	}catch(GetSymlinkTargetFailed){
		throw DangerousSyscall(SYS_openat);
	}
}

void SyscallHandler::beforeSyscall(ChildProcess &child){
	struct user_regs_struct &regs = child.regs;

	ptrace(PTRACE_GETREGS, child.pid, nullptr, &regs);

	uint64_t syscall_id = regs.orig_rax;
	if(syscall_id>=this->syscallMap.size()||(!(this->syscallMap[syscall_id]))){
		throw DangerousSyscall(syscall_id);
	}

	switch(syscall_id){
		case SYS_open:
			HandleSyscall_open(child);
			break;
		case SYS_openat:
			HandleSyscall_openat(child);
			break;
		default:
			// do nothing
			break;
	}
}

void SyscallHandler::afterSyscall(ChildProcess &process){
	// do nothing
}
