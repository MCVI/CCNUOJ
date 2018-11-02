#include <cstdint>

#include <vector>
#include <map>

#include <string>
#include <fstream>

namespace Config{
	const uint64_t MaxTimeLimit = 100;
	const uint64_t TimeLimitRedundant = 1;

	const uint64_t MaxMemoryLimit = 4*(uint64_t)1024*1024*1024;
	const uint64_t MemoryLimitRedundant= 16*1024*1024;

	const int MaxFileListItemNum = 100;
	const uint64_t MaxSyscallID = 1000;
}

struct SandboxConfig{
	struct File{
		std::string filename;
		struct{
			int read:1;
			int write:1;
		}permission;
	};

	std::string programPath;

	uint64_t timeLimit;
	uint64_t memoryLimit;

	std::vector<File> fileList;

	std::vector<bool> syscall;

	static SandboxConfig readFromJSON(std::ifstream &);
};

class ReadConfigError{};
class InvalidConfigFile:ReadConfigError{};
class ConfigLimitExceeded:ReadConfigError{};
class UnrecognizedSyscall:ReadConfigError{};

extern std::map<std::string, uint64_t> syscall_name_to_id;
extern std::map<uint64_t, std::string> syscall_id_to_name;

void SyscallList_Init();
void Run(const SandboxConfig &);
