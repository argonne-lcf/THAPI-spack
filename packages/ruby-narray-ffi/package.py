# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
class RubyNarrayFfi(RubyPackage):
    """Ruby narray ffi interface"""

    homepage = "https://github.com/Nanosim-LIG/narray-ffi"
    url      = "https://rubygems.org/downloads/narray_ffi-1.4.4.gem"

    version('1.4.4', sha256='26621b4cea463635867aa8305ad863e67c5bb8321df74e5d3fc95c6425b6197b', expand=False)

    depends_on('ruby', type=('build', 'run'))
    depends_on('ruby-narray-old', type=('build', 'run'))
    depends_on('ruby-ffi', type=('build', 'run'))

