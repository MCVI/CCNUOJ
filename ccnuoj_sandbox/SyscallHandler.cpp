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
using namespace std::experimental::filesystem;
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
		const int oflags,
		const SandboxConfig::File::Permission &permission
){
	// stub
	printf("stub: check oflags=%x\n", oflags);
}

inline static void checkOpenFile(
		const SyscallHandler &handler,
		ChildProcess &child,
		string workDirSymlinkPath,
		string _relPath,
		int oflags
){
	string pathStr;
	path relPath(move(_relPath));

	if(relPath.is_absolute()){
		pathStr = move(relPath);
	}else{
		path filePath;
		if(exists(workDirSymlinkPath)&&is_symlink(workDirSymlinkPath)){
			filePath = read_symlink(move(workDirSymlinkPath));
		}else{
			throw GetSymlinkTargetFailed();
		}
		filePath.append(string(move(relPath)));
		pathStr = move(filePath);
	}

	map<string, File::Permission>::const_iterator iti = handler.fileMap.find(pathStr);
	if(iti==handler.fileMap.cend()){
		for(const File &file: handler.wildcardFileList){
			size_t len = file.filename.size();
			if(pathStr.size()<len){
				continue;
			}else{
				if(pathStr.substr(0, len)==file.filename){
					checkPermission(oflags, file.permission);
					return;
				}
			}
		}
		throw DangerousFileOperation(pathStr);
	}else{
		checkPermission(oflags, iti->second);
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

		path symlinkPath = "/proc/"+to_string(child.pid)+"/cwd";

		checkOpenFile(*this, child, symlinkPath, relPath, static_cast<int>(regs.rsi));

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

		path symlinkPath;
		if(dirfd==AT_FDCWD){
			symlinkPath = "/proc/"+to_string(child.pid)+"/cwd";
		}else{
			symlinkPath = "/proc/"+to_string(child.pid)+"/fd/"+to_string(dirfd);
		}

		checkOpenFile(*this, child, symlinkPath, relPath, static_cast<int>(regs.rdx));

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
