#pragma once

#include "common.h"
#include "SandboxException.h"

class LaunchFailed:public SandboxException{
public:
	RetValue getRetValue()const override{
		return RetValue::LaunchFailed;
	}

	static std::string staticName(){
		return "LaunchFailed";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = SandboxException::getCategory();
		category.append(staticName());
		return category;
	}
};

class CloneFailed:public LaunchFailed{
public:
	const int errorCode;

	explicit CloneFailed(const int errorCode):errorCode(errorCode){}

	RetValue getRetValue()const override{
		return RetValue::CloneFailed;
	}

	static std::string staticName(){
		return "CloneFailed";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = LaunchFailed::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = LaunchFailed::getJsonObject();
		json["detail"]["errorCode"] = this->errorCode;
		return json;
	};
};

class OpenFileFailed:public LaunchFailed{
public:
	RetValue getRetValue()const override{
		return RetValue::OpenFileFailed;
	}

	static std::string staticName(){
		return "OpenFileFailed";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = LaunchFailed::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = LaunchFailed::getJsonObject();
		return json;
	};
};

class ExecFailed:public LaunchFailed{
public:
	RetValue getRetValue()const override{
		return RetValue::ExecFailed;
	}

	static std::string staticName(){
		return "ExecFailed";
	}

	std::string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = LaunchFailed::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = LaunchFailed::getJsonObject();
		return json;
	};
};
