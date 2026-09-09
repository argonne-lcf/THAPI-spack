# THAPI-spack

This repository provides a [Spack](https://spack.io) environment for installing and managing
[THAPI](https://github.com/argonne-lcf/THAPI).

## How to Install THAPI

✍️**Note**: This guide assumes `spack` is installed and available in your `PATH`. If it is not,
see [How to Install Spack](#how-to-install-spack).

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

### Tips For Speeding Up THAPI Installation

#### `spack external find`

`spack external find` can be used to find existing packages on the system known to Spack. This way you can
avoid building them when building THAPI. Use the following command before installing THAPI to find external
packages available on the system:
```bash
spack external find --all --exclude llvm
```
Always exclude `llvm`: the entry detection writes cannot satisfy `h2yaml`. Declare that one with
the helper instead -- see [Reusing a system LLVM](#reusing-a-system-llvm).

Make sure to `module load` the packages you want Spack to find (or set other environment variables like `PATH`)
before running it.

Some packages when found using `spack external find` are known to cause build failures. If you run into such
cases, use `spack external find --exclude <pkg>` so that Spack will build them instead of using the system
installed versions. For example:
```bash
spack external find --all --exclude bzip2 --exclude xz --exclude curl --exclude llvm
```

#### Reusing a system LLVM

`thapi@0.0.14:` needs `h2yaml`, which needs `llvm@18:+clang+python`. That `+python` means the LLVM
prefix must contain clang's Python bindings (`clang/cindex.py`), not just `libclang.so`. Building
LLVM from source is by far the longest step of a THAPI install, so it is worth reusing a system one.

Point the helper at any LLVM 18+ on the system (`module avail llvm`, `/usr/lib/llvm-*`,
`/opt/llvm*`, or your site software tree) and apply what it prints:

```bash
# The python Spack will run h2yaml with, so the overlay is laid out to match.
PYVER=$(spack spec -j h2yaml | grep -v '^==>' \
  | jq -r '[.spec.nodes[] | select(.name == "python") | .version | split(".")[:2] | join(".")]
           | unique | .[0]')

python3 scripts/gen-llvm-external.py /path/to/system/llvm --python-version $PYVER > llvm-external.yaml
spack config add -f llvm-external.yaml
```

The script needs only Python 3, no dependencies. If the LLVM already has the bindings it points the
external straight at it. Otherwise -- a site LLVM is usually read-only, so they cannot just be
dropped in next to it -- it builds an *overlay* in `--overlay-dir` (default `~/.spack`): a tree of
symlinks to the real install, plus the bindings, downloaded from the matching LLVM release if the
system has none. The external points into that directory, so keep it.

If there is no LLVM 18+ on the system at all, skip this: Spack will build one.

Check that it took -- LLVM should show `[e]` rather than `-`:

```bash
spack spec -I thapi | grep llvm
```

> [!IMPORTANT]
> The external has to be declared this way rather than by `spack external find`, which picks variants
> from executables only and never looks for the bindings. It therefore always records LLVM as
> `~python` -- bindings present or not -- and such an entry can never satisfy `h2yaml`: Spack ignores
> it and, unless something else provides `+python`, builds LLVM from source. Always pass
> `--exclude llvm` when running it.

#### `spack install -j<core> <spec>`

Depending on the number of available cores on your platform, you can specify number of parallel build
processes to be used during the build of `spec` using `-j` option to `spack` (e.g., `-j16`).

## Building THAPI Manually

You can use Spack to install the required dependencies and set up the environment to build THAPI manually
from source (without using Spack to build THAPI):
```bash
spack build-env thapi bash
```
This will spawn a new shell with the correct environment variables and dependencies set for building THAPI
manually. This is useful when building THAPI for your own development work.

## Known Issues

- THAPI Spack package (and some of its dependencies) is known to run into build failures with NVHPC SDK
  (available on ALCF Polaris for example). Please make sure to use GNU programming environment whenever
  possible.
- Users have noticed `spack` processes getting killed (due to timeout) on login nodes on both ALCF Aurora
  and Polaris. Use a compute node whenever possible.

## Miscellaneous

### How to Install Spack

⚠️ **Important**: The default branch for Spack is `develop`, which is unstable. To ensure a reliable installation,
use the latest release of Spack.

To install Spack:
```bash
git clone -c feature.manyFiles=true -b releases/latest https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
```
