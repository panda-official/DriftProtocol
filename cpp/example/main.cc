#include <drift_protocol/common/data_payload.pb.h>
#include <drift_protocol/common/drift_package.pb.h>

using drift::proto::common::DataPayload;
using drift::proto::common::DriftPackage;
using drift::proto::common::StatusCode;


int main() {
    // Create a package and serialize it
    DriftPackage original;

    original.set_id(0000001); // usually we use UNIX timestamp in ms
    original.set_status(StatusCode::GOOD);

    DataPayload payload;
    payload.set_data("some data to send");

    original.add_data()->PackFrom(payload);

    std::string blob = original.SerializeAsString();

    // Parse the package
    DriftPackage new_package;
    new_package.ParseFromString(blob);
}
