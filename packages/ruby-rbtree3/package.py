# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class RubyRbtree3(RubyPackage):
    """A sorted associative collection backed by a red-black tree, written in C.
    It maps keys to values like a Hash but keeps them in ascending key order,
    and adds lower_bound, upper_bound and bound to search that order. Maintained
    fork of the unmaintained rbtree gem."""

    homepage = "https://github.com/kyrylo/rbtree3"
    url = "https://rubygems.org/downloads/rbtree3-1.1.0.gem"
    list_url = "https://rubygems.org/gems/rbtree3/versions"
    list_depth = 1

    version(
        "1.1.0",
        sha256="457586f9d498d4f78f8a5701be24145754b8c106435e1000eff2e166e34062a6",
        expand=False,
    )

    depends_on("ruby@3.0:", type=("build", "run"))
    depends_on("gmake", type="build")
