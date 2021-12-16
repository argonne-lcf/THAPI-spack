# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LttngTools(AutotoolsPackage):
    """Linux Tracing Toolkit next generation tools (LTTng-tools)."""

    homepage = "https://lttng.org"
    url      = "https://lttng.org/files/lttng-tools/lttng-tools-2.12.0.tar.bz2"

    maintainers = ['Kerilk']

    version('2.12.0',  sha256='405661d27617dc79a42712174a051a45c7ca12d167576c0d93f2de708ed29445')
    version('2.11.3',  sha256='d7e50f5fe3782e4d2d95ed7021c11a703ab8a3272d8473e0bdb4e37c1990a2c2')
    version('2.10.11', sha256='3cb7341d2802ba154f6863c5c20368f8273173ab7080c3ae1ae7180ac7a6f8c5')

    depends_on('lttng-ust@2.12.0:2.12.999', when='@2.12')
    depends_on('lttng-ust@2.11.0:2.11.999', when='@2.11')
    depends_on('lttng-ust@2.10.0:2.10.999', when='@2.10')

    depends_on('libuuid')
    depends_on('popt@1.13:')
    depends_on('userspace-rcu@0.9.0:')
    depends_on('libxml2@2.7.6:')
    depends_on('pkg-config')
