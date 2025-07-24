# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
class LttngUst(AutotoolsPackage):
    """Linux Tracing Toolkit next generation user space tracer (LTTng-UST)."""

    homepage = "https://lttng.org"
    url      = "https://lttng.org/files/lttng-ust/lttng-ust-2.12.0.tar.bz2"
    git      = "https://github.com/lttng/lttng-ust.git"

    maintainers = ['Kerilk']

    version('master', branch='master')
    version("2.14.0", sha256="82cdfd304bbb2b2b7d17cc951a6756b37a9f73868ec0ba7db448a0d5ca51b763")
    version("2.13.9", sha256="c56418f49f12dab9c0333c4cacf2511bbd8bf28fb5604ce7439a816cde18f132")
    version("2.13.8", sha256="d4ef98dab9a37ad4f524ccafdfd50af4f266039b528dd5afabce78e49024d937")
    version('2.13.6', sha256='e7e04596dd73ac7aa99e27cd000f949dbb0fed51bd29099f9b08a25c1df0ced5')
    version('2.12.4', sha256='2124da2003a921f5da86c9aec00b897b5bbc006b0110a3ab29f1c1bc1c073f86')
    version('2.12.0', sha256='1983edb525f3f27e3494088d8d5389b4c71af66bbfe63c6f1df2ad95aa44a528')
    version('2.11.2', sha256='6b481cec7fe748503c827319e3356137bceef4cce8adecbda3a94c6effcdd161')
    version('2.10.7', sha256='a9c651eea8a33f50c07a6e69e3e4094e4897340c97eb0166e6dde0e80668742b')

    patch('1f41dc0.diff', when='@2.13.4:2.13.6')
    patch('55cca69.diff', when='@2.13.4:')

    variant('api-doc', default=False, description='Build HTML API documentation')
    variant('man-pages', default=False, description='Build man pages')

    with when("+man-pages"):
        depends_on('asciidoc@8.6.8:', type='build')
        depends_on('xmlto@0.0.25:', type='build')

    with when("+api-doc"):
        depends_on('asciidoc@8.6.8:', type='build')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('userspace-rcu@0.14:', when='@2.14:')
    depends_on('userspace-rcu@0.12:', when='@2.13:')
    depends_on('userspace-rcu@0.11:', when='@:2.12.999')
    depends_on('numactl')
    depends_on('pkg-config')

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("api-doc"))
        args.extend(self.enable_or_disable("man-pages"))
        return args

    def setup_build_environment(self, env):
        # Without the following line, configure checks for userspace-rcu headers
        # fails to find them in some systems.
        env.prepend_path("CPPFLAGS", "-I" + self.spec["userspace-rcu"].prefix.include)
        # Without the following line, configure checks for userspace-rcu libraries
        # fails to find them in some systems.
        env.prepend_path("LDFLAGS", "-L" + self.spec["userspace-rcu"].prefix.lib)
