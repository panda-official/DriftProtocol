#include <drift_protocol/common/data_payload.pb.h>
#include <drift_protocol/common/drift_package.pb.h>
#include <google/protobuf/util/time_util.h>
#include <drift_bytes/bytes.h>

using drift::proto::common::DataPayload;
using drift::proto::common::DriftPackage;
using drift::proto::common::StatusCode;
using drift::proto::meta::MetaInfo;
using drift::proto::meta::TypedDataInfo;

using drift_bytes::Variant;
using drift_bytes::InputBuffer;
using drift_bytes::OutputBuffer;

using google::protobuf::util::TimeUtil;
using google::protobuf::Any;

int main() {
    const auto pb_time = TimeUtil::GetCurrentTime();
    std::string message;

    const auto kData = {Variant(true), Variant(1), Variant(1.0), Variant("Hello")};
    const std::vector<std::string> kNames = {"bool", "int", "float", "string"};

    {
        // Create a package and serialize it
        DriftPackage original;
        original.set_id(TimeUtil::TimestampToMilliseconds(pb_time)); // UNIX timestamp in ms
        original.set_status(StatusCode::GOOD);
        original.mutable_source_timestamp()->CopyFrom(pb_time);
        original.mutable_publish_timestamp()->CopyFrom(pb_time);

        // Fill meta data
        TypedDataInfo info;
        for (const auto &name: kNames) {
            auto var = info.add_items();
            var->set_name(name);
            var->set_status(StatusCode::GOOD);
        }

        MetaInfo meta;
        meta.set_type(MetaInfo::TYPED_DATA);
        meta.mutable_typed_data_info()->CopyFrom(info);

        original.mutable_meta()->CopyFrom(meta);

        // Put data in buffer without decomposition and compression
        OutputBuffer buffer;
        for (const auto &data: kData) {
            buffer.push_back(data);
        }

        // Prepare payload
        DataPayload payload;
        payload.set_data(buffer.str());
        original.add_data()->PackFrom(payload);

        // Serialize package to message
        original.SerializePartialToString(&message);
    }

    // Parse the package
    DriftPackage new_package;
    new_package.ParseFromString(message);
    std::cout << "Package with ID=" << new_package.id() << " type="
              << MetaInfo::DataType_Name(new_package.meta().type()) << std::endl;

    DataPayload payload;
    new_package.data(0).UnpackTo(&payload);
    auto data = payload.data();
    auto buffer = InputBuffer(std::move(data));

    // Print data
    for (const auto &var: new_package.meta().typed_data_info().items()) {
        std::cout << var.name() << ": " << buffer.pop() << std::endl;
    }
}
