from pathlib import Path
import numpy as np

from drift_protocol.common import DriftPackage, DataPayload, StatusCode
from drift_protocol.meta import MetaInfo, ScalarValuesInfo
from wavelet_buffer import denoise, WaveletType, WaveletBuffer

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.any_pb2 import Any

IMG_PATH = Path(__file__).parent / "pandas.jpg"


def create_scalar_package() -> bytes:
    global original
    pb_time = Timestamp()
    pb_time.GetCurrentTime()
    DATA = np.array([0, 10.0, 0.3, 1], dtype=np.float32)
    NAMES = ["x0", "x1", "x2", "x3"]
    # Create a package and serialize it
    original = DriftPackage()
    original.id = pb_time.ToMilliseconds()
    original.source_timestamp.CopyFrom(pb_time)
    original.publish_timestamp.CopyFrom(pb_time)
    original.status = StatusCode.GOOD
    # Fill meta data
    info = ScalarValuesInfo()
    for name in NAMES:
        var = ScalarValuesInfo.VariableInfo()
        var.name = name
        var.status = StatusCode.GOOD
        info.variables.append(var)
    original.meta.type = MetaInfo.SCALAR_VALUES
    original.meta.scalar_info.CopyFrom(info)
    # Put data in buffer without decomposition and compression
    buffer = WaveletBuffer(
        signal_shape=[len(DATA)],
        signal_number=1,
        decomposition_steps=0,
        wavelet_type=WaveletType.NONE,
    )
    buffer.decompose(DATA, denoise.Null())
    # Prepare payload
    payload = DataPayload()
    payload.data = buffer.serialize(compression_level=0)
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


def parse_scalar_package(message: bytes) -> None:
    # Parse the package
    new_pacakge = DriftPackage()
    new_pacakge.ParseFromString(message)
    print(
        f"Package ID={new_pacakge.id} type={MetaInfo.DataType.Name(new_pacakge.meta.type)}"
    )

    print("Labels:")
    for label in new_pacakge.labels:
        print(f"{label.key}={label.value}")

    payload = DataPayload()
    new_pacakge.data[0].Unpack(payload)
    buffer = WaveletBuffer.parse(payload.data)
    values = buffer.compose()

    print("Values:")
    for i, var in enumerate(new_pacakge.meta.scalar_info.variables):
        print(f"{var.name}=value={values[i]}, status={var.status}")


if __name__ == "__main__":
    message = create_scalar_package()
    parse_scalar_package(message)
