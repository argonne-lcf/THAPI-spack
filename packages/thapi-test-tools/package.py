# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.version
from spack.package import *


class ThapiTestTools(BundlePackage):
    """Dev and test tools required for THAPI development and testing."""

    version("develop")

    depends_on("bats")
    depends_on("clinfo")
    depends_on("jq")
    depends_on("ittapi")
    depends_on("py-ittapi")
