from spack.package import *
import sys


class PyIttapi(PythonPackage):
    homepage = "https://pypi.org/project/ittapi"
    list_url = "https://pypi.org/simple/ittapi/"

    def url_for_version(self, version):
        url = "https://pypi.io/packages/cp{1}/i/ittapi/ittapi-{0}-cp{1}-cp{1}-{2}.whl"

        if sys.platform.startswith("win"):
            platform_string = "win_amd64"
        elif sys.platform.startswith("linux"):
            platform_string = "manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64"

        py_ver = Version(version.string.split("y")[1])

        return url.format(version.string.split("-")[0], py_ver.joined, platform_string)

    if sys.platform.startswith("linux"):
        version(
            "1.2.0-py3.10",
            sha256="11ea1a75d9bcc3f67d29c5a0840c11810a0a0c631240ff17b06f4d0d4493ebda",
        )

    if sys.platform.startswith("win"):
        version(
            "1.2.0-py3.10",
            sha256="46e15efaf53291eb9a1e2e4ab9c44613a1ac5939ee86d123451a00b068fcadc1",
        )

    depends_on("python@3.10:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("ittapi", type=("build", "run"))
