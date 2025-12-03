from spack.package import *
import sys


class PyIttapi(PythonPackage):
    homepage = "https://pypi.org/project/ittapi"
    git = "https://github.com/intel/ittapi"
    url = "https://github.com/intel/ittapi/archive/refs/tags/v3.26.4.tar.gz"
    build_directory = "python"

    version(
        "1.2.0",
        sha256="22e62bc1e0bae9ca001d6ae7447d26b7bcfe5d955724d74e6bd1e3e2102b48b1",
        url="https://github.com/intel/ittapi/archive/refs/tags/v3.26.4.tar.gz",
    )

    depends_on("ittapi", type=("build", "run"))
    depends_on("py-setuptools", type="build")
