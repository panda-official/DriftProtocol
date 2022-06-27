# Drift Protocol

Protobuf Libraries to encode message in Drift infrastructure.
The libraries provide pre-generated Protobuf messages so that you don't need to install protobuf compiler and
generate them yourself.


## C++ Package

### С++ (Conan)

Registry PANDA's Conan repo

```shell
conan remote add panda https://conan.panda.technology/artifactory/api/conan/drift
```

Add to conanfile.txt

```shell
drift_protocol/0.x.y@drift/stable
```

###Python

* generate access token with API permissions
* configure your pip to use private `PYPI`,
```bash
pip config set global.extra-index-url https://__token__:<YOUR_TOKEN_HERE>@gitlab.panda.technology/api/v4/projects/231/packages/pypi/simple/
```
* install package
```bash
pip install drift-proto
```

Install from the source files (requires proto compiler)
```bash
pip install git+ssh://git@gitlab.panda.technology/drift/sdk/drift_proto.git
```

**Usage:**
```python
from drift_proto.common import DriftPackage


package = DriftPackage()
```

### NodeJS / React.js

Create file .npmrc in NPM your project and add there:
```
registry=https://npm.panda.technology/
```

Then install the pre-compiled Protobuf messages
```shell
npm -i  @panda/drift_proto
```

**Usage**:

```javascript
import {common} from '@panda/drift_proto';

const pack  = new common.DriftPackage();
```
