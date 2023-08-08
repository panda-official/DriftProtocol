from pathlib import Path

from drift_protocol.common import DriftPackage, DataPayload, StatusCode
from drift_protocol.meta import MetaInfo, TypedDataInfo
from drift_bytes import Variant, InputBuffer, OutputBuffer

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.any_pb2 import Any


def create_typed_package() -> bytes:
    global original
    pb_time = Timestamp()
    pb_time.GetCurrentTime()
    DATA = [Variant(False), Variant(1), Variant(3.14), Variant("Hello World")]
    NAMES = ["bool", "int", "float", "string"]

    # Create a package and serialize it
    original = DriftPackage()
    original.id = pb_time.ToMilliseconds()
    original.source_timestamp.CopyFrom(pb_time)
    original.publish_timestamp.CopyFrom(pb_time)
    original.status = StatusCode.GOOD
    # Fill meta data
    info = TypedDataInfo()
    for name in NAMES:
        var = TypedDataInfo.Item()
        var.name = name
        var.status = StatusCode.GOOD
        info.items.append(var)
    original.meta.type = MetaInfo.TYPED_DATA
    original.meta.typed_data_info.CopyFrom(info)
    # Put data in buffer
    buffer = OutputBuffer()
    for var in DATA:
        buffer.push(var)

    # Prepare payload
    payload = DataPayload()
    payload.data = buffer.bytes()
    msg = Any()
    msg.Pack(payload)
    original.data.append(msg)

    label = DriftPackage.Label()
    label.key = "host_name"
    label.value = "my_host"
    original.labels.append(label)

    label = DriftPackage.Label()
    label.key = "topic"
    label.value = "opcua"
    original.labels.append(label)

    # Serialize package to message
    return original.SerializeToString()


def parse_typed_data(message: bytes) -> None:
    # Parse the package
    new_package = DriftPackage()
    new_package.ParseFromString(message)
    print(
        f"Package ID={new_package.id} type={MetaInfo.DataType.Name(new_package.meta.type)}"
    )

    print("Labels:")
    for label in new_package.labels:
        print(f"{label.key}={label.value}")

    payload = DataPayload()
    new_package.data[0].Unpack(payload)
    buffer = InputBuffer(payload.data)

    print("Values:")
    for i, var in enumerate(new_package.meta.typed_data_info.items):
        print(f"{var.name}={buffer.pop().value}, status={var.status}")


if __name__ == "__main__":
    message = create_typed_package()
    parse_typed_data(message)
