# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyWalk(RubyPackage):
    """Directory tree traversal tool inspired by python os.walk"""

    homepage = "https://rubygems.org/gems/walk"
    url      = "https://rubygems.org/downloads/walk-0.1.0.gem"

    version('0.1.0', sha256='79705078a5a505ab218ff154997b837b03639dc6422c492b6b9ee6e6ab01ff60', expand=False)

    depends_on('ruby', type=('build', 'run'))
