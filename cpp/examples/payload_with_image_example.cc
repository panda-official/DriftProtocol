#include <drift_protocol/common/data_payload.pb.h>
#include <drift_protocol/common/drift_package.pb.h>
#include <google/protobuf/util/time_util.h>

#include <wavelet_buffer/wavelet_buffer.h>
#include <wavelet_buffer/img/wavelet_image.h>
#include <wavelet_buffer/img/jpeg_codecs.h>
#include <wavelet_buffer/denoise_algorithms.h>


using drift::proto::common::DataPayload;
using drift::proto::common::DriftPackage;
using drift::proto::common::StatusCode;
using drift::proto::meta::MetaInfo;
using drift::proto::meta::ImageInfo;

using drift::WaveletBuffer;
using drift::WaveletParameters;
using drift::WaveletTypes;
using drift::img::WaveletImage;
using Denoiser = drift::SimpleDenoiseAlgorithm<float>;
using drift::img::RgbJpegCodec;

using google::protobuf::util::TimeUtil;
using google::protobuf::Any;

int main() {
    const auto pb_time = TimeUtil::GetCurrentTime();
    std::string message;

    // Load and decompose image with wavelet image
    const auto kWidth = 800;
    const auto kHeight = 500;
    WaveletImage img(WaveletParameters{
            .signal_shape = {kWidth, kHeight},
            .signal_number = 3,
            .decomposition_steps = 3,
            .wavelet_type = WaveletTypes::kDB3,
    });

    // Load JPG image, decode, decompose with wavelet transformation and denoise
    if (auto code = img.ImportFromFile(IMAGE_PATH, Denoiser(0.9), RgbJpegCodec())) {
        std::cerr << "Failed to import image " << code;
        return -1;
    }

    {
        // Create a package and serialize it
        DriftPackage original;
        original.set_id(TimeUtil::TimestampToMilliseconds(pb_time)); // UNIX timestamp in ms
        original.set_status(StatusCode::GOOD);
        original.mutable_source_timestamp()->CopyFrom(pb_time);
        original.mutable_publish_timestamp()->CopyFrom(pb_time);

        // Fill meta data
        ImageInfo image_info;
        image_info.set_type(ImageInfo::WB); // this is image decode with WaveletBuffer
        image_info.set_width(kWidth);
        image_info.set_height(kHeight);
        image_info.set_channel_layout("RGB");

        MetaInfo meta;
        meta.set_type(MetaInfo::IMAGE);
        meta.mutable_image_info()->CopyFrom(image_info);

        original.mutable_meta()->CopyFrom(meta);

        // Prepare payload with the image
        std::string compressed_image;
        if (!img.buffer().Serialize(&compressed_image, 16)) {
            std::cerr << "Failed to compress image image";
            return -1;
        }

        DataPayload payload;
        payload.set_data(compressed_image);
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
