"""Drfit Package"""
import time
from typing import Optional, Dict, Tuple

from google.protobuf.any_pb2 import Any
from drift_protocol.common import (
    DriftPackage as ProtoDriftPackage,
    StatusCode,
    DataPayload,
)
from drift_bytes import Variant, OutputBuffer, InputBuffer

from drift_protocol.meta import TypedDataInfo, MetaInfo


class DriftPackage:
    def __init__(self):
        self._proto = ProtoDriftPackage()

    @staticmethod
    def parse(message):
        """
        Parse drift package

        Args:
            message: Message as bytes

        Returns:
            Drift package
        """
        package = DriftPackage()
        package._proto.ParseFromString(message)
        return package

    @staticmethod
    def build_from_msg(
        message,
        pkg_id: Optional[int | float] = None,
        status: StatusCode = StatusCode.GOOD,
        **kwargs
    ) -> "DriftPackage":
        """
        Build drift package

        Args:
            message: Message to be packed
            pkg_id: ID as timestamp as float in seconds or int in milliseconds. If None, current time is used.
            status: Status code

        Keyword Args:
            publish_timestamp (int | float): Publish timestamp as float in seconds or int in milliseconds.
                If None, current time is used.
            source_timestamp (int | float): Source timestamp as float in seconds or int in milliseconds.
                If None, current time is used.
        Returns:
            Drift package
        """
        package = DriftPackage()
        if pkg_id is None:
            pkg_id = time.time()

        pkg_id = int(pkg_id * 1000) if isinstance(pkg_id, float) else pkg_id
        package._proto.id = pkg_id
        package._proto.status = status

        publish_timestamp = kwargs.get("publish_timestamp", time.time())
        if isinstance(publish_timestamp, float):
            publish_timestamp = int(publish_timestamp * 1000)
        package._proto.publish_timestamp.FromMilliseconds(publish_timestamp)

        source_timestamp = kwargs.get("source_timestamp", time.time())
        if isinstance(source_timestamp, float):
            source_timestamp = int(source_timestamp * 1000)
        package._proto.source_timestamp.FromMilliseconds(source_timestamp)

        msg = Any()

        if hasattr(message, "_proto"):
            msg.Pack(message._proto)
        else:
            msg.Pack(message)

        package._proto.data.append(msg)

        return package

    @staticmethod
    def build_typed_data(
        values: Dict[str, Variant.SUPPORTED_TYPES],
        statuses: Optional[Dict[str, int]] = None,
        pkg_id: Optional[int | float] = None,
        status: StatusCode = StatusCode.GOOD,
        **kwargs
    ) -> "DriftPackage":
        """
        Build drift package from typed data
        """
        statuses = statuses or {}

        info = TypedDataInfo()

        buffer = OutputBuffer(len(values))
        for idx, entry in enumerate(values.items()):
            name, value = entry
            buffer[idx] = value

            item = TypedDataInfo.Item()
            item.name = name
            item.status = statuses.get(name, StatusCode.GOOD)
            info.items.append(item)

        data_payload = DataPayload()
        data_payload.data = buffer.bytes()

        package = DriftPackage.build_from_msg(
            data_payload, pkg_id=pkg_id, status=status, **kwargs
        )
        package._proto.meta.type = MetaInfo.TYPED_DATA
        package._proto.meta.typed_data_info.CopyFrom(info)

        return package

    @property
    def id(self) -> int:
        """
        Package ID
        """
        return self._proto.id

    @property
    def status(self) -> StatusCode:
        """
        Package status
        """
        return self._proto.status

    @property
    def publish_timestamp(self) -> float:
        """
        Publish timestamp in seconds
        """
        return self._proto.publish_timestamp.ToMilliseconds() / 1000

    @property
    def source_timestamp(self) -> float:
        """
        Source timestamp in seconds
        """
        return self._proto.source_timestamp.ToMilliseconds() / 1000

    @property
    def data_type(self):
        """
        Data type

        Returns:
            Data type or None if there is no meta info
        """
        if self._proto.meta:
            return self._proto.meta.type
        return None

    def as_typed_data(self) -> Optional[Dict[str, Tuple[Variant.SUPPORTED_TYPES, int]]]:
        """
        Get typed data

        Returns:
            Typed data or None if there is no meta info
        """
        if self._proto.meta and self._proto.meta.type == MetaInfo.TYPED_DATA:
            data = {}
            payload = DataPayload()
            self._proto.data[0].Unpack(payload)

            buffer = InputBuffer(payload.data)

            for idx, item in enumerate(self._proto.meta.typed_data_info.items):
                data[item.name] = (buffer[idx].value, item.status)
            return data

        return None

    def unpack(self, msg):
        """
        Unpack message it must be either a protobuf message or an "easy" message
        """
        if hasattr(msg, "_proto"):
            self._proto.data[0].Unpack(msg._proto)
        else:
            self._proto.data[0].Unpack(msg)
