from drift_protocol.common import DriftPackage, DataPayload, StatusCode

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.any_pb2 import Any

if __name__ == "__main__":
    pb_time = Timestamp()
    pb_time.GetCurrentTime()

    # Create a package and serialize it
    original = DriftPackage()
    original.id = pb_time.ToMilliseconds()
    original.source_timestamp.CopyFrom(pb_time)
    original.publish_timestamp.CopyFrom(pb_time)
    original.status = StatusCode.GOOD

    # Prepare payload
    payload = DataPayload()
    payload.data = b"some data to send"

    msg = Any()
    msg.Pack(payload)
    original.data.append(msg)

    # Serialize package to message
    message = original.SerializeToString()

    # Parse the package
    new_pacakge = DriftPackage()
    new_pacakge.ParseFromString(message)
    print(f"Package ID={new_pacakge.id}")

    payload = DataPayload()
    new_pacakge.data[0].Unpack(payload)
    print(f"Data: {payload.data}")
