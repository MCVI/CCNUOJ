#include <cstring>
#include <cassert>

#include "common.h"
#include "SandboxException.h"

using namespace std;

class ReadConfigError:public SandboxException{
public:
	static std::string staticName(){
		return "ReadConfigError";
	}

	string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = SandboxException::getCategory();
		category.append(staticName());
		return category;
	}
};

class ConfigFileParseError:public ReadConfigError{
public:
	const string message;

	explicit ConfigFileParseError(string message):message(move(message)){}

	RetValue getRetValue()const override{
		return RetValue::ConfigFileParseError;
	}

	static std::string staticName(){
		return "ConfigFileParseError";
	}

	string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ReadConfigError::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = ReadConfigError::getJsonObject();
		json["detail"]["message"] = message;
		return json;
	};
};

class ConfigSemanticError:public ReadConfigError{
public:
	const string keyName;

	explicit ConfigSemanticError(string keyName):keyName(move(keyName)){}

	static std::string staticName(){
		return "ConfigSemanticError";
	}

	string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ReadConfigError::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = ReadConfigError::getJsonObject();
		json["detail"]["keyName"] = keyName;
		return json;
	};
};

class ConfigTypeError:public ConfigSemanticError{
public:
	const Json::ValueType required;
	const Json::ValueType actual;

	ConfigTypeError(
			string keyName,
			const Json::ValueType required,
			const Json::ValueType actual
	):ConfigSemanticError(move(keyName)), required(required), actual(actual){}

	RetValue getRetValue()const override{
		return RetValue::ConfigTypeError;
	}

	static std::string staticName(){
		return "ConfigTypeError";
	}

	string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ConfigSemanticError::getCategory();
		category.append(staticName());
		return category;
	}

	static string valueTypeName(Json::ValueType type){
		switch(type){
			case Json::ValueType::stringValue:
				return "string";

			case Json::ValueType::intValue:
			case Json::ValueType::uintValue:
			case Json::ValueType::realValue:
				return "number";

			case Json::ValueType::objectValue:
				return "object";

			case Json::ValueType::arrayValue:
				return "array";

			case Json::ValueType::booleanValue:
				return "boolean";

			case Json::ValueType::nullValue:
				return "null";

			default:
				throw std::runtime_error("Unrecognized Json ValueType");
		}
	}

	Json::Value getJsonObject()const override{
		Json::Value json = ConfigSemanticError::getJsonObject();
		json["detail"]["required"] = valueTypeName(required);
		json["detail"]["actual"] = valueTypeName(actual);
		return json;
	};
};

class ConfigLimitExceeded:ConfigSemanticError{
public:
	const Json::Value limit;
	const Json::Value actual;

	ConfigLimitExceeded(
			string keyName,
			Json::Value limit,
			Json::Value actual
	):ConfigSemanticError(move(keyName)), limit(move(limit)), actual(move(actual)){}

	RetValue getRetValue()const override{
		return RetValue::ConfigLimitExceeded;
	}

	static std::string staticName(){
		return "ConfigLimitExceeded";
	}

	string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ConfigSemanticError::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = ConfigSemanticError::getJsonObject();
		json["detail"]["limit"] = limit;
		json["detail"]["actual"] = actual;
		return json;
	};
};

class UnrecognizedSyscall:ConfigSemanticError{
public:
	const Json::Value unrecognized;

	UnrecognizedSyscall(
			string keyName,
			Json::Value unrecognized
	):ConfigSemanticError(move(keyName)), unrecognized(move(unrecognized)){}

	RetValue getRetValue()const override{
		return RetValue::UnrecognizedSyscall;
	}

	static std::string staticName(){
		return "UnrecognizedSyscall";
	}

	string getName()const override{
		return staticName();
	}

	Json::Value getCategory()const override{
		Json::Value category = ConfigSemanticError::getCategory();
		category.append(staticName());
		return category;
	}

	Json::Value getJsonObject()const override{
		Json::Value json = ConfigSemanticError::getJsonObject();
		json["detail"]["unrecognized"] = unrecognized;
		return json;
	};
};


template<Json::ValueType type>
inline auto requireType(const string &key, const Json::Value &value);
template<>
inline auto requireType<Json::ValueType::nullValue>(const string &key, const Json::Value &value){
	if(value.isNull()){
		return;
	}else{
		throw ConfigTypeError(key, Json::ValueType::nullValue, value.type());
	}
}
template<>
inline auto requireType<Json::ValueType::booleanValue>(const string &key, const Json::Value &value){
	if(value.isBool()){
		return value.asBool();
	}else{
		throw ConfigTypeError(key, Json::ValueType::booleanValue, value.type());
	}
}
template<>
inline auto requireType<Json::ValueType::intValue>(const string &key, const Json::Value &value){
	if(value.isInt64()){
		return value.asInt64();
	}else{
		throw ConfigTypeError(key, Json::ValueType::intValue, value.type());
	}
}
template<>
inline auto requireType<Json::ValueType::uintValue>(const string &key, const Json::Value &value){
	if(value.isUInt64()){
		return value.asUInt64();
	}else{
		throw ConfigTypeError(key, Json::ValueType::uintValue, value.type());
	}
}
template<>
inline auto requireType<Json::ValueType::realValue>(const string &key, const Json::Value &value){
	if(value.isDouble()){
		return value.asDouble();
	}else{
		throw ConfigTypeError(key, Json::ValueType::realValue, value.type());
	}
}
template<>
inline auto requireType<Json::ValueType::stringValue>(const string &key, const Json::Value &value){
	if(value.isString()){
		return value.asString();
	}else{
		throw ConfigTypeError(key, Json::ValueType::stringValue, value.type());
	}
}
template<>
inline auto requireType<Json::ValueType::arrayValue>(const string &key, const Json::Value &value){
	if(value.isArray()){
		return value;
	}else{
		throw ConfigTypeError(key, Json::ValueType::arrayValue, value.type());
	}
}
template<>
inline auto requireType<Json::ValueType::objectValue>(const string &key, const Json::Value &value){
	if(value.isObject()){
		return value;
	}else{
		throw ConfigTypeError(key, Json::ValueType::objectValue, value.type());
	}
}

inline static uint64_t requireUInt64Limit(
		const string &key,
		const Json::Value &value,
		const uint64_t min,
		const uint64_t max
){
	const uint64_t num = requireType<Json::ValueType::uintValue>(key, value);

	if(num<min||num>max){
		Json::Value limit;
		limit["min"] = min;
		limit["max"] = max;
		throw ConfigLimitExceeded(key, limit, num);
	}else{
		return num;
	}
}

inline static const Json::Value& requireObjectLimit(
		const string &key,
		const Json::Value &value,
		const uint64_t maxSize
){
	const Json::Value &object = requireType<Json::ValueType::objectValue>(key, value);

	if(object.size()>maxSize){
		Json::Value limit, actual;
		limit["maxSize"] = maxSize;
		actual["size"] = object.size();
		throw ConfigLimitExceeded(key, limit, actual);
	}else{
		return value;
	}
}

inline static const Json::Value& requireNonEmptyArray(
		const string &key,
		const Json::Value &value
){
	const Json::Value &array = requireType<Json::ValueType::arrayValue>(key, value);
	if(array.empty()){
		Json::Value limit, actual;
		limit["empty"] = false;
		actual["empty"] = true;
		throw ConfigLimitExceeded(key, limit, actual);
	}else{
		return value;
	}
}

static void ReadConfigFromJson(SandboxConfig &config, const Json::Value &json){
	Json::Value::const_iterator iti;

	requireType<Json::ValueType::objectValue>("", json);

	string sandboxOutput_path = requireType<Json::ValueType::stringValue>("sandboxOutput", json["sandboxOutput"]);
	unique_ptr<ofstream> sandboxOutput_file = make_unique<ofstream>(ofstream());
	sandboxOutput_file->open(sandboxOutput_path, ios::out);
	if(sandboxOutput_file->is_open()){
		config.sandboxOutput = move(sandboxOutput_file);
	}else{
		Json::Value required_operation;
		required_operation.append("write");
		throw FileOperationError(sandboxOutput_path, required_operation);
	}

	config.programPath = requireType<Json::ValueType::stringValue>("programPath", json["programPath"]);
	config.timeLimit = requireUInt64Limit("timeLimit", json["timeLimit"], 0, Config::MaxTimeLimit);
	config.memoryLimit = requireUInt64Limit("memoryLimit", json["memoryLimit"], 0, Config::MaxMemoryLimit);

	const Json::Value &fileList = requireObjectLimit("file", json["file"], Config::MaxFileListItemNum);
	config.fileList.resize(fileList.size());

	iti=fileList.begin();
	int i=0;
	while(iti!=fileList.end()){
		SandboxConfig::File &config_file = config.fileList[i];

		config_file.filename = requireType<Json::ValueType::stringValue>(
				"file::keyType["+iti.key().toStyledString()+"]",
				iti.key()
		);
		const string key = "file.\'" + config_file.filename + "\'";

		auto &config_permission = config_file.permission;
		memset(&config_permission, 0, sizeof(config_permission)); // sizeof(X &) == sizeof(X)

		const Json::Value &value = *iti;
		if(value.isArray()){
			const Json::Value &array = requireNonEmptyArray(key, *iti);
			for(int j=0;j<array.size();j++){
					const string permission_key = key+"["+to_string(j)+"]";
					const string permission_name = requireType<Json::ValueType::stringValue>(permission_key, array[j]);
					if(permission_name=="read"){
						config_permission.read = 1;
					}else if(permission_name=="write"){
						config_permission.write = 1;
					}else{
						Json::Value limit, allow_value;
						allow_value.append("read");
						allow_value.append("write");
						limit["array"] = allow_value;
						throw ConfigLimitExceeded(permission_key, limit, permission_name);
					}
			}
		}else if(value.isNull()){
			config_permission.read = 1;
			config_permission.write = 0;
		}else{
			throw ConfigTypeError(
					"file.\'"+key+"\'",
					Json::ValueType::objectValue,
					value.type()
			);
		}

		iti++;
		i++;
	}

	const Json::Value &syscallList = requireType<Json::ValueType::objectValue>("syscall", json["syscall"]);
	const Json::Value &syscallAllowList = requireType<Json::ValueType::arrayValue>("syscall.allow", syscallList["allow"]);
	config.allowedSyscall.clear();

	iti=syscallAllowList.begin();
	while(iti!=syscallAllowList.end()){
		const Json::Value &syscall = *iti;
		if(syscall.isString()){
			const string syscall_name = syscall.asString();
			auto iti_map = syscall_name_to_id.find(syscall_name);
			if(iti_map==syscall_name_to_id.cend()){
				throw UnrecognizedSyscall("syscall.allow", syscall_name);
			}else{
				config.allowedSyscall.insert(iti_map->second);
			}
		}else if(syscall.isNumeric()){
			uint64_t syscall_id = syscall.asUInt64();
			if(syscall_id>Config::MaxSyscallID){
				throw UnrecognizedSyscall("syscall.allow", syscall_id);
			}else{
				config.allowedSyscall.insert(syscall_id);
			}
		}else{
			throw ConfigTypeError(
					"syscall.allow::keyType["+iti.key().toStyledString()+"]",
					Json::ValueType::stringValue,
					iti.key().type()
			);
		}
		iti++;
	}
}

void ReadConfigFromFile(SandboxConfig &config, ifstream &f){
	Json::CharReaderBuilder builder;
	string errorMessage;

	Json::Value json;

	if(Json::parseFromStream(builder, f, &json, &errorMessage)){
		ReadConfigFromJson(config, json);
	}else{
		throw ConfigFileParseError(errorMessage);
	}
}
