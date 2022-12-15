# Drift Protocol

The Drift Protocol is a set of libraries that
use [Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview) (Protobuf) to encode messages in
the [PANDA|Drift infrastructure](https://driftpythonclient.readthedocs.io/en/latest/docs/panda_drift/).. The libraries
provide pre-generated Protobuf messages so that users do not have to install the protobuf compiler and generate them
themselves.

## Implementations

* [For C++](cpp/README.md)
* [For Python](python/README.md)

## Example

The Drift Protocol can be used to create microservice applications. An example of such an application is shown in the
accompanying diagram:

![Drift Protocol Example](docs/img/example.drawio.svg)

Trigger Service publishes a trigger as a [Drift Package](docs/api/common.md#driftpackage) with ID = 1630062869443 and
a [Trigger Interval Message](docs/api/triggering.md#intervaltriggermessage), which contains a time interval [t0, t1], to
the  `trigger` MQTT topic.

Timeswipe Service subscribes on the `trigger` topic and receives the trigger package. Then it retrieves data of 48000
samples per second from a vibration sensor for the interval [t0, t1] by using Time Swipe Device, compresses, serializes
the data and sends it to MQTT topic `drift/sensor` as a [Drift Package](docs/api/common.md#driftpackage) with
a [Data Payload](docs/api/common.md#datapayload) inside. It contains a
serialized [Wavelet Buffer](https://github.com/panda-official/WaveletBuffer) in the `data` field. The ID of the packages
is the same ID=1630062869443, so we see that the trigger and the data are connected.

The [Drift Core](https://driftpythonclient.readthedocs.io/en/latest/docs/panda_drift/) services subscribe to all MQTT
topics which have `drift/` prefix, parse [Drift Packages](docs/api/common.md#driftpackage) and store them in the metric
and blob storages. After that, you can use [Drift Python Client](https://github.com/panda-official/DriftPythonClient) to
request data from the storage.

## Why Protobuf?

We use Protobuf to encode messages in Drift Protocol because it is a very efficient and flexible serialization format,
especially for binary data. It is also very easy to use and has a lot of implementations for different programming

## Related Projects

* [WaveletBuffer](https://github.com/panda-official/WaveletBuffer) - A universal C++ compression library based on
  wavelet transformation
* [Drift Python Client](https://github.com/panda-official/DriftPythonClient) - Python Client to access data of
  PANDA|Drift
