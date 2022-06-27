""" Tools to generate ProtoBuf bindings from proto-files
"""
import subprocess
import sys
import os
from pathlib import Path
from distutils.spawn import find_executable

ROOT_FOLDER = Path(__file__).parent.parent.parent.resolve()
PROTO_SPEC_FOLDER = ROOT_FOLDER / "proto_specs"
PROTO_OUT_FOLDER = Path("./proto")


def find_protocol_compiler() -> str:
    """Find protoc compiler in PATH or use PROTOC env"""
    if "PROTOC" in os.environ and os.path.exists(os.environ["PROTOC"]):
        protoc = os.environ["PROTOC"]
    else:
        protoc = find_executable("protoc")

    if protoc is None:
        raise RuntimeError("protoc is not installed")
    return protoc


def get_compiler_version() -> str:
    """Figure out version of the compiler"""
    protoc_command = [find_protocol_compiler(), "--version"]

    ret = subprocess.run(protoc_command, capture_output=True, check=True)

    version = str(ret.stdout)[12:-3]
    print(f"Protoc version: {version}")
    return version


class ProtoCompiler:
    """Protobuf compiler that generates python bindings"""

    def __init__(self, output_dir: str, includes=()):
        self.protoc = find_protocol_compiler()
        self.includes = [f"-I{(PROTO_SPEC_FOLDER / p).resolve()}" for p in includes]
        self.output_dir = Path(output_dir)

    def module_path_from_proto(self, source: Path) -> Path:
        """Gets output filename from proto-file"""
        output_basename = source.name.replace(".proto", "_pb2.py")
        return self.package_path_from_proto(source) / output_basename

    @staticmethod
    def module_name_from_proto(source: Path) -> str:
        """Get module's name from proto-file's name"""
        return source.name.replace(".proto", "_pb2")

    def package_path_from_proto(self, source: Path) -> Path:
        """Get package's name from proto-file's name"""
        return self.output_dir / source.parent

    def generate_proto(self, source: str, create_package=True) -> str:
        """Invokes the Protocol Compiler to generate a _pb2.py from the given
        .proto file.  Does nothing if the output already exists and
        is newer than the input.
        """
        source_path = PROTO_SPEC_FOLDER / source
        if not source_path.exists():
            raise RuntimeError(f"Can't find required file: {source_path}\n")

        output_path = self.module_path_from_proto(Path(source))
        if os.path.exists(output_path):
            if source_path.stat().st_mtime <= output_path.stat().st_mtime:
                print(f"Proto file `{output_path}` already generated, skipping..")
                return str(output_path)

        if create_package:
            self._create_package(Path(source))

        print(f"Generating {output_path}...")
        includes = (f"-I{source_path.parent.resolve()}", *self.includes)
        protoc_command = [
            self.protoc,
            *includes,
            f"--python_out={output_path.parent}",
            str(source_path),
        ]

        if subprocess.call(protoc_command) != 0:
            sys.exit(-1)

        return str(output_path)

    def _create_package(self, path: Path):
        """Create package folder(s) and __init__.py file"""
        print("Create package", path.parent)
        package_path = self.package_path_from_proto(path)
        package_path.mkdir(parents=True, exist_ok=True)

        print("Create __init__.py file")
        init_path = package_path / "__init__.py"
        init_path.touch()

        module_name = self.module_name_from_proto(path)
        with init_path.open("a") as file:
            file.write(f"from .{module_name} import *\n")


def generate_proto(source: str, dest: str = str(PROTO_OUT_FOLDER)) -> str:
    """Call protobuf compiler and return filename of generated python file

    :param source: protobuf filename
    :param dest: output folder
    :return: generated python file
    """
    compiler = ProtoCompiler(output_dir=dest, includes=["."])
    generated_filename = compiler.generate_proto(source)

    return generated_filename
