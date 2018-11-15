cmake_minimum_required(VERSION 3.12)
project(ccnuoj_sandbox)

set(CMAKE_CXX_STANDARD 17)

include(ExternalProject)
externalproject_add(
        jsoncpp
        URL https://github.com/open-source-parsers/jsoncpp/archive/1.8.4.tar.gz
        URL_HASH SHA512=f70361a3263dd8b9441374a9a409462be1426c0d6587c865171a80448ab73b3f69de2b4d70d2f0c541764e1e6cccc727dd53178347901f625ec6fb54fb94f4f1
        PREFIX ${CMAKE_CURRENT_BINARY_DIR}/jsoncpp-prefix
        CMAKE_ARGS -DBUILD_STATIC_LIBS=ON -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}/jsoncpp-prefix
)

externalproject_get_property(jsoncpp INSTALL_DIR)
include_directories(${INSTALL_DIR}/include)
link_directories(${INSTALL_DIR}/lib64)

add_executable(ccnuoj_sandbox)

target_sources(ccnuoj_sandbox PUBLIC main.cpp)
target_sources(ccnuoj_sandbox PUBLIC syscall_list.cpp)
target_sources(ccnuoj_sandbox PUBLIC config.cpp)
target_sources(ccnuoj_sandbox PUBLIC run.cpp)
target_sources(ccnuoj_sandbox PUBLIC SyscallHandler.cpp)
target_sources(ccnuoj_sandbox PUBLIC ChildProcess.cpp)

target_link_libraries(ccnuoj_sandbox stdc++fs)
target_link_libraries(ccnuoj_sandbox libjsoncpp.a)
