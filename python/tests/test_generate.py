""" Tests for generator
"""

from time import time, sleep
from pathlib import Path

import pytest

from python.python_tools import generate_proto, PROTO_SPEC_FOLDER


def test__generate_proto_for_all_protofiles(tmp_path):
    """All proto-files must be generated without errors"""
    now = time()
    for proto_filename in PROTO_SPEC_FOLDER.glob("**/*.proto"):
        proto_filename = proto_filename.relative_to(PROTO_SPEC_FOLDER)
        out_filename = generate_proto(str(proto_filename), dest=str(tmp_path))
        assert Path(out_filename).stat().st_mtime > now


def test__generate_proto_for_unknown_path(tmp_path):
    """If specified proto-file doesn't exist the error must be raised"""
    proto_filename = PROTO_SPEC_FOLDER / "unknown.proto"
    error_message = f"Can't find required file: {str(proto_filename)}"
    with pytest.raises(RuntimeError, match=error_message):
        generate_proto(str(proto_filename), dest=str(tmp_path))


def test__generate_proto_when_already_generated(tmp_path):
    """Py-file doesn't need to be updated if proto-file is the same"""
    for proto_filename in PROTO_SPEC_FOLDER.glob("**/*.proto"):
        proto_filename = proto_filename.relative_to(PROTO_SPEC_FOLDER)
        generate_proto(str(proto_filename), dest=str(tmp_path))

    for proto_filename in PROTO_SPEC_FOLDER.glob("**/*.proto"):
        proto_filename = proto_filename.relative_to(PROTO_SPEC_FOLDER)
        generate_proto(str(proto_filename), dest=str(tmp_path))

    now = time()
    for generated_file in tmp_path.glob("**/*.proto"):
        assert Path(generated_file).stat().st_mtime < now


def test__generate_proto_when_updated(tmp_path):
    """Py-file must be updated when proto-file changed"""
    file_to_touch = next(PROTO_SPEC_FOLDER.glob("**/*.proto"))
    file_to_touch = file_to_touch.relative_to(PROTO_SPEC_FOLDER)
    out_filename = generate_proto(str(file_to_touch), dest=str(tmp_path))
    # disk cache makes it instant
    sleep(0.01)
    (PROTO_SPEC_FOLDER / file_to_touch).touch()
    st_mtime = Path(out_filename).stat().st_mtime

    generate_proto(str(file_to_touch), dest=str(tmp_path))

    assert Path(out_filename).stat().st_mtime > st_mtime
