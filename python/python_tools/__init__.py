""" Tools to generate protobuf bindings for Python
"""
from .generator import (
    generate_proto,
    PROTO_SPEC_FOLDER,
    ProtoCompiler,
    get_compiler_version,
)
