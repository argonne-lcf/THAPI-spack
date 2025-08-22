# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.version
from spack.package import *


class RubyCast(RubyPackage):
    """C parser and AST constructor."""

    def build(pkg, spec, prefix):
        pkg.module.rake("gem:build")

    homepage = "http://github.com/oggy/cast"
    git = "http://github.com/oggy/cast.git"

    if Version(spack.spack_version) < Version("1.0"):
        version('0.3.1', tag='v0.3.1', get_full_repo=True)
    else:
        version('0.3.1', tag='v0.3.1', get_full_repo=True, commit='3c9b06093680781242dd72b04065ea62412daee1')

    depends_on('ruby@2.3.0:', type=('build', 'run'))
    depends_on('ruby-racc', type=('build', 'run'))
    depends_on('ruby-ritual', type=('build'))
    depends_on('ruby-rake', type=('build'))
    depends_on('re2c', type=('build'))

    patch('fix_import.patch')
    patch('fix_race_condition.patch')
