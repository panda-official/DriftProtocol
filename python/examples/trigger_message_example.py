from google.protobuf.any_pb2 import Any
from google.protobuf.timestamp_pb2 import Timestamp

from drift_protocol.common import DriftPackage, StatusCode
from drift_protocol.trigger_service import IntervalTriggerMessage

if __name__ == "__main__":
    pb_time = Timestamp()
    pb_time.GetCurrentTime()

    # Create a package and serialize it
    original = DriftPackage()
    original.id = pb_time.ToMilliseconds()
    original.source_timestamp.CopyFrom(pb_time)
    original.publish_timestamp.CopyFrom(pb_time)
    original.status = StatusCode.GOOD

    # Trigger message for 1 second interval
    trigger = IntervalTriggerMessage()
    trigger.start_timestamp.FromMilliseconds(pb_time.ToMilliseconds() - 1_000_000)
    trigger.stop_timestamp.CopyFrom(pb_time)

    msg = Any()
    msg.Pack(trigger)
    original.data.append(msg)

    # Serialize package to message
    message = original.SerializeToString()

    # Parse the package
    new_pacakge = DriftPackage()
    new_pacakge.ParseFromString(message)
    print(f"Package ID={new_pacakge.id}")

    trigger = IntervalTriggerMessage()
    new_pacakge.data[0].Unpack(trigger)
    print(f"Trigger interval from from {trigger.start_timestamp.ToDatetime()} to {trigger.stop_timestamp.ToDatetime()}")
