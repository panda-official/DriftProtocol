#include <drift_protocol/common/data_payload.pb.h>
#include <drift_protocol/common/drift_package.pb.h>
#include <google/protobuf/util/time_util.h>

using drift::proto::common::DataPayload;
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

        // Prepare payload
        DataPayload payload;
        payload.set_data("some data to send");
        original.add_data()->PackFrom(payload);

        // Serialize package to message
        original.SerializePartialToString(&message);
    }

    // Parse the package
    DriftPackage new_package;
    new_package.ParseFromString(message);
    std::cout << "Package ID=" << new_package.id() << std::endl;

    DataPayload payload;
    new_package.data(0).UnpackTo(&payload);
    std::cout << "Data: " << payload.data() << std::endl;
}
