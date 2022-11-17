# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RubyOpencl(RubyPackage):
    """Ruby OpenCL FFI bindings. OpenCL 3.0 ready"""

    homepage = "https://github.com/Nanosim-LIG/opencl-ruby"
    url      = "https://rubygems.org/downloads/opencl_ruby_ffi-1.3.12.gem"

    version('1.3.12', sha256='e177a50112ab3b9379277943b3112110f52ac32eb2f039c2796b5e11762308ce', expand=False)

    depends_on('ruby', type=('build', 'run'))
    depends_on('ruby-narray-old', type=('build', 'run'))
    depends_on('ruby-ffi', type=('build', 'run'))
    depends_on('ruby-narray-ffi', type=('build', 'run'))
