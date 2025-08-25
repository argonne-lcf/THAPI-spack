# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyRitual(RubyPackage):
    """Adds tasks and helpers to your Rakefile to manage releases in a lightweight manner."""

    homepage = "https://github.com/oggy/ritual"
    url      = "https://rubygems.org/downloads/ritual-0.5.1.gem"

    # fmt: off
    version('0.5.1', sha256='9c1a574b23a98c0139fa87d1c30ea85094e14fe194d11bfa975e58248788770b', expand=False)
    # fmt: on

    depends_on('ruby@2.3.0:', type=('build', 'run'))
    depends_on('ruby-thor', type=('build', 'run'))
    depends_on('ruby-rake', type=('build', 'run'))

