# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Thapi(AutotoolsPackage):
    """A tracing infrastructure for heterogeneous computing applications."""

    homepage = "https://github.com/argonne-lcf/THAPI"
    git      = "https://github.com/argonne-lcf/THAPI.git"

    version('master', branch='master', preferred=True)
    version('0.0.12', tag='v0.0.12')
    version('0.0.11', tag='v0.0.11')
    version('0.0.10', tag='v0.0.10')
    version('0.0.9', tag='v0.0.9')
    version('0.0.8', tag='v0.0.8')
    version('0.0.7', tag='v0.0.7')

    depends_on('automake', type=('build'))
    depends_on('autoconf', type=('build'))
    depends_on('libtool', type=('build'))
    depends_on('pkgconfig')
    # 4.3+ for grouped target 
    depends_on('gmake@4.3:', type=('build'))
    depends_on('babeltrace2', type=('build', 'link', 'run'))
    depends_on('protobuf@3.12.4:', type=('build', 'link', 'run'))
    depends_on('lttng-ust', type=('build', 'link', 'run'), when='@0.0.8:')
    depends_on('lttng-tools', type=('build', 'link', 'run'), when='@0.0.8:')
    depends_on('lttng-ust@:2.12.999', type=('build', 'link', 'run'), when='@:0.0.7')
    depends_on('lttng-tools@:2.12.999', type=('build', 'link', 'run'), when='@:0.0.7')

    # Restricting to ruby <= 3.1 when spack is less than 0.23
    if spack.version.Version(spack.spack_version) < spack.version.Version("0.23"):
        depends_on('ruby@2.7.0:3.1', type=('build', 'run'))
    else:
        depends_on('ruby@2.7.0:', type=('build', 'run'))

    depends_on('ruby-babeltrace2', type=('build', 'run'))
    depends_on('ruby-opencl', type=('build', 'run'))
    depends_on('ruby-nokogiri', type=('build'))
    depends_on('ruby-cast-to-yaml', type=('build'))
    depends_on('ruby-metababel@0.1.0:0.9', type=('build'), when='@:0.0.10')
    depends_on('ruby-metababel@1.0.0:', type=('build'), when='@0.0.11')
    depends_on('ruby-metababel@1.1.2:', type=('build'), when='@0.0.12:')

    depends_on('libiberty+pic')
    depends_on('libffi')
    depends_on('mpi', when='+mpi')
    # We add a Python dependency at buildtime, because `lttng-gen-tp` needs it.
    # We don't add Python as a runtime dependency of lttng to avoid python propagated as a runtime dependency of thapi
    depends_on('python', type=('build'))

    variant('strict', default=False, description='Enable -Werror during the build')    
    variant('mpi', default=False, description='Enable MPI support for the Sync Daemon')

    patch('0001-Ignore-int-conversions.patch', when='@0.0.8:0.0.11')
    def configure_args(self):
        args = [] 
        args.extend(self.enable_or_disable('mpi'))
        args.extend(self.enable_or_disable('strict'))
        return args
