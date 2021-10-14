# THAPI-spack
This is a spack environement for THAPI.

## How to install THAPI

Due to a current limitation on the ruby support of spack, one need to use our patched spack version (https://github.com/spack/spack/pull/26729) 
```
git clone --depth 1 --branch fix-ruby https://github.com/Kerilk/spack.git
source spack/share/spack/setup-env.sh
```

Then one can use the package of this repo to build thapi:
```
git clone https://github.com/argonne-lcf/THAPI-spack
spack repo add ./THAPI-spack/
spack install thapi
spack load thapi
```
