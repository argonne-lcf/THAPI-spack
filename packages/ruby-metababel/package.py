# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyMetababel(RubyPackage):
    """YAML to Babeltrace 2 Component compiler-compiler"""

    homepage = "https://github.com/TApplencourt/metababel"
    url      = "https://rubygems.org/downloads/metababel-0.0.0.gem"

    version('0.0.0', sha256='9af39e0af353d9ff9c74f301b0a8fea409b784ded622a9e30d387b1cb233d50a', expand=False)
    version('0.0.1', sha256='3d7a515faea00d4e8b7fc6b01c57b6d8ef6b5135dfd7361f5717a19bc12e6475', expand=False)
    version('0.0.2', sha256='920d2157e8b5586455c211b88470441ac9a361fe84481abe184732e299a3c701', expand=False)
    version('0.0.3', sha256='9f880cf6d463ced9d4c0966ae16bfa6eb330df373adc7b7e0dd182e8345befcd', expand=False)
    depends_on('ruby@2.7.0:', type=('build', 'run'))
