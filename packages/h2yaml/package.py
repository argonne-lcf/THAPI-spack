# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

class H2yaml(PythonPackage):
    """Matrices describing affine transformation of the plane."""

    homepage = "https://github.com/TApplencourt/h2yaml"
    url = "https://github.com/TApplencourt/h2yaml/archive/refs/tags/v0.1.1.tar.gz"

    version("0.1.4", sha256="0c1e3871833a984f6d8375a69659f199eb30bcb51ed45b99c01c33abc7367b7c")
    version("0.1.3", sha256="f521f33c4db9abdb329969e256d32bee52fe9ff51643c56a5572a2329cfe72eb")
    version("0.1.2", sha256="d5a338da036d35f8fc3faa381a2b41a8f4cc68d7ca5abbf114c2569ca63e47ec")
    version("0.1.1", sha256="7bc695d4aca62baae9708e20351c94154db08a26f7fd31b9b0f2e52bcfd0bf98")

    depends_on("python@3.10:", type=("build", "run", "test"))
    depends_on("py-setuptools", type="build")
    depends_on("py-libclang@18:", type=("run", "test"))
    depends_on("llvm@18:+clang", type=("run", "test"))
    depends_on("py-pyyaml", type=("run", "test"))
    depends_on("py-pytest", type=("test"))

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["llvm"].prefix.lib)

    def setup_test_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["llvm"].prefix.lib)

    def setup_build_environment(self, env):
        """Wrapper until spack has a real implementation of setup_test_environment()"""
        if self.run_tests:
            # Workarround to some bug with pythonpath
            env.prepend_path("PYTHONPATH", self.stage.source_path)
            self.setup_test_environment(env)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        python("-m", "pytest", ".")
