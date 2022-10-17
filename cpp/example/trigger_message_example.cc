#include <drift_protocol/common/drift_package.pb.h>
#include <drift_protocol/trigger_service/interval_trigger_message.pb.h>
#include <google/protobuf/util/time_util.h>

using drift::proto::trigger_service::IntervalTriggerMessage;
using drift::proto::common::DriftPackage;
using drift::proto::common::StatusCode;

using google::protobuf::util::TimeUtil;
using google::protobuf::Any;

int main() {
    const auto pb_time = TimeUtil::GetCurrentTime();
    std::string message;

    {
        // Create a package and serialize it
        DriftPackage original;
        original.set_id(TimeUtil::TimestampToMilliseconds(pb_time)); // UNIX timestamp in ms
        original.set_status(StatusCode::GOOD);
        original.mutable_source_timestamp()->CopyFrom(pb_time);
        original.mutable_publish_timestamp()->CopyFrom(pb_time);

        // Trigger message for 1 second interval
        IntervalTriggerMessage trigger;
        trigger.mutable_start_timestamp()->CopyFrom(pb_time - TimeUtil::SecondsToDuration(1));
        trigger.mutable_stop_timestamp()->CopyFrom(pb_time);

        // Serialize package to message
        original.add_data()->PackFrom(trigger);
        original.SerializePartialToString(&message);
    }

    // Parse the package with the trigger
    DriftPackage new_package;
    new_package.ParseFromString(message);
    std::cout << "Package ID=" << new_package.id() << std::endl;

    IntervalTriggerMessage trigger;
    new_package.data(0).UnpackTo(&trigger);
    std::cout << "Trigger interval from " << TimeUtil::ToString(trigger.start_timestamp()) << " to "
              << TimeUtil::ToString(trigger.stop_timestamp()) << std::endl;
}
