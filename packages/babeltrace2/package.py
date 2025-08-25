# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Babeltrace2(AutotoolsPackage):
    """Babeltrace /ˈbæbəltreɪs/, an EfficiOS project, is an open-source
    trace manipulation toolkit."""

    homepage = "https://babeltrace.org/"
    url      = "https://www.efficios.com/files/babeltrace/babeltrace2-2.0.2.tar.bz2"
    git      = "https://github.com/efficios/babeltrace.git"

    maintainers = ['Kerilk']

    # fmt: off 
    version('master', branch='master')
    version('2.1.1',      sha256='5033ca8c57fdb5b110f44693b543c01bbf8b0cafdf1496930aad4c0e74c4727f')
    version('2.1.0',      sha256='af182591efe62039e22d02e93a083d7835df21eac8cf84a4c980804f76040e48')
    version('2.0.6',      sha256='a01c7e75e642de0b5b91f32cc706234c99eb556fcd52c9959045dc23a9ec52c9')
    version('2.0.5',      sha256='7b8f9ef2a7ee7c9ec292d4568811cf6926089b25e49cdaab449e2cb724edf2b4')
    version('2.0.4',      sha256='774f116685dab5db9c51577dde43c8c1df482aae6bb78a089b1e9e7c8b489bca')
    version('2.0.3',      sha256='a53625152554102d868ba8395347d0daba0bec9c4b854c3e9bd97c77b0bf04a0')
    version('2.0.2',      sha256='30c684e8b948fb79b12ee6861957dc3b99f2aba33a11cfb7fbe598e8a4aae24a')
    # fmt: on

    variant('python-bindings', default=False, description='Build the Python bindings')
    variant('python-plugins', default=False, description='Enable the Python plugins support for the library and converter')
    # FIXME: Turning on debug-info=True causes a configure failure due to
    # autoconf not being able to find libdw.
    variant('debug-info', default=False, description='disable the debug info support (default on macOS, Solaris and Windows)')
    variant('api-doc', default=False, description='Build HTML API documentation')
    variant('built-in-plugins', default=False, description='Statically-link in-tree plug-ins into the babeltrace2 executable')
    variant('built-in-python-plugin-support', default=False, description='Statically-link Python plugin support into the babeltrace library')
    variant('man-pages', default=False, description='Build man pages')
    variant('asan', default=False, description='Build with AddressSanitizer', when='@2.1:')
    variant('ubsan', default=False, description='Build with UndefinedBehaviorSanitizer', when='@2.1:')
    variant('Werror', default=False, description='Enable -Werror')

    depends_on('c', type='build')
    depends_on('cxx', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('pkg-config')

    depends_on('glib@2.28:', type=('build', 'link'))
    depends_on('elfutils@0.154:')

    with when("+python-bindings"):
        depends_on('python@3.4:')
        depends_on('swig@3.0:')

    with when('+python-plugins'):
        depends_on('python@3.4:')
        depends_on('swig@3.0:')

    with when('+built-in-python-plugin-support'):
        depends_on('python@3.4:')
        depends_on('swig@3.0:')

    with when('+api-doc'):
        depends_on('asciidoc@8.6.8:')

    with when('+man-pages'):
        depends_on('asciidoc@8.6.8:')
        depends_on('xmlto@0.0.25:')

    # Add varient pour esam
    patch('d2d2e6cc.patch', when='@:2.0.999')
    patch('0001-Prevent-null-character-from-stopping-string-decoding.patch', when='@2.1:')

    patch('0db1832.patch', when='@:2.0.4')
    patch('3079913.patch', when='@:2.0.999')
    patch('0001-ctf-grow-stored_values-array-when-necessary.patch', when='@:2.0.999')

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable('python-bindings'))
        args.extend(self.enable_or_disable('python-plugins'))
        args.extend(self.enable_or_disable('debug-info'))
        args.extend(self.enable_or_disable('api-doc'))
        args.extend(self.enable_or_disable('built-in-plugins'))
        args.extend(self.enable_or_disable('built-in-python-plugin-support'))
        args.extend(self.enable_or_disable('man-pages'))
        with when('@2.1:'):
            args.extend(self.enable_or_disable('asan'))
            args.extend(self.enable_or_disable('ubsan'))
        args.extend(self.enable_or_disable('Werror'))

        if ('+python-bindings' in self.spec or
            '+python-plugins' in self.spec or
            '+built-in-python-plugin-support' in self.spec):
            def setup_run_environment(self, env):
                env.prepend_path('PYTHONPATH', self.prefix)

        return args

    def setup_build_environment(self, env):
        # Without the following line, conftest checking glib version picks up
        # system glib instead of the spack installed glib.
        env.prepend_path("LD_LIBRARY_PATH", self.spec["glib"].prefix.lib)
