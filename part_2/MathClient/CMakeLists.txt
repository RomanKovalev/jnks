# MathClient/CMakeLists.txt

cmake_minimum_required(VERSION 3.10)
project(MathClient)

add_executable(MathClient MathClient.cpp)

target_link_libraries(MathClient PRIVATE MathLibrary)