# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyRacc(RubyPackage):
    """ Racc is an LALR(1) parser generator. 
        It is written in Ruby itself, and generates Ruby program."""

    homepage = "https://rubygems.org/gems/racc"
    url      = "https://rubygems.org/downloads/racc-1.8.1.gem"

    version('1.8.1', sha256='54f2e6d1e1b91c154013277d986f52a90e5ececbe91465d29172e49342732b98', expand=False)

    depends_on('ruby@2.5.0:', type=('build', 'run'))
