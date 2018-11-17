extern "C" {
#include <unistd.h>
#include <fcntl.h>

#include <sys/signal.h>
#include <sys/wait.h>
#include <sys/ptrace.h>
#include <sys/resource.h>
#include <sys/times.h>
}

#include <cstring>
#include <cmath>
#include <cassert>

#include <json/json.h>

#include "common.h"
#include "SyscallHandler.h"
#include "LaunchException.h"
#include "ProgramTerminated.h"

using namespace std;

void Run(const SandboxConfig &config){
	struct tms timeBegin, timeEnd;
	times(&timeBegin);


	SyscallHandler syscallHandler(config);

	ChildProcess child([&config]() -> int{

		const int numStdioRedirection = sizeof(config.stdioRedirection)/sizeof(*(config.stdioRedirection));
		for(int i=0;i<numStdioRedirection;i++){
			const ssize_t index = config.stdioRedirection[i];
			bool valid;

			if(index>=0){
				const SandboxConfig::File &file = config.fileList[index];
				int oflag;

				valid = false;
				switch(i){
					case STDIN_FILENO:
						if(file.permission.read){
							oflag = O_RDONLY;
							valid = true;
						}
						break;
					case STDOUT_FILENO:
						if(file.permission.write){
							oflag = O_WRONLY|O_TRUNC;
							valid = true;
						}
						break;
					case STDERR_FILENO:
						if(file.permission.write){
							oflag = O_WRONLY|O_TRUNC;
							valid = true;
						}
						break;
					default:
						break;
				}
				if(valid){
					if(file.permission.create){
						oflag |= O_CREAT;
					}

					// mode handling is not implemented, hard code instead
					const mode_t mode = S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP;

					int fd = open(file.filename.c_str(), oflag, mode);
					if(fd==-1){
						return static_cast<int>(SandboxException::RetValue::OpenFileFailed);
					}else{
						dup2(fd, i);
						close(fd);
					}
				}
			}else{
				valid = false;
			}

			if(!valid){
				close(i);   // will return -1 and set errno to EBADF if FD[i] is not opened
			}
		}

		struct rlimit limit;

		limit.rlim_cur = (uint64_t) ceil((config.timeLimit+Config::TimeLimitSoftRedundant)/(double) 1000);
		limit.rlim_max = (uint64_t) ceil((config.timeLimit+Config::TimeLimitHardRedundant)/(double) 1000);
		setrlimit(RLIMIT_CPU, &limit);

		limit.rlim_cur = config.memoryLimit+Config::MemoryLimitSoftRedundant;
		limit.rlim_max = config.memoryLimit+Config::MemoryLimitHardRedundant;
		setrlimit(RLIMIT_AS, &limit);

		execl(config.programPath.c_str(), config.programPath.c_str(), nullptr); // will not return when succeeded
		return static_cast<int>(SandboxException::RetValue::ExecFailed);
	});

	try{
		while(child.isRunning()){
			if(child.isPaused()){
				switch(child.state){
					case ChildProcess::State::ReceivedSignal:
						switch(child.signal){
							case SIGTRAP:
								if(!child.inUser){
									child.signal = 0;
									child.inUser = true;
								}
								break;
							case SIGXCPU:
								throw TimeLimitExceeded();
							default:
								break;
						}
						break;
					case ChildProcess::State::BeforeSyscall:
						syscallHandler.beforeSyscall(child);
						break;
					case ChildProcess::State::AfterSyscall:
						syscallHandler.afterSyscall(child);
						break;
					default:
						assert(false);
						break;
				}
				child.continueRunning();
			}else{
				child.waitNextEvent(true);
			}
		}
		switch(child.state){
			case ChildProcess::State::Terminated:
				throw ProgramSignaled(child.signal);

			case ChildProcess::State::Exited:
				if(child.inUser){
					if(child.information.memory.asUInt64()>config.memoryLimit){
						throw MemoryLimitExceeded();
					}else if(child.information.time.asDouble()*1000>config.timeLimit){
						throw TimeLimitExceeded();
					}else{
						throw ProgramExited(child.ret);
					}
				}else{
					SandboxException::RetValue ret = static_cast<SandboxException::RetValue>(child.ret);
					if(ret==SandboxException::RetValue::OpenFileFailed){
						throw OpenFileFailed();
					}else if(ret==SandboxException::RetValue::ExecFailed){
						throw ExecFailed();
					}else{
						throw LaunchFailed();
					}
				}

			default:
				assert(false);
				break;
		}
	}catch(ProcessInformation &e){
		if(child.isRunning()){
			child.terminate();
		}
		e.copyProcessInformationFrom(child.information);
		throw;
	}
}
