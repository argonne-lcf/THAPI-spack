# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LttngTools(AutotoolsPackage):
    """Linux Tracing Toolkit next generation tools (LTTng-tools)."""

    homepage = "https://lttng.org"
    url      = "https://lttng.org/files/lttng-tools/lttng-tools-2.12.0.tar.bz2"
    git      = "https://github.com/lttng/lttng-tools.git"

    maintainers = ['Kerilk']

    version('master', branch='master')
    version('2.13.9',  sha256='8d94dc95b608cf70216b01203a3f8242b97a232db2e23421a2f43708da08f337')
    version('2.12.11', sha256='40a394400aa751231116602a0a53f6943237c56f25c53f422b5b4b38361b96b8')
    version('2.12.0',  sha256='405661d27617dc79a42712174a051a45c7ca12d167576c0d93f2de708ed29445')
    version('2.11.3',  sha256='d7e50f5fe3782e4d2d95ed7021c11a703ab8a3272d8473e0bdb4e37c1990a2c2')
    version('2.10.11', sha256='3cb7341d2802ba154f6863c5c20368f8273173ab7080c3ae1ae7180ac7a6f8c5')

    depends_on('lttng-ust@master', when='@master')
    depends_on('lttng-ust@2.13.0:2.13.999', when='@2.13')
    depends_on('lttng-ust@2.12.0:2.12.999', when='@2.12')
    depends_on('lttng-ust@2.11.0:2.11.999', when='@2.11')
    depends_on('lttng-ust@2.10.0:2.10.999', when='@2.10')

    depends_on('asciidoc@8.6.8:', type='build')
    depends_on('xmlto@0.0.25:', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('libuuid')
    depends_on('popt@1.13:')
    depends_on('userspace-rcu@0.14.0:', when='@2.14:')
    depends_on('userspace-rcu@0.11.0:', when='@2.11:')
    depends_on('userspace-rcu@0.9.0:', when='@:2.10.999')
    depends_on('libxml2@2.7.6:')
    depends_on('pkg-config')

    patch('71540e4.diff', when='@2.14:')
