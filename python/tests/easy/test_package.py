"""Unit test for package.py"""

from drift_protocol.common import DriftPackage as ProtoDriftPackage
from drift_protocol.easy import DriftPackage, TriggerMessage, StatusCode


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
