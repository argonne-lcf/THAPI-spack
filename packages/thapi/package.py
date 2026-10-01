# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.version
from spack.package import *

# When 0.0.17 is released and master is fast-forwarded past it,
# we can inline PRE_BLOB to "@:0.0.16" and BLOB to `@0.0.17:99`
PRE_BLOB = "@:0.0.16,master"
BLOB = "@0.0.17:99,develop"
# Same era, narrowed to the versions that have the feature: lttng became a
# dependency in 0.0.8, archive mode arrived in 0.0.13. Spelled out rather than
# PRE_BLOB + "@0.0.8:", which spack rejects as two version constraints on one
# spec; the point of naming them is that each hand-intersected range keeps the
# `master` PRE_BLOB names.
PRE_BLOB_TRACED = "@0.0.8:0.0.16,master"
PRE_BLOB_ARCHIVE = "@0.0.13:0.0.16,master"


class Thapi(AutotoolsPackage):
    """A tracing infrastructure for heterogeneous computing applications."""

    homepage = "https://github.com/argonne-lcf/THAPI"
    git = "https://github.com/argonne-lcf/THAPI.git"

    version("master", branch="master", preferred=True)
    version("develop", branch="devel")
    version("0.0.16", tag="v0.0.16")
    version("0.0.15", tag="v0.0.15")
    version("0.0.14", tag="v0.0.14")
    version("0.0.13", tag="v0.0.13")
    version("0.0.12", tag="v0.0.12")
    version("0.0.11", tag="v0.0.11")
    version("0.0.10", tag="v0.0.10")
    version("0.0.9", tag="v0.0.9")
    version("0.0.8", tag="v0.0.8")
    version("0.0.7", tag="v0.0.7")

    variant("strict", default=False, description="Enable -Werror during the build")
    variant("test-dependencies", default=False, description="Install THAPI test dependencies (bats, clinfo, etc.)")
    variant("mpi", default=False, description="Enable MPI support for the Sync Daemon", when="@:0.0.12")
    variant("sync-daemon-mpi", default=False, description="Enable MPI support for the Sync Daemon", when="@0.0.13:")
    variant("clang-parser", default=True, description="Enable Clang Parser", when="@0.0.13")
    variant("archive", default=False, description="Enable archive mode of THAPI", when=PRE_BLOB_ARCHIVE)
    # On by default from the BLOB port on: reading archives on the fly is what
    # the pause/resume back-pressure loop exists for. Disable with ~archive.
    variant("archive", default=True, description="Enable archive mode of THAPI", when=BLOB)

    depends_on("c", type=("build"))
    depends_on("cxx", type=("build"))
    depends_on("automake", type=("build"))
    depends_on("autoconf", type=("build"))
    depends_on("libtool", type=("build"))
    depends_on("pkgconfig")

    # 4.3+ for grouped target
    depends_on("gmake@4.3:", type=("build"))
    depends_on("protobuf@3.12.4:", type=("build", "link", "run"))
    # abseil-cpp@20250127.0: has an unguarded `#include <version>` in span.h that
    # picks up our utils/version data file. 0.0.16 renamed it to thapi_version,
    # so the cap only applies through 0.0.15. protobuf@30: needs those abseil
    # versions, so both are capped together.
    depends_on("protobuf@:29", type=("build", "link", "run"), when="@:0.0.15")
    depends_on("abseil-cpp@:20240722", type=("build", "link", "run"), when="@:0.0.15")

    # THAPI records raw bytes as BLOB fields since 0.0.17, which bounds both
    # halves of the round trip: lttng-ust 2.16 writes the field, babeltrace2 2.1
    # reads it. Before that it traced them as text and needed both halves of a
    # work-around instead -- a patched lttng-ust that wrote the field in full,
    # and a babeltrace that read it past its first NUL. So an older THAPI is
    # held to lttng-ust/lttng-tools 2.15 and asks babeltrace for
    # +text-as-bytes, while the blob era takes a stock 2.16 stack.
    depends_on("babeltrace2", type=("build", "link", "run"))
    depends_on("babeltrace2 +text-as-bytes", type=("build", "link", "run"), when=PRE_BLOB)
    depends_on("babeltrace2@2.1.0-archive", type=("build", "link", "run"), when=PRE_BLOB + " +archive")
    depends_on("babeltrace2@2.1.2-archive", type=("build", "link", "run"), when=BLOB + " +archive")
    # The bt_field_class_blob_* API is 2.1, so it bounds ~archive builds too --
    # the -archive versions above already satisfy it.
    depends_on("babeltrace2@2.1:", type=("build", "link", "run"), when=BLOB)

    depends_on("lttng-ust", type=("build", "link", "run"), when="@0.0.8:")
    depends_on("lttng-ust@:2.15", type=("build", "link", "run"), when=PRE_BLOB_TRACED)
    depends_on("lttng-ust@:2.12.999", type=("build", "link", "run"), when="@:0.0.7")
    depends_on("lttng-ust@2.16.0:", type=("build", "link", "run"), when=BLOB)

    depends_on("lttng-tools", type=("build", "link", "run"), when="@0.0.8:")
    depends_on("lttng-tools@:2.15", type=("build", "link", "run"), when=PRE_BLOB_TRACED)
    depends_on("lttng-tools@:2.12.999", type=("build", "link", "run"), when="@:0.0.7")
    depends_on("lttng-tools@2.14.0-archive ~bin-lttng-crash", type=("build", "link", "run"), when=PRE_BLOB + " +archive")
    depends_on("lttng-tools@2.16.0-archive ~bin-lttng-crash", type=("build", "link", "run"), when=BLOB + " +archive")

    # Check compilers and versions. Version checks are mainly for magic_enum:
    # https://github.com/Neargye/magic_enum?tab=readme-ov-file#compiler-compatibility
    conflicts("%gcc@:8", msg="GCC version >= 9 required.")
    conflicts("%llvm@:4", msg="clang >= 5 required.")
    conflicts("%oneapi@:2023", msg="OneAPI >= 2024.0.0 is required.")
    conflicts("%msvc", msg="MSVC is not supported.")

    # Restricting to ruby <= 3.1 when spack is less than 0.23
    if Version(spack.spack_version) < Version("0.23"):
        depends_on("ruby@2.7.0:3.1", type=("build", "run"))
    else:
        depends_on("ruby@2.7.0:", type=("build", "run"))

    depends_on("ruby-babeltrace2", type=("build", "run"))
    # Reading a blob-era trace needs the BLOB field support that no
    # ruby-babeltrace2 release carries yet.
    depends_on("ruby-babeltrace2@main", type=("build", "run"), when=BLOB)
    depends_on("ruby-opencl", type=("build", "run"))
    depends_on("ruby-nokogiri", type=("build"))
    depends_on("ruby-cast-to-yaml", type=("build"))
    depends_on("ruby-metababel@0.1.0:0.9", type=("build"), when="@:0.0.10")
    depends_on("ruby-metababel@1.0.0:", type=("build"), when="@0.0.11")
    depends_on("ruby-metababel@1.1.2:", type=("build"), when="@0.0.12:")
    depends_on("ruby-metababel@1.1.4:", type=("build"), when="@0.0.13:")
    # metababel 2.0.0 is a breaking change: a dynamic length is named by a
    # structured length_field_location, and the length_field_path these models
    # emit is no longer a keyword it accepts -- codegen dies with
    # `unknown keyword: length_field_path`. The floors above are open-ended, so
    # without this cap concretization hands 2.0.0 to a pre-blob THAPI.
    depends_on("ruby-metababel@:1", type=("build"), when=PRE_BLOB)
    # BLOB codegen, and the MIP-1 field locations it emits, are 2.0.0. Older
    # metababel dies on the generated yaml with `unknown keyword:
    # :length_field_location`. configure.ac requires >= 2.0.0 to match.
    depends_on("ruby-metababel@2.0.0:", type=("build"), when=BLOB)

    # Demangling: 0.0.16 switched from libiberty to llvm::demangle (a tiny
    # standalone extraction of LLVM's demangler) for the symbols
    # __cxa_demangle can't handle. +pic so the static lib links into the
    # shared babeltrace plugins.
    depends_on("libiberty+pic", when="@:0.0.15")
    depends_on("llvm-demangle+pic", when="@0.0.16:")
    depends_on("libffi")
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+sync-daemon-mpi")
    # 0.0.14 dropped --disable-clang-parser: configure now hard-errors without
    # h2yaml, so from there on it is an unconditional build dep.
    depends_on("h2yaml@0.4.3:", type=("build"), when="@0.0.13 +clang-parser")
    depends_on("h2yaml@0.4.3:", type=("build"), when="@0.0.14:")

    # Add dev tools required for THAPI development and testing.
    depends_on("bats", when="+test-dependencies")
    depends_on("clinfo", when="+test-dependencies")
    depends_on("jq", when="+test-dependencies")
    depends_on("ittapi", when="+test-dependencies")
    depends_on("py-ittapi", when="+test-dependencies")

    # We add a Python dependency at buildtime, because `lttng-gen-tp` needs it.
    # We don't add Python as a runtime dependency of lttng to avoid python
    # propagated as a runtime dependency of thapi
    depends_on("python", type=("build"))

    patch("0001-Ignore-int-conversions.patch", when="@0.0.8:0.0.11")

    def configure_args(self):
        args = []
        if self.spec.version >= Version("0.0.13"):
            args.extend(self.enable_or_disable("sync-daemon-mpi"))
        else:
            args.extend(self.enable_or_disable("mpi"))
        args.extend(self.enable_or_disable("strict"))

        # `--disable-clang-parser` only ever existed in 0.0.13; the clang
        # parser is mandatory from 0.0.14 on.
        if self.spec.satisfies("@0.0.13 ~clang-parser"):
            args.append("--disable-clang-parser")
        return args
