#include <fcntl.h>
#include <sys/user.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>

#include "common.h"
#include "SyscallHandler.h"
#include "ProgramTerminated.h"

using namespace std;

SyscallHandler::SyscallHandler(const SandboxConfig &config):config(config){
	for(const File &file: config.fileList){
		if(file.filename.find('*')==string::npos){
			// '*' not found
			this->fileMap[file.filename] = file.permission;
		}else{
			this->wildcardFileList.push_back(file);
		}
	}

	this->syscallMap.clear();
	this->syscallMap.resize((*(config.allowedSyscall.crbegin()))+1, false);
	for(const uint64_t id: config.allowedSyscall){
		syscallMap[id] = true;
	}
}

inline void SyscallHandler::HandleSyscall_openat(int dirfd)const{
	// stub
}

void SyscallHandler::beforeSyscall(ChildProcess &child){
	ptrace(PTRACE_GETREGS, child.pid, nullptr, &regs);

	uint64_t syscall_id = regs.orig_rax;

	if(syscall_id>=this->syscallMap.size()){
		throw DangerousSyscall(Json::Value(), Json::Value(), syscall_id);
	}else if(!(this->syscallMap[syscall_id])){
		throw DangerousSyscall(Json::Value(), Json::Value(), syscall_id);
	}

	switch(syscall_id){
		case SYS_open:
			HandleSyscall_openat(AT_FDCWD);
			break;
		case SYS_openat:
			HandleSyscall_openat((int)regs.rbx);
			break;
		default:
			// do nothing
			break;
	}
}

void SyscallHandler::afterSyscall(ChildProcess &process){
	// do nothing
}
