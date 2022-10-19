from pathlib import Path
import numpy as np

from drift_protocol.common import DriftPackage, DataPayload, StatusCode
from drift_protocol.meta import MetaInfo, ScalarValuesInfo
from wavelet_buffer import denoise, WaveletType, WaveletBuffer

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.any_pb2 import Any

IMG_PATH = Path(__file__).parent / "pandas.jpg"

if __name__ == "__main__":
    pb_time = Timestamp()
    pb_time.GetCurrentTime()

    DATA = np.array([0, 10., 0.3, 1], dtype=np.float32)
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
        info.variables.append(var)

    meta = MetaInfo
    meta.type = MetaInfo.SCALAR_VALUES
    meta.image_info = info

    # Decompose and compress signal
    buffer = WaveletBuffer(signal_shape=[len(DATA)], signal_number=1, decomposition_steps=0,
                           wavelet_type=WaveletType.NONE)
    buffer.decompose(DATA, denoise.Null())

    # Prepare payload
    payload = DataPayload()
    payload.data = buffer.serialize(compression_level=0)

    msg = Any()
    msg.Pack(payload)
    original.data.append(msg)

    # Serialize package to message
    message = original.SerializeToString()

    # Parse the package
    new_pacakge = DriftPackage()
    new_pacakge.ParseFromString(message)
    print(f"Package ID={new_pacakge.id} type={MetaInfo.DataType.Name(new_pacakge.meta.type)}")

    payload = DataPayload()
    new_pacakge.data[0].Unpack(payload)

    buffer = WaveletBuffer.parse(payload.data)
    print(f"WaveletBuffer {buffer.compose()}")
