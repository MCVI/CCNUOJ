#pragma once

extern "C" {
#include <sys/user.h>
}

#include "common.h"
#include "ChildProcess.h"

class SyscallHandler{
	const SandboxConfig &config;

	using File=SandboxConfig::File;
	std::map<std::string, File::Permission> _fileMap;
	std::vector<File> _wildcardFileList;

	std::vector<bool> _syscallMap;

	void HandleSyscall_open(ChildProcess &child)const;
	void HandleSyscall_openat(ChildProcess &child)const;

public:
	const std::map<std::string, File::Permission> &fileMap;
	const std::vector<File> &wildcardFileList;
	const std::vector<bool> &syscallMap;

	explicit SyscallHandler(const SandboxConfig &config);

	void beforeSyscall(ChildProcess &child);
	void afterSyscall(ChildProcess &child);
};
