# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyNokogiri(RubyPackage):
    """Nokogiri (鋸) makes it easy and painless to work with XML and HTML from
       Ruby. It provides a sensible, easy-to-understand API for reading,
       writing, modifying, and querying documents. It isfast and
       standards-compliant by relying on native parsers like libxml2 (C) and
       xerces (Java)."""

    homepage = "https://nokogiri.org"
    url      = "https://rubygems.org/downloads/nokogiri-1.12.5.gem"

    version('1.12.5', sha256='2b20905942acc580697c8c496d0d1672ab617facb9d30d156b3c7676e67902ec', expand=False)

    depends_on('ruby@2.5.0:', type=('build', 'run'))
    depends_on('ruby-rake@13.0.0:', type=('build'))
    depends_on('ruby-mini-portile2@2.6.1', type=('build', 'run'))
