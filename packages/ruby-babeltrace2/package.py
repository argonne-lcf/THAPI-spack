# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyBabeltrace2(RubyPackage):
    """Ruby libbabeltrace2 ffi bindings"""

    homepage = "https://github.com/argonne-lcf/babeltrace2-ruby"
    url      = "https://rubygems.org/downloads/babeltrace2-0.1.1.gem"

    version('0.1.1', sha256='2a5c35a72ded62240230dd5b31eb7f2e6cdeabc5b29685a0b636c73c17a6c30c', expand=False)

    depends_on('ruby@2.3.0:', type=('build', 'run'))
    depends_on('ruby-ffi', type=('build', 'run'))
    depends_on('babeltrace2@2.0.4:', type=('run'))

    def setup_run_environment(self, env):
        super().setup_run_environment(env)
        env.prepend_path('LD_LIBRARY_PATH', self.spec['babeltrace2'].prefix.lib)

    def setup_dependent_build_environment(self, env, dependent_spec):
        super().setup_dependent_build_environment(env, dependent_spec)
        env.prepend_path('LD_LIBRARY_PATH', self.spec['babeltrace2'].prefix.lib)
