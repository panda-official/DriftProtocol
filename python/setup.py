import os
import re
from collections import abc
from functools import partial
from pathlib import Path
from string import Template

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

from python_tools import PROTO_SPEC_FOLDER, ProtoCompiler, get_compiler_version

MAJOR_VERSION = 0
MINOR_VERSION = 6
PATCH_VERSION = 0

PROTOBUF_VERSION = "3.12.4"  # DON'T REMOVE WE USE IT CI
VERSION_SUFFIX = os.getenv("VERSION_SUFFIX")
PACKAGE_NAME = "drift-protocol"

HERE = Path(__file__).parent.resolve()
PROTO_OUTPUT_PATH = HERE / "pkg"


def get_file_content(path):
    with open(path, "r", encoding="utf-8") as fp:
        return fp.read()


def read_version_from_package(path):
    """Get version from package's __init__ file"""
    version_file = get_file_content(path)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def update_package_version(path: Path, version: str, protoc_version: str):
    """Overwrite/create __init__.py file and fill __version__"""
    template = (path / "__init__.py.in").read_text(encoding="utf-8")
    init_content = Template(template).substitute(
        version=version, protoc_version=protoc_version
    )
    with open(path / "__init__.py", "w") as f:
        f.write(init_content)

    with open(path.parent / "drift" / "__init__.py", "w") as f:
        f.write(init_content)


def build_version():
    """Build dynamic version and update version in package"""
    version = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}"
    if VERSION_SUFFIX:
        version += f"dev.{VERSION_SUFFIX}"

    update_package_version(
        PROTO_OUTPUT_PATH / PACKAGE_NAME.replace("-", "_"),
        version=version,
        protoc_version=get_compiler_version(),
    )

    return version


def read_requirements_file(filename: Path):
    """Process requirements file and handle -r lines (include files)"""
    requirements = []

    with open(filename) as file:
        for line in file:
            line = line.strip()
            if line.startswith("-r"):
                included_filename = filename.parent / line.split()[1]
                requirements.extend(read_requirements_file(included_filename))
            else:
                requirements.append(line)

    return requirements


def get_long_description(base_path: Path):
    return (base_path / "README.md").read_text(encoding="utf-8")


class BuildPyWithProtobuf(build_py):
    """Custom BuildPy command that generate protobuf bindings"""

    def run(self):
        compiler = ProtoCompiler(output_dir=str(PROTO_OUTPUT_PATH), includes=["."])
        for proto_filename in PROTO_SPEC_FOLDER.glob("**/*.proto"):
            proto_filename = proto_filename.relative_to(PROTO_SPEC_FOLDER)
            print("Generate pb2 file from ", proto_filename)

            compiler.generate_proto(proto_filename)

        # _build_py is an old-style class, so super() doesn't work
        build_py.run(self)


class InstallThatRunBuildPyFirst(install):
    def run(self):
        self.run_command("build_py")
        return install.run(self)


class EggInfoThatRunBuildPyFirst(egg_info):
    def run(self):
        self.run_command("build_py")
        return egg_info.run(self)


class LazyPackageFinder(abc.Sequence):
    def __init__(self, finder):
        self._packages = None
        self._finder = finder

    def __len__(self) -> int:
        return len(self.packages)

    def __getitem__(self, index):
        return self.packages[index]

    @property
    def packages(self):
        self._packages = self._packages or self._finder()
        return self._packages


setup(
    cmdclass={
        "install": InstallThatRunBuildPyFirst,
        "build_py": BuildPyWithProtobuf,
        "egg_info": EggInfoThatRunBuildPyFirst,
    },
    name=PACKAGE_NAME,
    version=build_version(),
    description="Protobuf Libraries to encode message in Drift infrastructure",
    long_description=get_long_description(HERE),
    long_description_content_type="text/markdown",
    url="https://github.com/panda-official/DriftProtocol/",
    author="PANDA, GmbH",
    author_email="info@panda.technology",
    package_dir={"": "pkg"},
    packages=LazyPackageFinder(finder=partial(find_packages, where="pkg")),
    python_requires=">=3.7",
    install_requires=[f"protobuf>={PROTOBUF_VERSION}, <=3.20.3", "betterproto[compiler]>=2.0.0b6"],
)
