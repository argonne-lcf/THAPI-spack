# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

class H2yaml(PythonPackage):
    """Matrices describing affine transformation of the plane."""

    homepage = "https://github.com/TApplencourt/h2yaml"
    url = "https://github.com/TApplencourt/h2yaml/archive/refs/tags/v0.1.1.tar.gz"

    version("0.1.1", sha256="7bc695d4aca62baae9708e20351c94154db08a26f7fd31b9b0f2e52bcfd0bf98")

    depends_on("python@3.10:", type=("build", "run", "test"))
    depends_on("py-setuptools", type="build")
    depends_on("llvm+python", type=("run","test"))
    depends_on("py-pyyaml", type=("run","test"))
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
