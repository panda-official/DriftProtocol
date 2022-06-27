# Drift Protocol for Python

A Python Protobuf library to encode message in Drift infrastructure.
It provides pre-generated Protobuf messages so that you don't need to install protobuf compiler and generate them yourself.


## Features

* Pure Python
* No Protobuf Compiler and generation needed

## Install

You can install the library as a PIP package

```
pip install -U drift-protocol
```

## Usage example


Parsing a Drift package:

```python

from drift_protocol.common import DriftPackage, DataPayload, StatusCode

some_blob_received_from_drift = "...."

package: DriftPackage = DriftPackage()
package.ParseFromString(some_blob_received_from_drift)

if package.statuse != StatusCode.GOOD:
    exit(-1)

for any_data in package.data:
    if any_data.Is(DataPayload.DESCRIPTOR):
        payload = DataPayload()
        any_data.Unpack(payload)

        data: bytes = payload.data
```


## Related Projects

* [WaveletBuffer](https://github.com/panda-official/WaveletBuffer) - A universal C++ compression library based on wavelet transformation
