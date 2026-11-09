# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RubyNarrayOld(RubyPackage):
    """Numerical N-dimensional Array class"""

    homepage = "http://masa16.github.io/narray/"
    url = "https://rubygems.org/downloads/narray-0.6.1.2.gem"

    version("0.6.1.2", sha256="73bf101929a1570e8034058e1296fec58d6c3386c26bf26810d33f70dd4236b7", expand=False)

    depends_on("ruby", type=("build", "run"))
    # Native extension: gem builds via make. Declaring gmake lets Spack detect the
    # concrete make version and pick a jobserver protocol it understands.
    depends_on("gmake", type="build")

    def setup_build_environment(self, env):
        # narray 0.6 declares its function-pointer tables with K&R-style empty
        # parameter lists (`void (*f)()`). Under C23, the default since GCC 15,
        # `()` means "no arguments" and every call through those tables fails.
        # The gem is built by mkmf, which reads extconf options from
        # CONFIGURE_ARGS; keep Ruby's own cflags and pin the older standard.
        env.set("CONFIGURE_ARGS", "--with-cflags='$(cflags) -std=gnu17'")
