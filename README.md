# THAPI-spack
This is a spack environment for THAPI.

## How to install THAPI

This assumes that you have a valid `spack` in your path

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
git clone -c feature.manyFiles=true -b releases/latest https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
```

## Note regarding building THAPI from source

You can use spack to install THAPI, then use `spack build-env thapi` to get the correct environment required to build THAPI for source. ( `spack build-env thapi bash` will spawn a new bash will all the ENV variables corretcly set) 

