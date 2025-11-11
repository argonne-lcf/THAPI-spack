# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from glob import glob
from os import *
import subprocess
import sys


class PyLibclang(PythonPackage):
    """The repository contains code that taken from the LLVM project, to make
    it easier to install clang's python bindings."""

    homepage = "https://github.com/sighingnow/libclang"

    url = "https://github.com/sighingnow/libclang/archive/refs/tags/llvm-11.1.0.tar.gz"

    license("Apache-2.0")

    version("18.1.1", sha256="829f1afbf6a704da2130f541279e58d719eb9b67713a0641eb723a2970de1b66")
    version("17.0.6", sha256="dfdc19199ba3ed2169e7f9849bd1472d61fc1fdb8af699e3d083c27e53d394c3")
    version("16.0.6", sha256="626bc239e7568354c8bc5137541732ae81c4e65221b27d9021b9f13306a7a1b2")
    version("16.0.0", sha256="a3eae57519209ed6fca4e76425f3159e54a08cbb2918d92a7a35640d4c28ec07")
    version("15.0.6.1", sha256="f8ac6e30868e9eb92bb1001920230381565f9a3cf415411d3b67bb2339640d81")
    version("14.0.6", sha256="3666679d9f23270a230a4d4dae49bc48fc2515c272ff5855b2618e23daa50100")
    version("14.0.1", sha256="58a255381d6360aca8d4978c8bb2e6be55ac0bdd18bc10372da0febe0a7f9472")

    depends_on("python@2.7:2.8,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    patch("0001-Add-environment-variable-LIBCLANG_LIBRARY_FILE-to-se.patch", when="@13.0.0:16.0.6")
    patch("0002-Add-environment-variable-LIBCLANG_LIBRARY_FILE-to-se.patch", when="@17.0.6:")

    for ver in ["14", "15", "16", "17", "18"]:
        depends_on("llvm+clang@" + ver, when="@" + ver, type="build")

    def setup_run_environment(self, env):
        super().setup_run_environment(env)
        s = self.spec["llvm"]
        cp = subprocess.run(
            [path.join(s.prefix.bin, "llvm-config-" + str(s.version[0])), "--libdir"], capture_output=True, encoding=sys.stdout.encoding
        )
        libpath = cp.stdout.rstrip("\r\n")
        libpattern = path.join(libpath, "libclang-" + str(s.version[0]) + ".*")
        libname = glob(libpattern)[0]
        env.set("LIBCLANG_LIBRARY_FILE", libname)
