# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyCast(RubyPackage):
    """C parser and AST constructor."""

    homepage = "http://github.com/oggy/cast"
    url      = "https://rubygems.org/downloads/cast-0.3.1.gem"

    version('0.3.1', sha256='0dd28460a9f1b925be20236223e5289bc23341ee2a46394f276c0bc097dba06e', expand=False)

    depends_on('ruby@2.3.0:', type=('build', 'run'))
