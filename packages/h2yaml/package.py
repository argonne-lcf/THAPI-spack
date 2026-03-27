# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
import re
import os
import sys


def find_libclang(root, lib_ext):
    regex = re.compile(rf"libclang(?:-\d+)?.{lib_ext}(?:.\d+)?")
    for root, dirs, files in os.walk(root):
        for file in files:
            if regex.match(file):
                return os.path.join(root, file)


class H2yaml(PythonPackage):
    """Matrices describing affine transformation of the plane."""

    homepage = "https://github.com/TApplencourt/h2yaml"
    url = "https://github.com/TApplencourt/h2yaml/archive/refs/tags/v0.1.1.tar.gz"
    git = "https://github.com/TApplencourt/h2yaml.git"

    version("0.4.2", sha256="0e5cc1d7d4507373a9d85dd082e3ffda1436943c9516f7f385471b936bc59f6c")
    version("0.4.1", sha256="c79b1cc766259d9af4562e5c83eede97fba6206ba5223cc3166fc8c045ed180b")
    version("0.4.0", sha256="0b7dce0eb82a6bb0fa169628b7d00fa5ca0e00c5a6c0e147f465718ed25a35b3")
    version("0.3.2", sha256="57fa0163ae3a27b9a44dc1c85a4886a49a528c30605502faff1ac380fa69e9b6")
    version("0.3.1", sha256="f1a45e83bd1898add516a380dd0d7b54870f6e9211b9bc068bd73f93f297033f")
    version("0.3.0", sha256="f78f4c9f4516736ffe000a5ea691557cb7091cff7337af2936483a90eac4ffcd")
    version("0.1.4", sha256="0c1e3871833a984f6d8375a69659f199eb30bcb51ed45b99c01c33abc7367b7c")
    version("0.1.3", sha256="f521f33c4db9abdb329969e256d32bee52fe9ff51643c56a5572a2329cfe72eb")
    version("0.1.2", sha256="d5a338da036d35f8fc3faa381a2b41a8f4cc68d7ca5abbf114c2569ca63e47ec")
    version("0.1.1", sha256="7bc695d4aca62baae9708e20351c94154db08a26f7fd31b9b0f2e52bcfd0bf98")

    depends_on("python@3.10:", type=("build", "run", "test"))
    depends_on("py-setuptools", type="build")
    depends_on("py-libclang@18", type=("run", "test"), when="@:0.4.0")
    depends_on("llvm@18:+clang+python", type=("run", "test"), when="@0.4.1:")
    depends_on("py-pyyaml", type=("run", "test"))
    depends_on("py-pytest", type=("test"))

    def setup_build_environment(self, env):
        """Wrapper until spack has a real implementation of setup_test_environment()"""
        if self.run_tests:
            # Workarround to some bug with pythonpath
            env.prepend_path("PYTHONPATH", self.stage.source_path)
            self.setup_test_environment(env)

    def setup_run_environment(self, env):
        if self.version < Version("0.4.1"):
            return
        super().setup_run_environment(env)
        s = self.spec["llvm"]
        llvm_config = os.path.join(s.prefix.bin, "llvm-config-" + str(s.version[0]))
        if not os.path.exists(llvm_config):
            llvm_config = os.path.join(s.prefix.bin, "llvm-config")
        output = Executable(llvm_config)("--libdir", output=str, error=str, fail_on_error=False)
        lib_path = output.rstrip()

        lib_ext = "dylib" if sys.platform == "darwin" else "so"
        lib_so = join_path(self.spec["llvm"].prefix.lib, f"libclang.{lib_ext}")
        if not os.path.isfile(lib_so):
            lib_so = find_libclang(lib_path, lib_ext)
        env.set("LIBCLANG_LIBRARY_FILE", join_path(self.spec["llvm"].prefix.lib, lib_so))

        # Set PYTHONPATH so that `import clang` will work without an issue.
        env.append_path("PYTHONPATH", join_path(self.spec["llvm"].prefix.lib, f"python{self.spec['python'].version.up_to(2)}", "site-packages"))

    def setup_test_environment(self, env):
        if self.version < Version("0.4.1"):
            return
        self.setup_run_environment(env)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        python("-m", "pytest", ".")
