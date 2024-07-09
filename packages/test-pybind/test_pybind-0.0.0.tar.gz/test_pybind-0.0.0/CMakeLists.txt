# define minimum cmake version
cmake_minimum_required(VERSION 3.11 FATAL_ERROR)

# project name and supported language
project(test_pybind LANGUAGES CXX)

# require C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# for testing we will need the python interpreter
find_package(PythonInterp REQUIRED)

add_subdirectory(test_pybind)

# turn on testing
enable_testing()

# define test
add_test(
        NAME
                python_test
        COMMAND
                ${CMAKE_COMMAND} -E env ACCOUNT_MODULE_PATH=$<TARGET_FILE_DIR:test_pybind>
                ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/test_pybind/test.py
        )
install(
        TARGETS
                test_pybind
        LIBRARY
                DESTINATION test_pybind
        )