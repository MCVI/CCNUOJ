#pragma once

#include "common.h"
#include "SandboxException.h"

class ProgramTerminated:public SandboxException{
public:
	Json::Value time;
	Json::Value memory;

	ProgramTerminated(Json::Value time, Json::Value memory):time(std::move(time)),memory(std::move(memory)){}

	RetValue getRetValue()const override{
		return RetValue::Finished;
	}

	static std::string staticName(){
		return "ProgramTerminated";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = SandboxException::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = SandboxException::getJsonObject();
		json["detail"]["time"] = time;
		json["detail"]["memory"] = memory;
		return json;
	}
};

class DangerousBehavior:public ProgramTerminated{
public:
	DangerousBehavior(Json::Value time, Json::Value memory):ProgramTerminated(std::move(time), std::move(memory)){}

	static std::string staticName(){
		return "DangerousBehavior";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ProgramTerminated::getCategory();
		category.append(staticName());
		return category;
	}
};

class DangerousSyscall:public DangerousBehavior{
public:
	const uint64_t syscallID;

	explicit DangerousSyscall(
			Json::Value time,
			Json::Value memory,
			const uint64_t syscallID
	):DangerousBehavior(std::move(time),std::move(memory)), syscallID(syscallID){}

	static std::string staticName(){
		return "DangerousSyscall";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = DangerousBehavior::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = DangerousBehavior::getJsonObject();
		Json::Value syscall;
		syscall["id"] = this->syscallID;
		std::map<uint64_t, std::string>::iterator iti = syscall_id_to_name.find(this->syscallID);
		if(iti!=syscall_id_to_name.end()){
			syscall["name"] = iti->second;
		}
		json["detail"]["dangerousSyscall"] = syscall;
		return json;
	};
};

class DangerousFileOperation:public DangerousBehavior{
public:
	const std::string path;

	explicit DangerousFileOperation(
			Json::Value time,
			Json::Value memory,
			std::string path
	):DangerousBehavior(std::move(time),std::move(memory)), path(move(path)){}

	static std::string staticName(){
		return "DangerousFileOperation";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = DangerousBehavior::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = DangerousBehavior::getJsonObject();
		Json::Value operation = Json::Value();
		operation["path"] = path;
		json["detail"]["dangerousFileOperation"] = operation;
		return json;
	};
};

class ProgramSignaled:public ProgramTerminated{
public:
	const int signal;

	explicit ProgramSignaled(
			Json::Value time,
			Json::Value memory,
			const int signal
	):ProgramTerminated(std::move(time), std::move(memory)), signal(signal){}

	static std::string staticName(){
		return "ProgramSignaled";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ProgramTerminated::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = ProgramTerminated::getJsonObject();
		Json::Value signal;
		signal["id"] = this->signal;
		json["detail"]["signal"] = signal;
		return json;
	};
};

class TimeLimitExceeded:public ProgramTerminated{
public:
	explicit TimeLimitExceeded(
			Json::Value time,
			Json::Value memory
	):ProgramTerminated(std::move(time), std::move(memory)){}

	static std::string staticName(){
		return "TimeLimitExceeded";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ProgramTerminated::getCategory();
		category.append(staticName());
		return category;
	}
};

class MemoryLimitExceeded:public ProgramTerminated{
public:
	explicit MemoryLimitExceeded(
			Json::Value time,
			Json::Value memory
	):ProgramTerminated(std::move(time), std::move(memory)){}

	static std::string staticName(){
		return "MemoryLimitExceeded";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ProgramTerminated::getCategory();
		category.append(staticName());
		return category;
	}
};

class ProgramExited:public ProgramTerminated{
public:
	int ret;

	explicit ProgramExited(
			Json::Value time,
			Json::Value memory,
			const int ret
	):ProgramTerminated(std::move(time), std::move(memory)), ret(ret){}

	static std::string staticName(){
		return "ProgramExited";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ProgramTerminated::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = ProgramTerminated::getJsonObject();
		json["detail"]["ret"] = ret;
		return json;
	};
};
