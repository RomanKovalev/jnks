# MathLibrary/CMakeLists.txt

cmake_minimum_required(VERSION 3.10)
project(MathLibrary)

add_library(MathLibrary STATIC MathLibrary.cpp MathLibrary.h)

target_include_directories(MathLibrary PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})