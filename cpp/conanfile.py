import os

from conans import ConanFile, CMake, tools


class DriftFrameworkConan(ConanFile):
    name = "drift_protocol"
    version = "0.2.0"

    license = "MPL-2.0"
    author = "PANDA GmbH"
    url = "https://github.com/panda-official/DriftProtocol.git"
    description = "Protobuf Library to encode message in Drift infrastructure"
    topics = ("protobuf",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    requires = ("protobuf/[>=3.12.4, <=3.20]",)

    def set_version(self):
        suffix = os.getenv("VERSION_SUFFIX")
        if suffix:
            self.version += f"-b.{suffix}"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        local_source = os.getenv("CONAN_SOURCE_DIR")
        if local_source is not None:
            self.run(
                "cp %s -r %s"
                % (os.getenv("CONAN_SOURCE_DIR"), f"{self.source_folder}/{self.name}")
            )
        else:
            branch = f"v{self.version}" if self.channel == "stable" else self.channel
            self.run(
                f"git clone --branch={branch}"
                f" https://github.com/panda-official/DriftProtocol.git {self.name}"
            )

    def build(self):
        cmake = CMake(self)
        self.run(
            "cmake -DCMAKE_BUILD_TYPE=Release %s/drift_protocol/cpp  %s"
            % (self.source_folder, cmake.command_line)
        )
        self.run("cmake --build . -- -j")

    def package(self):
        self.copy(
            "*.h",
            dst="include/drift_protocol",
            src=f"{self.build_folder}/drift_protocol",
        )
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["drift_protocol"]
