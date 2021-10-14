# THAPI-spack
This is a spack environement for THAPI.

## How to use to install THAPI

Due to a current limitation on the ruby support of spack, one need to use our patched spack version
```
 git clone --depth 1 --branch fix-ruby https://github.com/Kerilk/spack.git
 git clone https://github.com/argonne-lcf/THAPI-spack
 spack repo add ./THAPI-spack/

 spack install gcc
 spack load gcc

 spack install thapi
 spack load thapi
```
