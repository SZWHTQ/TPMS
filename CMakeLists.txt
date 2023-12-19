cmake_minimum_required(VERSION 3.15)

project(
    genTPMS
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)

include_directories(
    ${CMAKE_SOURCE_DIR}/include
)

set(srcs)
add_subdirectory(
    ${CMAKE_SOURCE_DIR}/src
)

add_executable(
    ${PROJECT_NAME}
    ${srcs}
)