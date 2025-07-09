# THAPI-spack

This repository provides a [Spack](https://spack.io) environment for installing and managing [THAPI](https://github.com/argonne-lcf/THAPI).

## How to Install THAPI

> **Note**: This guide assumes `spack` is installed and available in your `PATH`.

⚠️ **Important**: The default branch for Spack is `develop`, which is be unstable. To ensure a reliable installation, use the `releases/latest` branch of Spack.  See the section below on installing Spack.

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

### How to Install Spack

If you don't have Spack installed yet:
```bash
git clone -c feature.manyFiles=true -b releases/latest https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
```

## Building THAPI from Source.

You can use Spack to install the required dependencies and set up the environment to build THAPI from source:
```bash
spack build-env thapi bash
```
This will spawn a new shell with the correct environment variables set for building THAPI manualy.
