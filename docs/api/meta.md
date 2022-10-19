# Meta Protocol

Package: **drift.proto.meta**

Additionally to data, Drift Package can contain a message with meta information, which describers the data
in [DataPayload](/docs/api/common) . For example, if we send a [DataPayload](/docs/api/common) with time-series inside,
we can send information about the full size of the signal, time period etc.

The meta information describes the following data types:

* Time Series
* Images
* Scala Values
* Text
* Aligned Data

## MetaInfo

Top-level descriptor which has type of data in Drift Package and a type specific descriptor.

| Name                | Type                                                                     | Description                                                                      |
|---------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| type                | DataType                                                                 | Enumeration (TIME_SERIES=0, IMAGE=1, SCALAR_VALUES=2, TEXT=3, ALIGNED_PACKAGE=4) |
| One of filed below: | [oneof](https://developers.google.com/protocol-buffers/docs/proto#oneof) |
| timeseries_info     | [TimeSeriesInfo](/docs/api/meta#timeseriesinfo)                          |                                                                                  |
| image_info          | [ImageInfo](/docs/api/meta#imageinfo)                                    |                                                                                  |
| scalar_info         | [ScalarValuesInfo](/docs/api/meta#scalarvaluesinfo)                      |                                                                                  |
| text_info           | [TextInfo](/docs/api/meta#textinfo)                                      |                                                                                  |
| alignment_info      | [AlignmentInfo](/docs/api/meta#alignmentinfo)                            |                                                                                  |

## TimeSeriesInfo

TimeSeriesInfo describes time series data inside DriftPackage, which is sent as [DataPayload](/docs/api/common) with
a serialized [WaveletBuffer](https://github.com/panda-official/WaveletBuffer).

| Name            | Type      | Description                                         |
|-----------------|-----------|-----------------------------------------------------|
| start_timestamp | Timestamp | Timestamp of the first point in the series          |
| stop_timestamp  | Timestamp | Timestamp of the last point in the series           |
| size            | uint64    | Full size of the signal (all DataPayloads together) |
| first           | float     | First value in series                               |
| last            | float     | Last value in series                                |
| min             | float     | Min value in series                                 |
| max             | float     | Max value in series                                 |
| mean            | float     | Mean value                                          |

## ImageInfo

TimeSeriesInfo describes a serialized image inside DriftPackage. It may content
either [WaveletBuffer](https://github.com/panda-official/WaveletBuffer) (WB) or JPEG string.

| Name           | Type   | Description                                       |
|----------------|--------|---------------------------------------------------|
| type           | Type   | Enumeration (WB=0, JPEG=1)                        |
| width          | uint64 | Width of the image                                |
| height         | uint64 | Height of the image                               |
| channel_layout | string | “RGB”, “HSLGGG” - one HSL image and 3 gray images |

## ScalarValuesInfo

ScalarValuesInfo describes scalar values inside DriftPackage which is sent
as a [WaveletBuffer](https://github.com/panda-official/WaveletBuffer) without any decomposition.
This type of data is used when we have some samples as intentioned parameters from a data source.

| Name          | Type        | Description                                        |
|---------------|-------------|----------------------------------------------------|
| variables     | ValueInfo[] | Description for each scalar value in WaveletBuffer |
| **ValueInfo** |             |                                                    |
| name          | string      | Name of variable                                   |

## TextInfo

ScalarValuesInfo describes a text data like JSON, XML etc.

| Name      | Type   | Description                                                  |
|-----------|--------|--------------------------------------------------------------|
| mime_type | string | Format of data, e.g. “text/plain”, “text/json;charset=UTF-8” |

## AlignmentInfo

AlignmentInfo describes a special case, when we send a few Drift packages with the same ID but from
different MQTT topics.

| Name            | Type          | Description                                               |
|-----------------|---------------|-----------------------------------------------------------|
| packages        | PackageInfo[] | Description for each aligned package value in DataPayload |
| **PackageInfo** |               |                                                           |
| topic           | string        | Name of source topic                                      |