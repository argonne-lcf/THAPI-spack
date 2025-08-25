# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyCastToYaml(RubyPackage):
    """Extract information fom a C ast"""

    homepage = "https://github.com/argonne-lcf/cast-to-yaml"
    url = "https://rubygems.org/downloads/cast-to-yaml-0.1.1.gem"

    version("0.1.1", sha256="d741f258015dd526869a96a3e14442ac58484585fc5d8727d7ffeee109927756", expand=False)

    depends_on("ruby@2.3.0:", type=("build", "run"))
    depends_on("ruby-cast", type=("build", "run"))
