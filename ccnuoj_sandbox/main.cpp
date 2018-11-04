#include <iostream>
#include <memory>

#include "common.h"
#include "SandboxException.h"

using namespace std;

SandboxException::RetValue main_Internal(){
	ifstream configFile;
	configFile.open("config.json", ios::in);
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

int main(){
	SyscallList_Init();

	int ret = static_cast<int>(main_Internal());

	return ret;
}
