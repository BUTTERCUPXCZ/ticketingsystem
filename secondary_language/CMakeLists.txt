cmake_minimum_required(VERSION 3.10)

# Project name and version
project(PLProject VERSION 1.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)
# Add source directory
add_executable(PLProject src/main.cpp src/utils.cpp)

