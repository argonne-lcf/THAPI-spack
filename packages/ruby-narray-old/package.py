# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyNarrayOld(RubyPackage):
    """Numerical N-dimensional Array class"""

    homepage = "http://masa16.github.io/narray/"
    url      = "https://rubygems.org/downloads/narray-0.6.1.2.gem"

    version('0.6.1.2', sha256='73bf101929a1570e8034058e1296fec58d6c3386c26bf26810d33f70dd4236b7', expand=False)

    depends_on('ruby', type=('build', 'run'))
