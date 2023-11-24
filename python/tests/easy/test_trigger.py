"""Unit tests for trigger.py"""

from drift_protocol.easy import TriggerMessage


def test_build_trigger_message():
    """Test building trigger message"""
    trigger_message = TriggerMessage.build(1_000_000)
    assert trigger_message.timestamp == 1000.0

    trigger_message = TriggerMessage.build(1000.0)
    assert trigger_message.timestamp == 1000.0

    trigger_message = TriggerMessage.build()
    assert trigger_message.timestamp > 0


def test_parse_trigger_message():
    """Test parsing trigger message"""
    trigger_message = TriggerMessage.build(1_000_000)
    message = trigger_message._proto.SerializeToString()

    parsed_trigger_message = TriggerMessage.parse(message)
    assert parsed_trigger_message.timestamp == 1000.0
