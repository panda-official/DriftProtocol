# pylint: disable=import-outside-toplevel
""" Test package after build
"""
import os
import pkgutil
import drift_protocol


def test_version():
    """Test that package has version and it is a string"""
    assert drift_protocol.__version__
    assert isinstance(drift_protocol.__version__, str)


def test_modules():
    """Test that package has modules"""
    package_path = os.path.dirname(drift_protocol.__file__)
    modules = [name for _, name, _ in pkgutil.iter_modules([package_path])]

    assert modules


def test_import():
    """Test if no errors during the import"""
    from drift_protocol.common import (
        DriftPackage,
    )

    assert DriftPackage()
