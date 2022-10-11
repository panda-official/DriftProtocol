# Common Protocol

Package: **drift.proto.common**

## DriftPackage

A basic package for communication between services in PANDA|Drift infrastructure. All messages in Drift are wrapped into
it, so that the PANDA|Drift infrastructure can handle and store them.

| Name              | Type                                | Description                                                                       |
|-------------------|-------------------------------------|-----------------------------------------------------------------------------------|
| id                | int64                               | Package ID (Unix time in milliseconds)                                            |
| source_timestamp  | Timestamp                           | Timestamp when a service has received  an input package                           |
| publish_timestamp | Timestamp                           | Timestamp when a service has done its job and sends an output package             |
| status            | [StatusCode](#StatusCode)           | Status of the package. .                                                          |
| data              | Any[]                               | An array of any protobuf messages, it may be Drift Payload’s, Trigger Message etc |
| meta              | [MetaInfo](/docs/api/meta#MetaInfo) | See [MetProtocol](/docs/api/meta)                                                 |

## DataPayload

DataPayload represents serialized data which a server sends via MQTT. It is usually data denoised and compressed by
using [WaveletBuffer](https://github.com/panda-official/WaveletBuffer).

| Name  | Type   | Description                                                                                                                                                          |
|-------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| shape | uint32 | Shape of real data. DEPRECATED  We use [MetProtocol](/docs/api/meta) to describe shape of data                                                                       |
| data  | byte[] | ialized binary data. It maybe JPEG picture, Wavelet Buffer, JSON string etc.   A service which subscribes on this data should know the format and how to process it. |

## StatusCode

Status of the package. Ok (0) means the package is valid and you can trust the data. Other code explains the reason why
the package is not valid. You should not use its data, however the service should publish an empty packages with the bad
status any way.

| Name                    | Code         | Description                                                                               |
|-------------------------|--------------|-------------------------------------------------------------------------------------------|
| GOOD                    | 0x0000 (0)   | No errors                                                                                 |
|                         |              |                                                                                           |
| UNCERTAIN               | 0x0100 (256) | Common uncertain status. For example, data isn't initialized yet or something is disabled |
| UNCERTAIN_SERVICE_BUSY  | 0x0101 (257) | No errors, but service isn't ready to handle response                                     |
|                         |              |                                                                                           |
| BAD                     | 0x0200 (512) | Common bad status can be used as a flag                                                   |
| BAD_MALFORMED_REQUEST   | 0x0201 (513) | Format of  request is wrong                                                               |
| BAD_MALFORMED_RESPONSE  | 0x0202 (514) | Format of response is wrong                                                               |
| BAD_INVALID_ARGUMENT    | 0x0203 (515) | Value of number or arguments in a request is wrong                                        |
| BAD_INTERNAL_ERROR      | 0x0204 (516) | Input is ok, but a service has internal error and failed to handle it                     |
| BAD_COMMUNICATION_ERROR | 0x0205 (517) | A service failed to reach data from input                                                 |
| BAD_SOURCE_STATE        | 0x0206 (518) | Data source is available but can't provide data                                           |
| BAD_SOURCE_DATA_QUALITY | 0x0207 (519) | Data source provides data but the quality is bad                                          |
| BAD_DATA_READ_TIMEOUT   | 0x0208 (520) | We failed to get data from the source for the given timeout                               |
