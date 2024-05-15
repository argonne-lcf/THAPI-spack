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
git clone -c feature.manyFiles=true -b releases/latest https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
```

## Note regarding building THAPI from source

You can use spack to install THAPI, then use `spack build-env thapi` to get the correct environment required to build THAPI for source. ( `spack build-env thapi bash` will spwan a new bash will all the ENV variable corretcly set) 

# Troubleshooting
## Errors with the C Compiler

If spack cannot find or use your C compiler (may see messages like `C compiler cannot create executables` or that your compiler `does not have your C++ compiler configured`), you may need to make sure spack is using gcc version 11.4.0 instead of more recent versions that can conflict with your build process. Run `spack config get compilers` to check your gcc version for spack. You might see only more recent versions of gcc like 12.3.0, or both 11.4.0 and newer versions. Either way, you will want to [manually conifgure your compilers](https://spack.readthedocs.io/en/latest/getting_started.html#manual-compiler-configuration) so that ONLY gcc 11.4.0 is present. This edit can be done by running `spack config edit compilers`. You can then remove the section that looks similar to this:

```
- compiler:
    spec: gcc@=12.3.0
    paths:
      cc: /usr/bin/gcc-12
      cxx: null
      f77: null
      fc: null
    flags: {}
    operating_system: ubuntu22.04
    target: x86_64
    modules: []
    environment: {}
    extra_rpaths: []
```
and add/keep the section that looks something like this:
```
- compiler:
    spec: gcc@=11.4.0
    paths:
      cc: /usr/bin/gcc
      cxx: /usr/bin/g++
      f77: /usr/bin/gfortran
      fc: /usr/bin/gfortran
    flags: {}
    operating_system: ubuntu22.04
    target: x86_64
    modules: []
    environment: {}
    extra_rpaths: []
```
allowing you to rebuild THAPI.