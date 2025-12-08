from spack.package import *
import os


class Ittapi(CMakePackage):
    """Intel Instrumentation and Tracing Technology API."""

    homepage = "https://github.com/intel/ittapi"
    git = "https://github.com/intel/ittapi.git"
    url = "https://github.com/intel/ittapi/archive/refs/tags/v3.26.4.tar.gz"

    version("3.26.4", sha256="22e62bc1e0bae9ca001d6ae7447d26b7bcfe5d955724d74e6bd1e3e2102b48b1")

    variant("fortran", default=False, description="Enable Fortran support")

    depends_on("c", type=("build"))
    depends_on("cxx", type=("build"))
    depends_on("fortran", type=("build"), when="+fortran")
    depends_on("cmake@3.5:", type=("build"))
    depends_on("python@3.6:", type=("build"))

    def cmake_args(self):
        args = []

        if self.spec.satisfies("fortran"):
            args.append("-DITT_API_FORTRAN_SUPPORT=ON")

        return args

    def setup_run_environment(self, env):
        env.set("ITTAPI_ROOT", self.prefix)
        env.prepend_path("C_INCLUDE_PATH", self.prefix.include)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib64 if os.path.isdir(self.prefix.lib64) else self.prefix.lib)
