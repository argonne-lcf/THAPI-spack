# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyRacc(RubyPackage):
    """Racc is an LALR(1) parser generator.
    It is written in Ruby itself, and generates Ruby program."""

    homepage = "https://rubygems.org/gems/racc"
    url = "https://rubygems.org/downloads/racc-1.8.1.gem"

    version("1.8.1", sha256="4a7f6929691dbec8b5209a0b373bc2614882b55fc5d2e447a21aaa691303d62f", expand=False)

    depends_on("ruby@2.5.0:", type=("build", "run"))
