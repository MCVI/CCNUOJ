#pragma once

#include "common.h"
#include "SandboxException.h"
#include "ChildProcess.h"

class ProgramTerminated: public SandboxException, public ProcessInformation{
public:
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
		this->ProcessInformation::fillDetail(json["detail"]);
		return json;
	}
};

class DangerousBehavior:public ProgramTerminated{
public:
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
			const uint64_t syscallID
	):syscallID(syscallID){}

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
			std::string path
	):path(move(path)){}

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
			const int signal
	):signal(signal){}

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
			const int ret
	):ret(ret){}

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
