# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
class Babeltrace(AutotoolsPackage):
    """Babeltrace is a trace viewer and converter reading and writing the
    Common Trace Format (CTF). Its main use is to pretty-print CTF traces
    into a human-readable text output ordered by time."""

    homepage = "http://www.efficios.com/babeltrace"
    url      = "https://www.efficios.com/files/babeltrace/babeltrace-1.2.4.tar.bz2"

    version('1.5.8', sha256='9ff143e4d1d7f1902b05542ac8f1747fb2d7e0ca31c6fa39ccae5765e11d6fc2')
    version('1.2.4', sha256='666e3a1ad2dc7d5703059963056e7800f0eab59c8eeb6be2efe4f3acc5209eb1')

    variant('python', default=False, description="With python bindings")

    depends_on('c', type='build')
    depends_on('cxx', type='build')

    depends_on('glib@2.22:', type=('build', 'link'))
    depends_on('uuid')
    depends_on('popt')
    depends_on('elfutils', when='@1.4.0:')
    depends_on('python', when='+python')
    depends_on('swig', when='+python')
    depends_on('pkg-config')

    parallel = False

    def configure_args(self):
        args = []
        if '+python' in self.spec:
            args.append('--enable-python-bindings')
            def setup_run_environment(self, env):
              env.prepend_path('PYTHONPATH', self.prefix)
        return args
