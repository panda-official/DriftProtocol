cmake_minimum_required(VERSION 3.13)

project(drift_protocol_examples VERSION 0.1.0)
set(CMAKE_CXX_STANDARD 17)

find_package(wavelet_buffer REQUIRED)
find_package(drift_protocol REQUIRED)

add_executable(test_package drift_package_example.cc)
target_link_libraries(test_package wavelet_buffer::wavelet_buffer
  drift_protocol::drift_protocol)

