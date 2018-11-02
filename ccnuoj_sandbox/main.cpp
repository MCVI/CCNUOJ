#include <iostream>
#include <memory>

#include "common.h"

using namespace std;

int main(){
	SyscallList_Init();

	ifstream configFile;
	configFile.open("config.json", ios::in);
	if(configFile.is_open()){
		unique_ptr<const SandboxConfig> config;
		try{
			config = move(make_unique<SandboxConfig>(SandboxConfig::readFromJSON(configFile)));
		}catch(ReadConfigError){
			return 2;
		}

		Run(*(config.get()));

		return 0;
	}else{
		fprintf(stderr, "Error: Failed to open 'config.json'.\n");
		return 1;
	}
}
