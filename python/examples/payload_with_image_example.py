from pathlib import Path

from drift_protocol.common import DriftPackage, DataPayload, StatusCode
from drift_protocol.meta import MetaInfo, ImageInfo
from wavelet_buffer import denoise, WaveletType, WaveletBuffer
from wavelet_buffer.img import WaveletImage, RgbJpeg

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.any_pb2 import Any

IMG_PATH = Path(__file__).parent / "pandas.jpg"

if __name__ == "__main__":
    pb_time = Timestamp()
    pb_time.GetCurrentTime()

    # Load and decompose image with wavelet image
    WIDTH = 800
    HEIGHT = 500
    img = WaveletImage(signal_shape=[WIDTH, HEIGHT], signal_number=3, decomposition_steps=3,
                       wavelet_type=WaveletType.DB3)

    img.import_from_file(str(IMG_PATH.resolve()), denoiser=denoise.Simple(0.9), codec=RgbJpeg())

    # Create a package and serialize it
    original = DriftPackage()
    original.id = pb_time.ToMilliseconds()
    original.source_timestamp.CopyFrom(pb_time)
    original.publish_timestamp.CopyFrom(pb_time)
    original.status = StatusCode.GOOD

    # Fill meta data
    image_info = ImageInfo()
    image_info.type = ImageInfo.ImageType.WB
    image_info.width = WIDTH
    image_info.height = HEIGHT
    image_info.channel_layout = "RGB"

    meta = MetaInfo
    meta.type = MetaInfo.IMAGE
    meta.image_info  = image_info

    # Prepare payload
    payload = DataPayload()
    payload.data = img.buffer.serialize(compression_level=16)

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
    print(f"WaveletBuffer {buffer}")
