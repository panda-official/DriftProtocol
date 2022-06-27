cmake_minimum_required(VERSION 3.13)

project(drift_protocol)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
list(APPEND CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})

if (NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
    file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/v0.16.1/conan.cmake"
            "${CMAKE_BINARY_DIR}/conan.cmake"
            EXPECTED_HASH SHA256=396e16d0f5eabdc6a14afddbcfff62a54a7ee75c6da23f32f7a31bc85db23484
            TLS_VERIFY ON)
endif ()

include(${CMAKE_BINARY_DIR}/conan.cmake)
conan_cmake_autodetect(settings)
conan_cmake_install(PATH_OR_REFERENCE ${CMAKE_SOURCE_DIR}/conanfile.py
        BUILD missing
        SETTINGS ${settings}
        PROFILE ${CONAN_PROFILE})


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

message(STATUS "Protobuf exe  ${Protobuf_PROTOC_EXECUTABLE}")

include(cmake/ProtobufGen.cmake)

add_library(drift_protocol STATIC ${PROTOBUF_FILES})
target_link_libraries(drift_protocol
        ${CONAN_LIBS}
        )

target_include_directories(drift_protocol SYSTEM PUBLIC
        ${CMAKE_BINARY_DIR}/)
