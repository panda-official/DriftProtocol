#include <drift_protocol/common/data_payload.pb.h>
#include <drift_protocol/common/drift_package.pb.h>
#include <google/protobuf/util/time_util.h>
#include <wavelet_buffer/wavelet_buffer.h>
#include <wavelet_buffer/denoise_algorithms.h>

using drift::proto::common::DataPayload;
using drift::proto::common::DriftPackage;
using drift::proto::common::StatusCode;
using drift::proto::meta::MetaInfo;
using drift::proto::meta::ScalarValuesInfo;

using drift::WaveletBuffer;
using drift::WaveletParameters;
using drift::WaveletTypes;
using drift::Signal1D;
using NoDenoise = drift::NullDenoiseAlgorithm<float>;

using google::protobuf::util::TimeUtil;
using google::protobuf::Any;

int main() {
    const auto pb_time = TimeUtil::GetCurrentTime();
    std::string message;

    const Signal1D kData = {0, 10., 0.3, 1};
    const std::vector<std::string> kNames = {"x0", "x1", "x2", "x3"};

    {
        // Create a package and serialize it
        DriftPackage original;
        original.set_id(TimeUtil::TimestampToMilliseconds(pb_time)); // UNIX timestamp in ms
        original.set_status(StatusCode::GOOD);
        original.mutable_source_timestamp()->CopyFrom(pb_time);
        original.mutable_publish_timestamp()->CopyFrom(pb_time);

        // Fill meta data
        ScalarValuesInfo info;
        for (const auto &name: kNames) {
            info.add_variables()->set_name(name);
        }

        MetaInfo meta;
        meta.set_type(MetaInfo::SCALAR_VALUES);
        meta.mutable_scalar_info()->CopyFrom(info);

        original.mutable_meta()->CopyFrom(meta);

        // Decompose and compress signal
        WaveletBuffer buffer(WaveletParameters{
                .signal_shape =  {kData.size()},
                .signal_number = 1,
                .decomposition_steps = 0,
                .wavelet_type = WaveletTypes::kNone, // No composition, wavelet buffer is a vector now
        });

        if (!buffer.Decompose(kData, NoDenoise())) {
            std::cerr << "Failed decompose the signal";
            return -1;
        }

        std::string data;
        if (!buffer.Serialize(&data, 16)) {
            std::cerr << "Failed decompose the signal";
            return -1;
        }

        // Prepare payload
        DataPayload payload;
        payload.set_data(data);
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
    auto buffer = WaveletBuffer::Parse(payload.data());
    std::cout << "Wavelet Buffer: " << buffer->parameters() << std::endl;
}
