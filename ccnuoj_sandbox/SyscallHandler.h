#pragma once

extern "C" {
#include <sys/user.h>
}

#include "common.h"
#include "ChildProcess.h"

class SyscallHandler{
	const SandboxConfig &config;

	struct user_regs_struct regs;

	using File=SandboxConfig::File;
	std::map<std::string, File::Permission> fileMap;
	std::vector<File> wildcardFileList;

	std::vector<bool> syscallMap;

	void HandleSyscall_openat(int dirfd)const;

public:
	explicit SyscallHandler(const SandboxConfig &config);

	void beforeSyscall(ChildProcess &child);
	void afterSyscall(ChildProcess &child);
};
