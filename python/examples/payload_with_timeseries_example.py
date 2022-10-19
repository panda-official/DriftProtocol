from pathlib import Path
import numpy as np

from drift_protocol.common import DriftPackage, DataPayload, StatusCode
from drift_protocol.meta import MetaInfo, TimeSeriesInfo
from wavelet_buffer import denoise, WaveletType, WaveletBuffer

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.any_pb2 import Any

IMG_PATH = Path(__file__).parent / "pandas.jpg"

if __name__ == "__main__":
    pb_time = Timestamp()
    pb_time.GetCurrentTime()

    SIGNAL = np.array(
        [0.1, 0.2, 0.5, 0.1, 0.2, 0.1, 0.6, 0.1, 0.1, 0.2], dtype=np.float32
    )

    # Create a package and serialize it
    original = DriftPackage()
    original.id = pb_time.ToMilliseconds()
    original.source_timestamp.CopyFrom(pb_time)
    original.publish_timestamp.CopyFrom(pb_time)
    original.status = StatusCode.GOOD

    # Fill meta data
    info = TimeSeriesInfo()
    info.start_timestamp.FromMilliseconds(pb_time.ToMilliseconds() - 1_000_000)
    info.stop_timestamp.CopyFrom(pb_time)
    info.size = len(SIGNAL)
    info.first = SIGNAL[0]
    info.last = SIGNAL[-1]
    info.min = np.min(SIGNAL)
    info.max = np.max(SIGNAL)
    info.mean = np.mean(SIGNAL)

    meta = MetaInfo
    meta.type = MetaInfo.TIME_SERIES
    meta.image_info = info

    # Decompose and compress signal
    buffer = WaveletBuffer(
        signal_shape=[len(SIGNAL)],
        signal_number=1,
        decomposition_steps=2,
        wavelet_type=WaveletType.DB1,
    )
    buffer.decompose(SIGNAL, denoise.Threshold(0, 0.1))

    # Prepare payload
    payload = DataPayload()
    payload.data = buffer.serialize(compression_level=16)

    msg = Any()
    msg.Pack(payload)
    original.data.append(msg)

    # Serialize package to message
    message = original.SerializeToString()

    # Parse the package
    new_pacakge = DriftPackage()
    new_pacakge.ParseFromString(message)
    print(
        f"Package ID={new_pacakge.id} type={MetaInfo.DataType.Name(new_pacakge.meta.type)}"
    )

    payload = DataPayload()
    new_pacakge.data[0].Unpack(payload)

    buffer = WaveletBuffer.parse(payload.data)
    print(f"WaveletBuffer {buffer.compose()}")
