import os

from conans import ConanFile, CMake, tools


class DriftFrameworkConan(ConanFile):
    name = "drift_proto"
    version = "1.2.0"

    license = "CLOSED"
    author = "PANDA GmbH"
    url = "https://gitlab.panda.technology/drift/sdk/drift_proto"
    description = "A collection of protobuf structures and helpers"
    topics = ("protobuf",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    requires = ("protobuf/3.11.3",)

    def set_version(self):
        build_id = os.getenv("CI_JOB_ID")
        if build_id and os.getenv("CI_COMMIT_BRANCH"):
            self.version += f'-b.{build_id}'

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        local_source = os.getenv('CONAN_SOURCE_DIR')
        if local_source is not None:
            self.run("cp %s -r %s" % (os.getenv('CONAN_SOURCE_DIR'), self.source_folder))
        else:
            branch = f'v{self.version}' if self.channel == 'stable' else self.channel
            self.run(f'git clone --branch={branch}'
                     ' git@gitlab.panda.technology:drift/sdk/drift_proto.git drift_proto')

    def build(self):
        cmake = CMake(self)
        self.run('cmake -DCMAKE_BUILD_TYPE=Release %s/drift_proto  %s'
                 % (self.source_folder, cmake.command_line))
        self.run("cmake --build . -- -j")

    def package(self):
        self.copy("*.h", dst="include/drift_proto", src=f"{self.build_folder}/drift_proto")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["drift_proto"]
