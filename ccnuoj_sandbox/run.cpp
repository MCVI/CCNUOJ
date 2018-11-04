extern "C" {
#include <unistd.h>

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
		struct rlimit limit;

		limit.rlim_cur = (uint64_t) ceil(config.timeLimit/(double) 1000);
		limit.rlim_max = (uint64_t) ceil((config.timeLimit+Config::TimeLimitRedundant)/(double) 1000);
		setrlimit(RLIMIT_CPU, &limit);

		limit.rlim_cur = config.memoryLimit;
		limit.rlim_max = config.memoryLimit+Config::MemoryLimitRedundant;
		setrlimit(RLIMIT_AS, &limit);

		execl(config.programPath.c_str(), config.programPath.c_str(), nullptr); // will not return when succeeded

		// failed
		kill(getpid(), SIGUSR1);

		exit(-1);
	});

	while(child.isRunning()){
		try{
			if(child.isPaused()){
				switch(child.state){
					case ChildProcess::State::ReceivedSignal:
						switch(child.signal){
							case SIGUSR1:
								if(!child.inUser){
									child.signal = 0;
									throw ExecFailed();
								}
								break;
							case SIGTRAP:
								if(!child.inUser){
									child.signal = 0;
									child.inUser = true;
								}
								break;
							case SIGXCPU:
								throw TimeLimitExceeded(Json::Value(), Json::Value());
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
		}catch(ProgramTerminated &e){
			child.terminate();
			e.time = child.time;
			e.memory = child.memory;
			throw;
		}
	}

	switch(child.state){
		case ChildProcess::State::Terminated:
			throw ProgramSignaled(child.time, child.memory, child.signal);

		case ChildProcess::State::Exited:
			throw ProgramExited(child.time, child.memory, child.ret);

		default:
			assert(false);
			break;
	}
}
