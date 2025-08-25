# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyNokogiri(RubyPackage):
    """Nokogiri (鋸) makes it easy and painless to work with XML and HTML from
       Ruby. It provides a sensible, easy-to-understand API for reading,
       writing, modifying, and querying documents. It isfast and
       standards-compliant by relying on native parsers like libxml2 (C) and
       xerces (Java)."""

    homepage = "https://nokogiri.org"
    url      = "https://rubygems.org/downloads/nokogiri-1.12.5.gem"

    # fmt: off
    version('1.16.7', sha256='f819cbfdfb0a7b19c9c52c6f2ca63df0e58a6125f4f139707b586b9511d7fe95', expand=False)
    version('1.12.5', sha256='2b20905942acc580697c8c496d0d1672ab617facb9d30d156b3c7676e67902ec', expand=False)
    # fmt: on

    depends_on('ruby-racc@1.4.0:', type=('build','run'))

    with when('@1.12.5'):
       depends_on('ruby@2.5.0:2.7.999', type=('build', 'run'))
       depends_on('ruby-mini-portile2@2.6.1:2.7.0', type=('build', 'run'))

    with when('@1.16.7'):
       depends_on('ruby@3.0.0:', type=('build', 'run'))
       depends_on('ruby-mini-portile2@2.8.2:2.9.0', type=('build', 'run'))
