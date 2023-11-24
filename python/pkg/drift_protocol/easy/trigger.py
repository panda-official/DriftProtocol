"""Trigger messages"""
import time
from typing import Dict, Optional

from drift_protocol.trigger_service.trigger_message_pb2 import (
    TriggerMessage as ProtoTriggerMessage,
)


class TriggerMessage:
    """Trigger message base class"""

    def __init__(self) -> None:
        self._proto = ProtoTriggerMessage()

    @staticmethod
    def parse(message: bytes) -> "TriggerMessage":
        """
        Parse trigger message

        Args:
            message: Message as bytes

        Returns:
            Trigger message
        """
        trigger = TriggerMessage()
        trigger._proto.ParseFromString(message)
        return trigger

    @staticmethod
    def build(timestamp: Optional[int | float] = None) -> "TriggerMessage":
        """
        Build trigger message

        Args:
            timestamp: Timestamp as float in seconds or int in milliseconds. If None, current time is used.

        Returns:
            Trigger message
        """
        trigger = TriggerMessage()
        if timestamp is None:
            timestamp = time.time()

        timestamp = int(timestamp * 1000) if isinstance(timestamp, float) else timestamp
        trigger._proto.timestamp.FromMilliseconds(timestamp)
        return trigger

    @property
    def timestamp(self) -> float:
        """
        Timestamp in seconds
        """
        return self._proto.timestamp.ToMilliseconds() / 1000
