# Meta Protocol

Package: **drift.proto.meta**

Additionally to data, Drift Package can contain a message with meta information, which describers the data
in [DataPayload](common.md) . For example, if we send a [DataPayload](common.md) with time-series inside,
we can send information about the full size of the signal, time period etc.

The meta information describes the following data types:

* Time Series
* Images
* Scala Values
* Text
* Aligned Data
* Typed Data

## MetaInfo

Top-level descriptor which has type of data in Drift Package and a type specific descriptor.

| Name                | Type                                                                     | Description                                                                      |
|---------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| type                | DataType                                                                 | Enumeration (TIME_SERIES=0, IMAGE=1, SCALAR_VALUES=2, TEXT=3, ALIGNED_PACKAGE=4) |
| One of filed below: | [oneof](https://developers.google.com/protocol-buffers/docs/proto#oneof) |
| timeseries_info     | [TimeSeriesInfo](meta.md#timeseriesinfo)                                 |                                                                                  |
| image_info          | [ImageInfo](meta.md#imageinfo)                                           |                                                                                  |
| scalar_info         | [ScalarValuesInfo](meta.md#scalarvaluesinfo)                             |                                                                                  |
| text_info           | [TextInfo](meta.md#textinfo)                                             |                                                                                  |
| alignment_info      | [AlignmentInfo](meta.md#alignmentinfo)                                   |                                                                                  |
| typed_data_info     | [TypedDataInfo](meta.md#typeddatainfo)                                   |                                                                                  |
| wavelet_buffer_info | [WaveletBufferInfo](meta.md#waveletbufferinfo)                           | Information about wavelet transformation and compression if used                 |

## TimeSeriesInfo

TimeSeriesInfo describes time series data inside DriftPackage, which is sent as [DataPayload](common.md) with
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

DEPRECATED: use [TypedDataInfo](meta.md#typeddatainfo) instead.

| Name          | Type                               | Description                                        |
|---------------|------------------------------------|----------------------------------------------------|
| variables     | ValueInfo[]                        | Description for each scalar value in WaveletBuffer |
| **ValueInfo** |                                    |                                                    |
| name          | string                             | Name of variable                                   |
| status        | [StatusCode](common.md#statuscode) | Status of variable                                 |

## TextInfo

ScalarValuesInfo describes a text data like JSON, XML etc.

| Name      | Type   | Description                                                  |
|-----------|--------|--------------------------------------------------------------|
| mime_type | string | Format of data, e.g. “text/plain”, “text/json;charset=UTF-8” |

## AlignmentInfo

AlignmentInfo describes a special case, when we send a few Drift packages with the same ID but from
different MQTT topics.

| Name            | Type                         | Description                                               |
|-----------------|------------------------------|-----------------------------------------------------------|
| packages        | PackageInfo[]                | Description for each aligned package value in DataPayload |
| **PackageInfo** |                              |                                                           |
| topic           | string                       | Name of source topic                                      |
| meta            | [MetaInfo](meta.md#metainfo) | Meta information for the package                          |

## TypedDataInfo

TypedDataInfo describes how to parse a binary data inside [DataPayload](common.md) when the data has values of different
types (not only float).

| Name     | Type     | Description                              |
|----------|----------|------------------------------------------|
| items    | Item[]   | Description for each item in DataPayload |
| **Item** |          |                                          |
| name     | string   | Name of item                             |
| type     | Type     | Type of item                             |
| status   | Status   | Status of item                           |
| shape    | uint64[] | Shape of item                            |

Supported types:

| Name    | ID | Description             |
|---------|----|-------------------------|
| BOOL    | 0  | Boolean                 |
| INT8    | 1  | 8-bit signed integer    |
| UINT8   | 2  | 8-bit unsigned integer  |
| INT16   | 3  | 16-bit signed integer   |
| UINT16  | 4  | 16-bit unsigned integer |
| INT32   | 5  | 32-bit signed integer   |
| UINT32  | 6  | 32-bit unsigned integer |
| INT64   | 7  | 64-bit signed integer   |
| UINT64  | 8  | 64-bit unsigned integer |
| FLOAT32 | 9  | 32-bit float            |
| FLOAT64 | 10 | 64-bit float            |
| STRING  | 11 | UTF-8 String            |


## WaveletBufferInfo

WaveletBufferInfo describes a wavelet transformation and compression parameters if they were applied to the data.

| Name                | Type                                             | Description                                                                                            |
|---------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| abi_version         | uint32                                           | ABI version of the WaveletBuffer library                                                               |
| wavelet_type        | uint32                                           | Wavelet type 0-no wavelet transformation, 1-DB1, 2-DB2 etc.                                            |
| decomposition_steps | uint32                                           | Number of decomposition steps applied to the data                                                      |
| float_compression   | uint32                                           | Float compression level applied to the data, 0 - no compression, 1-float is 2bit, 2-float is 3bit etc. |
| no_denoising        | [NoDenoising](meta.md#nodenoising)               | If initialized, no denoising was applied to the data.                                                  |
| threshold_denoising | [ThresholdDenoising](meta.md#thresholddenoising) | If initialized, threshold denoising was applied to the data.                                           |
| partial_denoising   | [PartialDenoising](meta.md#partialdenoising)     | If initialized, partial denoising was applied to the data.                                             |

## NoDenoising

No denoising was applied to the data.

| Name | Type | Description |
|------|------|-------------|

## ThresholdDenoising

A denoising method that uses a threshold to remove small coefficients. The threshold is calculated as a linear function
a*x+b,
where x is the step of decomposition.

| Name | Type  | Description |
|------|-------|-------------|
| a    | float | float       |  
| b    | float | float       |

## PartialDenoising

A denoising method that removes a part of coefficients

| Name    | Type  | Description                                          |
|---------|-------|------------------------------------------------------|
| partial | float | part of coefficients to remove 1.0 - all, 0.0 - none |