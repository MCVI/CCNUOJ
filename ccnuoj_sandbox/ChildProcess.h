#pragma once

#include <cassert>

#include <functional>
#include <json/json.h>

#include <sys/times.h>
#include <sys/user.h>

class ProcessInformation{
	friend class ChildProcess;

	Json::Value _time;
	Json::Value _memory;

public:
	const Json::Value &time;
	const Json::Value &memory;

	ProcessInformation(): time(_time), memory(_memory){}
	virtual ~ProcessInformation() = default;

	virtual void copyProcessInformationFrom(const ProcessInformation &info){
		this->_time = info._time;
		this->_memory = info._memory;
	}

	virtual void fillDetail(Json::Value &detail)const{
		detail["time"] = time;
		detail["memory"] = memory;
	}
};

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
	struct user_regs_struct regs;
	int status, ret, signal;
	bool inUser;

	ProcessInformation information;

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
