extern "C" {
#include <unistd.h>

#include <sys/signal.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <sys/ptrace.h>
#include <sys/resource.h>
}

#include <cstring>

#include "common.h"

using namespace std;

struct ChildQuit{};
struct SandboxError:ChildQuit{};
struct ProgramLaunchFailed:ChildQuit{};
struct ProgramExit:ChildQuit{
public:
	const int exit_code;

	explicit ProgramExit(const int exit_code):exit_code(exit_code){}
};
struct ProgramTerminated:ChildQuit{
public:
	const int terminate_signal;

	explicit ProgramTerminated(const int signal):terminate_signal(signal){}
};
struct ProgramDangerousBehavior:ChildQuit{};

void Child(const SandboxConfig &config){
	const pid_t child = getpid();
	ptrace(PTRACE_TRACEME, 0, nullptr, nullptr);
	kill(child, SIGTRAP);

	struct rlimit limit;

	limit.rlim_cur = config.timeLimit;
	limit.rlim_max = config.timeLimit + Config::TimeLimitRedundant;
	setrlimit(RLIMIT_CPU, &limit);

	limit.rlim_cur = config.memoryLimit;
	limit.rlim_max = config.memoryLimit + Config::MemoryLimitRedundant;
	setrlimit(RLIMIT_AS, &limit);

	execl(config.programPath.c_str(), nullptr);
	kill(child, SIGUSR1);
}

void Trace(const SandboxConfig &config, const pid_t child){
	while(true){
		int status;
		waitpid(child, &status, 0);

		if(WIFEXITED(status)){
			throw SandboxError();
		}else if(WIFSIGNALED(status)){
			throw SandboxError();
		}else if(WIFSTOPPED(status)){
			int signal = WSTOPSIG(status);
			if(signal==SIGTRAP){
				ptrace(PTRACE_CONT, child, nullptr, nullptr);
				break;
			}else{
				ptrace(PTRACE_CONT, child, nullptr, signal);
			}
		}else{
			kill(child, SIGKILL);
			throw SandboxError();
		}
	}

	ptrace(PTRACE_SETOPTIONS, child, PTRACE_O_TRACEEXIT);

	while(true){
		int status;
		waitpid(child, &status, 0);

		if(WIFEXITED(status)){
			fprintf(stderr, "exit code: %d\n", WEXITSTATUS(status));
			throw SandboxError();
		}else if(WIFSIGNALED(status)){
			throw SandboxError();
		}else if(WIFSTOPPED(status)){
			int signal = WSTOPSIG(status);
			if(signal==SIGTRAP){
				// exec succeeded
				ptrace(PTRACE_SYSCALL, child, nullptr, nullptr);
				break;
			}else if(signal==SIGUSR1){
				// exec failed
				throw ProgramLaunchFailed();
			}else{
				ptrace(PTRACE_CONT, child, nullptr, signal);
			}
		}else{
			kill(child, SIGKILL);
			throw SandboxError();
		}
	}

	bool inSyscall = false;
	while(true){
		int status;
		waitpid(child, &status, 0);

		if(WIFEXITED(status)){
			throw ProgramExit(WEXITSTATUS(status));
		}else if(WIFSIGNALED(status)){
			throw ProgramTerminated(WTERMSIG(status));
		}else if(WIFSTOPPED(status)){
			int signal = WSTOPSIG(status);
			if(signal==SIGTRAP){
				if(inSyscall){
					inSyscall = false;
					ptrace(PTRACE_SYSCALL, child, nullptr, nullptr);
				}else{
					struct user_regs_struct regs;
					ptrace(PTRACE_GETREGS, child, nullptr, &regs);
					uint64_t syscall_id = regs.orig_rax;

					bool check_result;
					if(syscall_id>=config.syscall.size()){
						check_result = false;
					}else{
						if(config.syscall[syscall_id]){
							check_result = true;
						}else{
							check_result = false;
						}
					}

					map<uint64_t, string>::iterator iti = syscall_id_to_name.find(syscall_id);
					if(iti==syscall_id_to_name.end()){
						fprintf(stderr, "Child called syscall[%d]\n", syscall_id);
					}else{
						fprintf(stderr, "Child called syscall[%d](%s)\n", syscall_id, iti->second.c_str());
					}

					inSyscall = true;
					if(check_result){
						ptrace(PTRACE_SYSCALL, child, nullptr, nullptr);
					}else{
						kill(child, SIGKILL);
						throw ProgramDangerousBehavior();
					}
				}
			}else{
				ptrace(PTRACE_SYSCALL, child, nullptr, signal);
			}
		}else{
			kill(child, SIGKILL);
			throw SandboxError();
		}
	}
}

void Run(const SandboxConfig &config){
	const pid_t pid = fork();
	if(pid==0){
		Child(config);
	}else{
		Trace(config, pid);
	}
}
