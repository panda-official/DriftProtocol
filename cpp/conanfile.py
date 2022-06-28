import os

from conans import ConanFile, CMake, tools


class DriftFrameworkConan(ConanFile):
    name = "drift_protocol"
    version = "0.1.0"

    license = "MPL-2.0"
    author = "PANDA GmbH"
    url = "https://github.com/panda-official/DriftProtocol.git"
    description = "Protobuf Library to encode message in Drift infrastructure"
    topics = ("protobuf",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"

    requires = ("protobuf/3.11.3",)

    def set_version(self):
        build_id = os.getenv("CI_JOB_ID")
        if build_id and os.getenv("CI_COMMIT_BRANCH"):
            self.version += f"-b.{build_id}"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        local_source = os.getenv("CONAN_SOURCE_DIR")
        if local_source is not None:
            self.run(
                "cp %s -r %s" % (os.getenv("CONAN_SOURCE_DIR"), self.source_folder)
            )
        else:
            branch = f"v{self.version}" if self.channel == "stable" else self.channel
            self.run(
                f"git clone --branch={branch}"
                " https://github.com/panda-official/DriftProtocol.git drift_protocol"
            )

    def build(self):
        cmake = CMake(self)
        self.run(
            "cmake -DCMAKE_BUILD_TYPE=Release %s/cpp  %s"
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
