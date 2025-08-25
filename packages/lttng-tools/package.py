# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *


class LttngTools(AutotoolsPackage):
    """Linux Tracing Toolkit next generation tools (LTTng-tools)."""

    homepage = "https://lttng.org"
    url = "https://lttng.org/files/lttng-tools/lttng-tools-2.12.0.tar.bz2"
    git = "https://github.com/lttng/lttng-tools.git"

    maintainers = ["Kerilk"]

    version("master", branch="master")
    version("2.14.0-archive", git="https://github.com/argonne-lcf/lttng-tools.git", branch="anl-ms3-v2.14.0")
    version("2.14.0", sha256="d8c39c26cec13b7bd82551cd52a22efc358b888e36ebcf9c1b60ef1c3a3c2fd3")
    version("2.13.15", sha256="edfcf924d86054178b286b50e151a440eee9ad79b7e08d7d12c84dc006ca151f")
    version("2.13.14", sha256="6213d9ed0d24b791c074f39b439ff85670eeaefc483d2b73c19fcf79ec1621d4")
    version("2.13.13", sha256="ff5f4f00b081dac66092afe8e72b7c790670931cf1c1ee0deaa7f80fbc53883e")
    version("2.13.9", sha256="8d94dc95b608cf70216b01203a3f8242b97a232db2e23421a2f43708da08f337")
    version("2.12.11", sha256="40a394400aa751231116602a0a53f6943237c56f25c53f422b5b4b38361b96b8")
    version("2.12.0", sha256="405661d27617dc79a42712174a051a45c7ca12d167576c0d93f2de708ed29445")
    version("2.11.3", sha256="d7e50f5fe3782e4d2d95ed7021c11a703ab8a3272d8473e0bdb4e37c1990a2c2")
    version("2.10.11", sha256="3cb7341d2802ba154f6863c5c20368f8273173ab7080c3ae1ae7180ac7a6f8c5")

    variant("man-pages", default=False, description="Build man pages")
    # FIXME: spack runs into build failures building the lttng-tools tests.
    variant("tests", default=False, description="Build the tests")
    variant("bin-lttng-crash", default=True, description="Enable lttng components related to crash tracing")

    depends_on("lttng-ust@master", when="@master")
    depends_on("lttng-ust@2.14.0:2.14.999", when="@2.14.0:2.14.999")
    depends_on("lttng-ust@2.13.8:2.13.999", when="@2.13.13:2.13.999")
    depends_on("lttng-ust@2.13.0:2.13.6", when="@2.13.0:2.13.9")
    depends_on("lttng-ust@2.12.0:2.12.999", when="@2.12")
    depends_on("lttng-ust@2.11.0:2.11.999", when="@2.11")
    depends_on("lttng-ust@2.10.0:2.10.999", when="@2.10")

    depends_on("babeltrace2", type="build", when="+tests")
    depends_on("babeltrace2", when="@2.14: +bin-lttng-crash")

    with when("+man-pages"):
        depends_on("asciidoc@8.6.8:", type="build")
        depends_on("xmlto@0.0.25:", type="build")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("pkg-config")

    # https://github.com/spack/spack/commit/e53bc780e4afdbec7263ef06c6266529abac4253
    depends_on("uuid")
    depends_on("popt@1.13:")
    depends_on("userspace-rcu@0.14.1:", when="@2.14:")
    depends_on("userspace-rcu@0.11.0:", when="@2.11:")
    depends_on("userspace-rcu@0.9.0:", when="@:2.10.999")
    depends_on("libxml2@2.7.6:")

    conflicts("+bin-lttng-crash", when="@2.14.0-archive")

    patch("popt_include_fixes.patch", when="@:2.12.999")
    # `--disable-test` is not available on lttng-tools v2.12 and below. Even though we have the
    # variant on our spack package, it doesn't actually turn off the tests without this patch.
    patch("disable_tests.patch", when="@:2.12.999")
    # disable_tests.patch changes configure.ac so we need to regenerate the configure file.
    # Apparently, spack doesn't generate the configure file if there is one already.
    force_autoreconf = True

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("man-pages"))
        args.extend(self.enable_or_disable("tests"))
        args.extend(self.enable_or_disable("bin-lttng-crash"))
        return args

    def setup_build_environment(self, env):
        # Without the following line, configure checks for userspace-rcu headers
        # fails to find them in some systems.
        env.prepend_path("CPPFLAGS", "-I" + self.spec["userspace-rcu"].prefix.include)
        # Without the following line, configure checks for userspace-rcu libraries
        # fails to find them in some systems.
        env.prepend_path("LDFLAGS", "-L" + self.spec["userspace-rcu"].prefix.lib)
