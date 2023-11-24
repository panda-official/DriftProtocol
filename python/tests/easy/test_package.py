"""Unit test for package.py"""

from drift_protocol.common import DriftPackage as ProtoDriftPackage
from drift_protocol.easy import DriftPackage, TriggerMessage, StatusCode
from drift_protocol.meta import MetaInfo


def test_build_package():
    """Test building package"""
    message = TriggerMessage.build(1_000_000)
    package = DriftPackage.build_from_msg(
        message,
        pkg_id=1_000_000,
        status=StatusCode.GOOD,
        source_timestamp=0,
        publish_timestamp=2_000_000,
    )

    assert package.id > 0
    assert package.status == StatusCode.GOOD
    assert package.source_timestamp == 0
    assert package.publish_timestamp == 2000.0

    new_message = TriggerMessage()
    package.unpack(new_message)

    assert new_message.timestamp == 1000.0


def test_parse_package():
    """Should parse a protobuf message"""
    proto = ProtoDriftPackage()
    proto.id = 1_000_000

    message = proto.SerializeToString()
    package = DriftPackage.parse(message)

    assert package.id == 1_000_000


def test_build_from_typed_data():
    """Should build a package from typed data"""
    values = {
        "int": 100,
        "float": 25.9,
        "string": "test",
        "bool": True,
        "list": [1, 2, 3],
    }

    statuses = {
        "string": StatusCode.BAD,
        "bool": StatusCode.GOOD,
    }

    package = DriftPackage.build_typed_data(
        values,
        statuses,
        pkg_id=1_000_000,
        status=StatusCode.GOOD,
        source_timestamp=0,
        publish_timestamp=2_000_000,
    )

    assert package.id > 0
    assert package.status == StatusCode.GOOD
    assert package.source_timestamp == 0
    assert package.publish_timestamp == 2000.0

    assert package.data_type == MetaInfo.TYPED_DATA
    assert package.as_typed_data() == {
        "int": (100, StatusCode.GOOD),
        "float": (25.9, StatusCode.GOOD),
        "string": ("test", StatusCode.BAD),
        "bool": (True, StatusCode.GOOD),
        "list": ([1, 2, 3], StatusCode.GOOD),
    }
