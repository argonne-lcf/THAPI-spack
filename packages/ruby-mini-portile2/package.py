# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyMiniPortile2(RubyPackage):
    """Simplistic port-like solution for developers. It provides a standard and
       simplified way to compile against dependency libraries without messing up
       your system."""

    homepage = "https://github.com/flavorjones/mini_portile"
    url      = "https://rubygems.org/downloads/mini_portile2-2.7.0.gem"

    version('2.7.0', sha256='6416bf22d3e463fc318b34810920e73055418483b074330d95c773f4596dbdfc', expand=False)
    version('2.6.1', sha256='385fd7a2f3cda0ea5a0cb85551a936da941d7580fc9037a75dea820843aa7dd3', expand=False)

    depends_on('ruby@2.3.0:', type=('build', 'run'))
