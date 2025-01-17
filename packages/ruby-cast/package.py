# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyCast(RubyPackage):
    """C parser and AST constructor."""

    def build(pkg, spec, prefix):
        pkg.module.rake("gem:build")

    homepage = "http://github.com/oggy/cast"
    git = "http://github.com/oggy/cast.git"

    version('0.3.1', tag='v0.3.1', get_full_repo=True)

    depends_on('ruby@2.3.0:', type=('build', 'run'))
    depends_on('ruby-racc', type=('build', 'run'))
    depends_on('ruby-ritual', type=('build'))
    depends_on('ruby-rake', type=('build'))
    depends_on('re2c', type=('build'))

    patch('fix_import.patch')
    patch('fix_race_condition.patch')
