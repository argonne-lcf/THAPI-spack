# THAPI-spack

This repository provides a [Spack](https://spack.io) environment for installing and managing [THAPI](https://github.com/argonne-lcf/THAPI).

## How to Install THAPI

✍️**Note**: This guide assumes `spack` is installed and available in your `PATH`. If it is not, see [How to Install Spack](#how-to-install-spack).

```bash
# Clone the THAPI-spack repository and add it as a Spack repo
git clone https://github.com/argonne-lcf/THAPI-spack
spack repo add ./THAPI-spack/
# Install THAPI
spack install thapi
```

Once installed, you can load THAPI with:
```bash
spack load thapi
```

### Tips for speeding up THAPI installation

#### `spack external find`
`spack external find` can be used to find existing packages on the system known to Spack. This way you can
avoid building them when building THAPI. Use the following command before installing THAPI to find external
packages available on the system:
```bash
spack external find --all
```
Some packages when found using `spack external find` are known to cause build failures. If you run into such
cases, use `spack external find --exclude <pkg>` so that Spack will build them instead of using the system
installed versions. For example:
```bash
spack external find --all --exclude bzip2 --exclude xz --exclude curl
```

#### `--concurrent-packages`
One may also be able to reduce the time to install THAPI by using `--concurrent-packages` option in `spack install`
as below:
```bash
spack install --concurrent-packages 2 thapi
```
Depending on the available number of CPU cores and how parallelizable the dependency graph is for the particular
specification, one may be able to specify more concurrent packages (as compared to `2` in the above example).


## Building THAPI from Source

You can use Spack to install the required dependencies and set up the environment to build THAPI from source:
```bash
spack build-env thapi bash
```
This will spawn a new shell with the correct environment variables set for building THAPI manually.


## Miscelanous

### How to Install Spack

⚠️ **Important**: The default branch for Spack is `develop`, which is unstable. To ensure a reliable installation,
use the latest release of Spack.

To install spack:
```bash
git clone -c feature.manyFiles=true -b releases/latest https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
```
