# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyFfi(RubyPackage):
    """Ruby-FFI is a gem for programmatically loading dynamically-linked native
    libraries, binding functions within them, and calling those functions
    from Ruby code."""

    homepage = "https://github.com/ffi/ffi/wiki"
    url = "https://rubygems.org/downloads/ffi-1.15.4.gem"

    version("1.15.4", sha256="56cfca5261ead48688241236adfefb07a000a6d17184d7a4eed48d55b9675d6b", expand=False)

    depends_on("ruby@2.3.0:", type=("build", "run"))
