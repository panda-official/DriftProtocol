cmake_minimum_required(VERSION 3.13)

project(drift_protocol_example VERSION 0.1.0)
set(CMAKE_CXX_STANDARD 17)

if (NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
    file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/v0.16.1/conan.cmake"
            "${CMAKE_BINARY_DIR}/conan.cmake"
            EXPECTED_HASH SHA256=396e16d0f5eabdc6a14afddbcfff62a54a7ee75c6da23f32f7a31bc85db23484
            TLS_VERIFY ON)
endif ()

include(${CMAKE_BINARY_DIR}/conan.cmake)
conan_cmake_autodetect(settings)
conan_cmake_install(PATH_OR_REFERENCE ${CMAKE_SOURCE_DIR}/conanfile.txt
        BUILD missing
        SETTINGS ${settings}
        PROFILE ${CONAN_PROFILE})


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()


add_executable(drift_protocol_example main.cc)
target_link_libraries(drift_protocol_example ${CONAN_LIBS})
