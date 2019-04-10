#include <iostream>
#include <memory>

#include "common.h"
#include "SandboxException.h"

using namespace std;

SandboxException::RetValue main_Internal(const char *config_file_path){
	ifstream configFile;
	configFile.open(config_file_path, ios::in);
	if(!configFile.is_open()){
		return SandboxException::RetValue::CannotOpenConfigFile;
	}

	SandboxConfig config;
	try{
		ReadConfigFromFile(config, configFile);
	}catch(SandboxException &e){
		if(config.sandboxOutput){
			(*config.sandboxOutput)<<e;
		}else{
			cerr<<e;
		}
		return e.getRetValue();
	}

	try{
		Run(config);
	}catch(SandboxException &e){
		(*config.sandboxOutput)<<e;
	}
	return SandboxException::RetValue::Finished;
}

int main(int argc, char *(argv[])){
	SandboxException::RetValue ret;
	if(argc == 2){
		SyscallList_Init();
		ret = main_Internal(argv[1]);
	}else{
		ret = SandboxException::RetValue::CommandLineUsageError;
	}
	return static_cast<int>(ret);
}
