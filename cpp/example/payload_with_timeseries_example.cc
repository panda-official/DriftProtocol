#include <drift_protocol/common/data_payload.pb.h>
#include <drift_protocol/common/drift_package.pb.h>
#include <google/protobuf/util/time_util.h>
#include <wavelet_buffer/wavelet_buffer.h>
#include <wavelet_buffer/denoise_algorithms.h>

using drift::proto::common::DataPayload;
using drift::proto::common::DriftPackage;
using drift::proto::common::StatusCode;
using drift::proto::meta::MetaInfo;
using drift::proto::meta::TimeSeriesInfo;

using drift::WaveletBuffer;
using drift::WaveletParameters;
using drift::WaveletTypes;
using drift::Signal1D;
using NoDenoise = drift::ThresholdAbsDenoiseAlgorithm<float>;

using google::protobuf::util::TimeUtil;
using google::protobuf::Any;

int main() {
    const auto pb_time = TimeUtil::GetCurrentTime();
    std::string message;

    const Signal1D kTimeSeries{0.1, 0.2, 0.5, 0.1, 0.2, 0.1, 0.6, 0.1, 0.1, 0.2};
    {
        // Create a package and serialize it
        DriftPackage original;
        original.set_id(TimeUtil::TimestampToMilliseconds(pb_time)); // UNIX timestamp in ms
        original.set_status(StatusCode::GOOD);
        original.mutable_source_timestamp()->CopyFrom(pb_time);
        original.mutable_publish_timestamp()->CopyFrom(pb_time);

        // Fill meta data
        TimeSeriesInfo info;
        info.mutable_start_timestamp()->CopyFrom(pb_time - TimeUtil::SecondsToDuration(1));
        info.mutable_stop_timestamp()->CopyFrom(pb_time);
        info.set_size(kTimeSeries.size());
        info.set_first(kTimeSeries[0]);
        info.set_last(kTimeSeries[kTimeSeries.size() - 1]);
        info.set_min(blaze::min(kTimeSeries));
        info.set_max(blaze::max(kTimeSeries));
        info.set_min(blaze::min(kTimeSeries));

        MetaInfo meta;
        meta.set_type(MetaInfo::TIME_SERIES);
        meta.mutable_time_series_info()->CopyFrom(info);

        original.mutable_meta()->CopyFrom(meta);

        // Decompose and compress signal
        WaveletBuffer buffer(WaveletParameters{
                .signal_shape =  {kTimeSeries.size()},
                .signal_number = 1,
                .decomposition_steps = 2,
                .wavelet_type = WaveletTypes::kDB1, // Haar
        });

        if (!buffer.Decompose(kTimeSeries, NoDenoise(0, 0.1))) {
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
