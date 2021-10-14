# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LttngUst(AutotoolsPackage):
    """Linux Tracing Toolkit next generation user space tracer (LTTng-UST)."""

    homepage = "https://lttng.org"
    url      = "https://lttng.org/files/lttng-ust/lttng-ust-2.12.0.tar.bz2"

    maintainers = ['Kerilk']

    version('2.12.0', sha256='1983edb525f3f27e3494088d8d5389b4c71af66bbfe63c6f1df2ad95aa44a528')
    version('2.11.2', sha256='6b481cec7fe748503c827319e3356137bceef4cce8adecbda3a94c6effcdd161')
    version('2.10.7', sha256='a9c651eea8a33f50c07a6e69e3e4094e4897340c97eb0166e6dde0e80668742b')

    depends_on('userspace-rcu@0.11:')
    depends_on('numactl')
