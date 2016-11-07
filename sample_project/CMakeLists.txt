cmake_minimum_required(VERSION 2.8.12)
project(MakeOrderSample)

include(build/conanbuildinfo.cmake)
conan_basic_setup()
include_directories(include build)
add_compile_options(-std=c++11)

add_executable(makeorder makeorder.cpp)
target_link_libraries(makeorder ${CONAN_LIBS})
