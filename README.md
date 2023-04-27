# THAPI-spack
This is a spack environement for THAPI.

## How to install THAPI

This assume that you have a valid `spack` in your path

```
git clone https://github.com/argonne-lcf/THAPI-spack
spack repo add ./THAPI-spack/
spack install thapi
```

Then you can simply load  thapi it via 
```
spack load thapi
```

### How to install spack

```
git clone -c feature.manyFiles=true https://github.com/spack/spack.git
cd spack/
git checkout releases/latest
. share/spack/setup-env.sh
```
