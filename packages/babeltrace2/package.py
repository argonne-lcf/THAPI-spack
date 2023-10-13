# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Babeltrace2(AutotoolsPackage):
    """Babeltrace /ˈbæbəltreɪs/, an EfficiOS project, is an open-source
    trace manipulation toolkit."""

    homepage = "https://babeltrace.org/"
    url      = "https://www.efficios.com/files/babeltrace/babeltrace2-2.0.2.tar.bz2"

    maintainers = ['Kerilk']

    version('2.0.5',      sha256='7b8f9ef2a7ee7c9ec292d4568811cf6926089b25e49cdaab449e2cb724edf2b4')
    version('2.0.4',      sha256='774f116685dab5db9c51577dde43c8c1df482aae6bb78a089b1e9e7c8b489bca')
    version('2.0.3',      sha256='a53625152554102d868ba8395347d0daba0bec9c4b854c3e9bd97c77b0bf04a0')
    version('2.0.2',      sha256='30c684e8b948fb79b12ee6861957dc3b99f2aba33a11cfb7fbe598e8a4aae24a')

    variant('python-bindings', default=False, description='Build the Python bindings')
    variant('python-plugins', default=False, description='Enable the Python plugins support for the library and converter')
    variant('debug-info', default=True, description='disable the debug info support (default on macOS, Solaris and Windows)')
    variant('api-doc', default=False, description='Build HTML API documentation')
    variant('built-in-plugins', default=False, description='Statically-link in-tree plug-ins into the babeltrace2 executable')
    variant('built-in-python-plugin-support', default=False, description='Statically-link Python plugin support into the babeltrace library')
    variant('man-pages', default=False, description='Build man pages')
    variant('Werror', default=False, description='Enable -Werror')

    depends_on('glib@2.28:', type=('build', 'link'))
    depends_on('elfutils@0.154:')
    depends_on('python@3.4:', when='+python-bindings')
    depends_on('python@3.4:', when='+python-plugins')
    depends_on('python@3.4:', when='+built-in-python-plugin-support')
    depends_on('swig@3.0:', when='+python-bindings')
    depends_on('swig@3.0:', when='+python-plugins')
    depends_on('swig@3.0:', when='+built-in-python-plugin-support')
    depends_on('doxygen@1.8.6:', when='+api-doc')
    depends_on('asciidoc@8.6.8:', when='+man-pages')
    depends_on('xmlto@0.0.25:', when='+man-pages')
    depends_on('pkg-config')

    patch('d2d2e6cc.patch', when='@:2.0.4')
    patch('0db1832.patch', when='@:2.0.4')
    patch('3079913.patch')
    patch('0001-ctf-grow-stored_values-array-when-necessary.patch', when='@2.0.4:')

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable('python-bindings'))
        args.extend(self.enable_or_disable('python-plugins'))
        args.extend(self.enable_or_disable('debug-info'))
        args.extend(self.enable_or_disable('api-doc'))
        args.extend(self.enable_or_disable('built-in-plugins'))
        args.extend(self.enable_or_disable('built-in-python-plugin-support'))
        args.extend(self.enable_or_disable('man-pages'))
        args.extend(self.enable_or_disable('Werror'))

        if ('+python-bindings' in self.spec or
            '+python-plugins' in self.spec or
            '+built-in-python-plugin-support' in self.spec):
            def setup_run_environment(self, env):
                env.prepend_path('PYTHONPATH', self.prefix)

        return args
