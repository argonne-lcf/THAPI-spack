# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubyBabeltrace2(RubyPackage):
    """Ruby libbabeltrace2 ffi bindings"""

    homepage = "https://github.com/argonne-lcf/babeltrace2-ruby"
    url      = "https://rubygems.org/downloads/babeltrace2-0.1.1.gem"

    # fmt: off
    version('0.1.5', sha256='9b8f7d14ad333be568cf4be1a52573af77f3047200c11f1c05d85b85ffd86a6d', expand=False)
    version('0.1.4', sha256='7d45e79f18ec2c9e24fc303924d48bd375667f06748eec83d60f7cc3b4ca4db2', expand=False)
    version('0.1.3', sha256='549cbd03c6e4987cb935ee20ca69887f8fd6bd5d2e6d9fca0706b63d966fca5c', expand=False)
    version('0.1.2', sha256='a09696933a5d36b2833bd6e3bda5b3981d9719ee77c71a5542ccc127e02b27c3', expand=False)
    version('0.1.1', sha256='2a5c35a72ded62240230dd5b31eb7f2e6cdeabc5b29685a0b636c73c17a6c30c', expand=False)
    # fmt: on

    depends_on('ruby@2.3.0:', type=('build', 'run'))
    depends_on('ruby-ffi', type=('build', 'run'))
    depends_on('babeltrace2@2.0.4:', type=('run'))

    def setup_run_environment(self, env):
        super().setup_run_environment(env)
        env.prepend_path('LD_LIBRARY_PATH', self.spec['babeltrace2'].prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        super().setup_dependent_build_environment(env, dependent_spec)
        env.prepend_path('LD_LIBRARY_PATH', self.spec['babeltrace2'].prefix.lib)
