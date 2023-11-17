import os

from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake
from conan.tools.layout import cmake_layout


class HelloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain", "VirtualRunEnv"

    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)
        self.requires("wavelet_buffer/0.6.0@drift/stable")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build_from_msg()

    def layout(self):
        cmake_layout(self)

    def test(self):
        if can_run(self):
            cmd = os.path.join(self.cpp.build_from_msg.bindirs[0], "test_package")
            self.run(cmd, env="conanrun")
