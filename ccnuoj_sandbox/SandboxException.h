#pragma once

#include <json/json.h>
#include <iostream>

#include "common.h"

class SandboxException{
public:
	enum class RetValue{
		Finished = 0,
		UnknownError = 1,
		FileOperationError = 2,
		CommandLineUsageError = 3,

		ReadConfigError = 10,
		CannotOpenConfigFile = 11,
		ConfigFileParseError = 15,

		ConfigSemanticError = 20,
		ConfigTypeError = 21,
		ConfigLimitExceeded = 22,
		ConfigKeyDuplicated = 23,
		UnrecognizedFile = 24,
		UnrecognizedSyscall = 25,

		LaunchFailed = 30,
		CloneFailed = 31,
		OpenFileFailed = 35,
		ExecFailed = 39,
	};

	virtual ~SandboxException() = default;

	static std::string staticName(){
		return "SandboxException";
	}

	virtual RetValue getRetValue()const=0;

	virtual std::string getName()const{
		return staticName();
	}
	virtual Json::Value getCategory()const{
		Json::Value category;
		category.append(staticName());
		return category;
	}
	virtual Json::Value getJsonObject()const{
		Json::Value json;
		json["name"] = getName();
		json["category"] = getCategory();
		json["detail"] = Json::Value();
		return json;
	}

	friend std::ostream& operator<< (std::ostream &f, const SandboxException &e){
		return f<<e.getJsonObject();
	}
};

class FileOperationError:public SandboxException{
public:
	const std::string path;
	const Json::Value required_operation;

	FileOperationError(
			std::string path,
			Json::Value required_operation
	):path(std::move(path)), required_operation(std::move(required_operation)){}

	RetValue getRetValue()const override{
		return RetValue::FileOperationError;
	}

	static std::string staticName(){
		return "FileOperationError";
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
		json["detail"]["path"] = this->path;
		json["detail"]["requiredOperation"] = this->required_operation;
		return json;
	};
};
