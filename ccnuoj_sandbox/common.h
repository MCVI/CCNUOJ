#pragma once

#include <cstdint>

#include <vector>
#include <set>
#include <map>

#include <string>
#include <fstream>
#include <memory>

namespace Config{
	const uint64_t MaxTimeLimit = 100*1000;
	const uint64_t TimeLimitRedundant = 1*1000;

	const uint64_t MaxMemoryLimit = 4*(uint64_t)1024*1024*1024;
	const uint64_t MemoryLimitRedundant= 16*1024*1024;

	const int MaxFileListItemNum = 100;
	const uint64_t MaxSyscallID = 1000;

	// Notice: this is the stack size of child process before launching the target program
	const size_t ChildStackSize = 4*1024*1024;
}

class SandboxConfig{
public:
	struct File{
		std::string filename;
		struct Permission{
			int read:1;
			int write:1;
		}permission;
	};

	std::unique_ptr<std::ostream> sandboxOutput;

	std::string programPath;

	uint64_t timeLimit;
	uint64_t memoryLimit;

	std::string stdioFile[3];
	std::vector<File> fileList;

	std::set<uint64_t> allowedSyscall;
};

extern std::map<std::string, uint64_t> syscall_name_to_id;
extern std::map<uint64_t, std::string> syscall_id_to_name;

void SyscallList_Init();
void ReadConfigFromFile(SandboxConfig &config, std::ifstream &f);
void Run(const SandboxConfig &);
