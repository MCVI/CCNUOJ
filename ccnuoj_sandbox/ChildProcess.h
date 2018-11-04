#pragma once

#include <cassert>

#include <functional>
#include <json/json.h>

#include <sys/times.h>

class ChildProcess{
	bool inSyscall;
	bool firstSIGUSR1;

	struct tms timeStart, timeEnd;

	std::function<int()> func;

	void continueRunning_Internal();
	void waitNextEvent_Internal();

	friend int ChildProcessEntry(void *obj);

public:
	enum class State{
		BeforeCreated = 0,
		Running,
		ReceivedSignal,
		BeforeSyscall,
		AfterSyscall,
		Exited,
		Terminated,
	};

	State state;
	pid_t pid;
	int status, ret, signal;

	bool inUser;

	double time;
	size_t memory;

	explicit ChildProcess(std::function<int()> func);
	ChildProcess(const ChildProcess &child) = delete;
	~ChildProcess();

	bool isRunning()const{
		return !(
				(state==State::BeforeCreated)||
				(state==State::Exited)||
				(state==State::Terminated)
		);
	}
	bool isPaused()const{
		return isRunning()&&(state!=State::Running);
	}

	void calcMemory();
	void calcTime();
	void terminate();
	void continueRunning();
	void waitNextEvent(bool sync = true);
};
