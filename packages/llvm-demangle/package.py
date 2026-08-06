# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class LlvmDemangle(CMakePackage):
    """Standalone extraction of LLVM's C++ symbol demangler (llvm/lib/Demangle).

    Builds just libLLVMDemangle and installs the public llvm/Demangle headers,
    with no dependency on the rest of LLVM. Provides llvm::demangle(), which
    handles Itanium symbols that libiberty's cplus_demangle() and libstdc++'s
    abi::__cxa_demangle() reject.
    """

    homepage = "https://github.com/TApplencourt/llvm-demangle"
    git = "https://github.com/TApplencourt/llvm-demangle.git"

    version("main", branch="main", preferred=True)

    # Static by default: consumers (THAPI) link the demangler straight into
    # their babeltrace plugins, so there is no runtime .so to locate.
    variant("shared", default=False, description="Build a shared library instead of static")
    # Position-independent code, so the static lib can be linked into shared
    # libraries (mirrors libiberty+pic, which THAPI used to depend on).
    variant("pic", default=True, description="Build with position-independent code")

    depends_on("cxx", type="build")
    depends_on("cmake@3.13:", type="build")

    def cmake_args(self):
        return [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]

    def setup_run_environment(self, env):
        # Only relevant for the shared flavor; the static default needs nothing.
        if self.spec.satisfies("+shared"):
            libdir = self.prefix.lib64 if os.path.isdir(self.prefix.lib64) else self.prefix.lib
            env.prepend_path("LD_LIBRARY_PATH", libdir)
