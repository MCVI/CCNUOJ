#include <unistd.h>
#include <sys/times.h>
#include <sys/signal.h>
#include <sys/mman.h>
#include <sys/ptrace.h>
#include <sys/wait.h>

#include <cassert>

#include <sstream>
#include <algorithm>

#include "common.h"
#include "ChildProcess.h"
#include "LaunchException.h"

using namespace std;

int ChildProcessEntry(void *obj){
	ptrace(PTRACE_TRACEME, 0, nullptr, nullptr);
	kill(getpid(), SIGUSR1);

	const ChildProcess &context = *reinterpret_cast<const ChildProcess *>(obj);
	return context.func.operator()();
}

ChildProcess::ChildProcess(std::function<int()> func):
		state(State::BeforeCreated),
		inSyscall(false),
		inUser(false),
		firstSIGUSR1(false),
		func(move(func)
){
	struct StackRaii{
		int8_t *stackBottom, *stackTop;
		StackRaii(){
			stackBottom = reinterpret_cast<int8_t *>(mmap(
					nullptr,
					Config::ChildStackSize,
					PROT_READ|PROT_WRITE,
					MAP_PRIVATE|MAP_ANONYMOUS|MAP_GROWSDOWN,
					-1,
					0
			));
			if(stackBottom==(void *)(-1)){
				throw bad_alloc();
			}
			stackTop = stackBottom + Config::ChildStackSize;
		}
		~StackRaii(){
			munmap(stackBottom, Config::ChildStackSize);
		}
	}stackRaii;

	times(&(this->timeStart));

	pid_t pid = clone(ChildProcessEntry, stackRaii.stackTop, SIGCHLD, this);
	if(pid==0){
		throw CloneFailed(errno);
	}else{
		this->pid = pid;
		this->state = State::Running;
	}
}

ChildProcess::~ChildProcess(){
	if(this->isRunning()){
		this->terminate();
	}
}

void ChildProcess::calcMemory(){
	const static string prefix("vmpeak:");

	Json::Value &memory = this->information._memory;

	string proc_file_path = string("/proc/") + to_string(this->pid) + "/status";
	fstream proc_file;

	proc_file.open(proc_file_path, ios::in);
	if(proc_file.is_open()){
		while(true){
			string line;
			getline(proc_file, line);
			if(proc_file.eof()){
				break;
			}

			transform(line.begin(), line.end(), line.begin(), ::tolower); // upper case to lower case

			if(line.compare(0, prefix.size(), prefix)==0){
				istringstream ss(line.substr(prefix.size(), line.size()));
				size_t num;
				string unit;
				ss>>num>>unit;
				if(unit.empty()){
					memory = num;
				}else if(unit=="kb"){
					memory = num*1024;
				}else if(unit=="mb"){
					memory = num*1024*1024;
				}else if(unit=="gb"){
					memory = num*1024*1024*1024;
				}
			}
		}
		proc_file.close();
	}
}

void ChildProcess::calcTime(){
	times(&(this->timeEnd));
	cerr<<"timeEnd.tms_utime"<<timeEnd.tms_utime<<" timeStart.tms_utime"<<timeStart.tms_utime<<endl;
	cerr<<"timeEnd.tms_cutime"<<timeEnd.tms_cutime<<" timeStart.tms_cutime"<<timeStart.tms_cutime<<endl;

	clock_t utime = timeEnd.tms_cutime - timeStart.tms_cutime;
	clock_t stime = timeEnd.tms_cstime - timeStart.tms_cstime;
	this->information._time = (utime+stime)/(double)sysconf(_SC_CLK_TCK);;
}

void ChildProcess::terminate(){
	assert(this->isRunning());

	calcMemory();

	/*
	cerr<<"waiting for char...";
	getchar();
	*/

	kill(this->pid, SIGKILL);

	//ptrace(PTRACE_CONT, this->pid, nullptr, nullptr);

	waitid(P_PID, (id_t)(this->pid), nullptr, WEXITED);
	this->state = State::Terminated;

	calcTime();
}

void ChildProcess::continueRunning_Internal(){
	enum __ptrace_request request;
	if(this->inUser){
		request = PTRACE_SYSCALL;
	}else{
		request = PTRACE_CONT;
	}

	int signal;
	if(this->state==State::ReceivedSignal){
		signal = this->signal;
	}else{
		signal = 0;
	}

	ptrace(request, this->pid, nullptr, signal);
}

void ChildProcess::continueRunning(){
	assert(this->isPaused());

	continueRunning_Internal();

	this->state = State::Running;
}

void ChildProcess::waitNextEvent_Internal(){
	if(WIFEXITED(status)){
		state = State::Exited;
		ret = WEXITSTATUS(status);
		calcTime();
	}else if(WIFSIGNALED(status)){
		state = State::Terminated;
		signal = WTERMSIG(status);
		calcTime();
	}else{
		// stopped
		this->signal = WSTOPSIG(status);
		switch(signal){
			case SIGUSR1:
				if(this->firstSIGUSR1){
					state = State::ReceivedSignal;
				}else{
					this->signal = 0;
					this->firstSIGUSR1 = true;

					ptrace(PTRACE_SETOPTIONS, this->pid, nullptr,
							PTRACE_O_EXITKILL|
							PTRACE_O_TRACESYSGOOD|
							PTRACE_O_TRACEEXIT
					);
				}
				break;
			case (SIGTRAP|0x80):
				if(inSyscall){
					state = State::AfterSyscall;
					inSyscall = false;
				}else{
					state = State::BeforeSyscall;
					inSyscall = true;
				}
				break;
			case SIGTRAP:
				if((status>>8)==(SIGTRAP|PTRACE_EVENT_EXIT<<8)){
					calcMemory();
				}else{
					state = State::ReceivedSignal;
				}
				break;
			default:
				state = State::ReceivedSignal;
				break;
		}
	}
}

void ChildProcess::waitNextEvent(bool sync){
	assert(this->state == State::Running);

	if(sync){
		while(true){
			waitpid(this->pid, &(this->status), 0);
			this->waitNextEvent_Internal();
			if(this->state == State::Running){
				this->continueRunning_Internal();
			}else{
				break;
			}
		}
	}else{
		if(waitpid(this->pid, &(this->status), WNOHANG)==0){
			return;
		}else{
			this->waitNextEvent_Internal();
		}
	}
}
