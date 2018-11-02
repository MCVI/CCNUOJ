#include <cstring>

#include <json/json.h>

#include "common.h"

using namespace std;

static void ReadConfig(SandboxConfig &config, const Json::Value &json){
	if(!json.isObject()){
		throw InvalidConfigFile();
	}

	const Json::Value &programPath = json["programPath"];
	if(programPath.isString()){
		config.programPath = programPath.asString();
	}else{
		throw InvalidConfigFile();
	}

	const Json::Value &timeLimit = json["timeLimit"];
	if(timeLimit.isNumeric()){
		uint64_t num = timeLimit.asUInt64();
		if(num>Config::MaxTimeLimit){
			throw ConfigLimitExceeded();
		}else{
			config.timeLimit = num;
		}
	}else{
		throw InvalidConfigFile();
	}

	const Json::Value &memoryLimit = json["memoryLimit"];
	if(memoryLimit.isNumeric()){
		uint64_t num = memoryLimit.asUInt64();
		if(num>Config::MaxMemoryLimit){
			throw ConfigLimitExceeded();
		}else{
			config.memoryLimit = num;
		}
	}else{
		throw InvalidConfigFile();
	}

	const Json::Value &fileList = json["file"];
	if(fileList.isObject()){
		if(fileList.size()>Config::MaxFileListItemNum){
			throw ConfigLimitExceeded();
		}else{
			config.fileList.resize(fileList.size());

			Json::Value::const_iterator iti=fileList.begin();
			int i=0;
			while(iti!=fileList.end()){
				const Json::Value &key = iti.key();
				SandboxConfig::File &config_file = config.fileList[i];
				auto &config_permission = config_file.permission;
				memset(&config_permission, 0, sizeof(config_permission)); // sizeof(X &) == sizeof(X)

				if(key.isString()){
					const Json::Value &value = *iti;
					if((value.isArray())&&(!value.empty())){
						for(int j=0;j<value.size();i++){
							if(value[j].isString()){
								const string permission_name = value[j].asString();
								if(permission_name=="read"){
									config_permission.read = 1;
								}else if(permission_name=="write"){
									config_permission.write = 1;
								}else{
									throw InvalidConfigFile();
								}
							}else{
								throw InvalidConfigFile();
							}
						}
					}else if(value.isNull()){
						config_permission.read = 1;
						config_permission.write = 0;
					}else{
						throw InvalidConfigFile();
					}
				}else{
					throw InvalidConfigFile();
				}

				iti++;
				i++;
			}
		}
	}else{
		throw InvalidConfigFile();
	}

	const Json::Value &syscallList = json["syscall"];
	if(syscallList.isObject()){
		const Json::Value &syscallAllowList = syscallList["allow"];
		if(syscallAllowList.isArray()){
			config.syscall.clear();

			Json::Value::const_iterator iti=syscallAllowList.begin();
			while(iti!=syscallAllowList.end()){
				auto allow_syscall = [&config](const uint64_t syscall_id){
					if(syscall_id+1>config.syscall.size()){
						config.syscall.resize(syscall_id+1, false);
					}
					config.syscall[syscall_id] = true;
				};

				const Json::Value &syscall = *iti;
				if(syscall.isString()){
					auto iti_map = syscall_name_to_id.find(syscall.asString());
					if(iti_map==syscall_name_to_id.cend()){
						throw UnrecognizedSyscall();
					}else{
						allow_syscall(iti_map->second);
					}
				}else if(syscall.isNumeric()){
					uint64_t syscall_id = syscall.asUInt64();
					if(syscall_id>Config::MaxSyscallID){
						throw UnrecognizedSyscall();
					}else{
						allow_syscall(syscall_id);
					}
				}else{
					throw InvalidConfigFile();
				}
				iti++;
			}
		}else{
			throw InvalidConfigFile();
		}
	}else{
		throw InvalidConfigFile();
	}
}

SandboxConfig SandboxConfig::readFromJSON(ifstream &f){
	Json::Value json;
	SandboxConfig config;

	f>>json;
	ReadConfig(config, json);

	return config;
}
