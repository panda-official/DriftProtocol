# Drift Protocol for C++

A C++ Protobuf library to encode message in Drift infrastructure.
It provides pre-generated Protobuf messages so that you don't need to install protobuf compiler and generate them
yourself.

## Features

* Protocol Buffer ==3.12.4, <=3.19
* No Protobuf Compiler and generation needed
* Conan distribution

## Integration

### Conan

The easiest way to integrate the library into your code, is to use it with conan.
Install the tool and add our repository.

```
pip install -U conan
conan remote add panda https://conan.panda.technology/artifactory/api/conan/drift
```

Then add into your `conanfile.txt` or `conanfile.py`:

```
drift_protocol/x.y.z@drift/stable
```

## Usage example

Handling a package:

```cpp
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
```

## Related Projects

* [WaveletBuffer](https://github.com/panda-official/WaveletBuffer) - A universal C++ compression library based on
  wavelet transformation
* [Drift Python Client](https://github.com/panda-official/DriftPythonClient) - Python Client to access data of
  PANDA|Drift