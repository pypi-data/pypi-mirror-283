import sys
import os
import os.path as op
import time
import shutil
import tempfile

from pkg_resources import parse_version as pv
from setuptools import setup, Extension, __version__ as setuptools_version
from setuptools.command.build_py import build_py
from setuptools.command.build_ext import build_ext

is_windows = sys.platform.startswith('win')

have_pep621_support = pv(setuptools_version) >= pv('61.0.0')

packname = 'pyrockoeost'
version = '2024.3'


def get_numpy_include():
    import numpy
    return numpy.get_include()


class NotInAGitRepos(Exception):
    pass


def git_infos():
    '''Query git about sha1 of last commit and check if there are local \
       modifications.'''

    from subprocess import run, PIPE
    import re

    def q(c):
        return run(c, stdout=PIPE, stderr=PIPE, check=True).stdout

    if not op.exists('.git'):
        raise NotInAGitRepos()

    sha1 = q(['git', 'log', '--pretty=oneline', '-n1']).split()[0]
    sha1 = re.sub(br'[^0-9a-f]', '', sha1)
    sha1 = str(sha1.decode('ascii'))
    sstatus = q(['git', 'status', '--porcelain', '-uno'])
    local_modifications = bool(sstatus.strip())
    return sha1, local_modifications


def print_e(*args):
    print(*args, file=sys.stderr)


def make_info_module(packname, version):
    '''Put version and revision information into file src/info.py.'''

    from subprocess import CalledProcessError

    sha1, local_modifications = None, None
    combi = '%s-%s' % (packname, version)
    try:
        sha1, local_modifications = git_infos()
        combi += '-%s' % sha1
        if local_modifications:
            combi += '-modified'

    except (OSError, CalledProcessError, NotInAGitRepos):
        print_e('Failed to include git commit ID into installation.')

    datestr = time.strftime('%Y-%m-%d_%H:%M:%S')
    combi += '-%s' % datestr

    s = '''# This module is automatically created from setup.py
git_sha1 = %s
local_modifications = %s
version = %s
long_version = %s  # noqa
installed_date = %s
src_path = %s
''' % tuple([repr(x) for x in (
        sha1, local_modifications, version, combi, datestr,
        op.dirname(op.abspath(__file__)))])

    info_path = op.join('src', 'info.py')
    if os.path.exists(info_path):
        # remove file for the case we are running as normal user but root-owned
        # file from a previous run is in src.
        os.unlink(info_path)

    f = open(info_path, 'w')
    f.write(s)
    f.close()


libmseed_sources = [op.join('libmseed', entry) for entry in [
    'fileutils.c', 'genutils.c', 'gswap.c', 'lmplatform.c',
    'logging.c', 'lookup.c', 'msrutils.c', 'pack.c', 'packdata.c',
    'parseutils.c', 'selection.c', 'tracelist.c', 'traceutils.c',
    'unpack.c', 'unpackdata.c']]


def make_prerequisites():
    from subprocess import check_call

    if is_windows:
        cmd = ['prerequisites\\prerequisites.bat']
    else:
        cmd = ['sh', 'prerequisites/prerequisites.sh']

    try:
        check_call(cmd)
    except Exception:
        sys.exit('error: failed to build the included prerequisites with '
                 '"%s"' % ' '.join(cmd))


def get_build_include(lib_name):
    return op.join(op.dirname(op.abspath(__file__)), lib_name)


class CustomBuildPyCommand(build_py):

    def make_compat_modules(self):
        mapping = [
            ('pyrockoeost', 'css', ['pyrockoeost.io.css']),
            ('pyrockoeost', 'datacube', ['pyrockoeost.io.datacube']),
            ('pyrockoeost.fdsn', '__init__', []),
            ('pyrockoeost.fdsn', 'enhanced_sacpz', ['pyrockoeost.io.enhanced_sacpz']),
            ('pyrockoeost.fdsn', 'station', ['pyrockoeost.io.stationxml']),
            ('pyrockoeost', 'gcf', ['pyrockoeost.io.gcf']),
            ('pyrockoeost', 'gse1', ['pyrockoeost.io.gse1']),
            ('pyrockoeost', 'gse2_io_wrap', ['pyrockoeost.io.gse2']),
            ('pyrockoeost', 'ims', ['pyrockoeost.io.ims']),
            ('pyrockoeost', 'io_common', ['pyrockoeost.io.io_common']),
            ('pyrockoeost', 'kan', ['pyrockoeost.io.kan']),
            ('pyrockoeost', 'mseed', ['pyrockoeost.io.mseed']),
            ('pyrockoeost', 'rdseed', ['pyrockoeost.io.rdseed']),
            ('pyrockoeost.fdsn', 'resp', ['pyrockoeost.io.resp']),
            ('pyrockoeost', 'sacio', ['pyrockoeost.io.sac']),
            ('pyrockoeost', 'segy', ['pyrockoeost.io.segy']),
            ('pyrockoeost', 'seisan_response', ['pyrockoeost.io.seisan_response']),
            ('pyrockoeost', 'seisan_waveform', ['pyrockoeost.io.seisan_waveform']),
            ('pyrockoeost', 'suds', ['pyrockoeost.io.suds']),
            ('pyrockoeost', 'yaff', ['pyrockoeost.io.yaff']),
            ('pyrockoeost', 'eventdata', ['pyrockoeost.io.eventdata']),
            ('pyrockoeost.fdsn', 'ws', ['pyrockoeost.client.fdsn']),
            ('pyrockoeost', 'catalog', ['pyrockoeost.client.catalog']),
            ('pyrockoeost', 'iris_ws', ['pyrockoeost.client.iris']),
            ('pyrockoeost', 'crust2x2', ['pyrockoeost.dataset.crust2x2']),
            ('pyrockoeost', 'crustdb', ['pyrockoeost.dataset.crustdb']),
            ('pyrockoeost', 'geonames', ['pyrockoeost.dataset.geonames']),
            ('pyrockoeost', 'tectonics', ['pyrockoeost.dataset.tectonics']),
            ('pyrockoeost', 'topo', ['pyrockoeost.dataset.topo']),
            ('pyrockoeost', 'automap', ['pyrockoeost.plot.automap']),
            ('pyrockoeost', 'beachball', ['pyrockoeost.plot.beachball']),
            ('pyrockoeost', 'cake_plot', ['pyrockoeost.plot.cake_plot']),
            ('pyrockoeost', 'gmtpy', ['pyrockoeost.plot.gmtpy']),
            ('pyrockoeost', 'hudson', ['pyrockoeost.plot.hudson']),
            ('pyrockoeost', 'response_plot', ['pyrockoeost.plot.response']),
            ('pyrockoeost', 'snuffling', ['pyrockoeost.gui.snuffler.snuffling']),
            ('pyrockoeost', 'pile_viewer', ['pyrockoeost.gui.snuffler.pile_viewer']),
            ('pyrockoeost', 'marker', ['pyrockoeost.gui.snuffler.marker']),
            ('pyrockoeost', 'snuffler', ['pyrockoeost.gui.snuffler.snuffler']),
            ('pyrockoeost', 'gui_util', ['pyrockoeost.gui.util']),
            ('pyrockoeost.gui', 'snuffling', ['pyrockoeost.gui.snuffler.snuffling']),
            ('pyrockoeost.gui', 'pile_viewer', [
                'pyrockoeost.gui.snuffler.pile_viewer']),
            ('pyrockoeost.gui', 'marker', ['pyrockoeost.gui.snuffler.marker']),
        ]

        for (package, compat_module, import_modules) in mapping:
            module_code = '''
import sys
import pyrockoeost
if pyrockoeost.grumpy == 1:
    sys.stderr.write('using renamed pyrockoeost module: %s.%s\\n')
    sys.stderr.write('           -> should now use: %s\\n\\n')
elif pyrockoeost.grumpy == 2:
    sys.stderr.write('pyrockoeost module has been renamed: %s.%s\\n')
    sys.stderr.write('              -> should now use: %s\\n\\n')
    raise ImportError('pyrockoeost module "%s.%s" has been renamed to "%s".')

''' % ((package, compat_module, ', '.join(import_modules))*3) + ''.join(
                ['from %s import *\n' % module for module in import_modules])

            outfile = self.get_module_outfile(
                self.build_lib, package.split('.'), compat_module)

            dir = os.path.dirname(outfile)
            self.mkpath(dir)
            with open(outfile, 'w') as f:
                f.write(module_code)

    def run(self):
        import numpy
        print_e('='*60)
        print_e('NumPy version used for build: %s' % numpy.__version__)
        print_e('='*60)
        make_info_module(packname, version)
        self.make_compat_modules()
        build_py.run(self)


class CustomBuildExtCommand(build_ext):
    def run(self):
        make_prerequisites()
        build_ext.run(self)


class CustomBuildAppCommand(build_ext):
    def run(self):
        self.make_app()

    def make_app(self):
        from setuptools import setup
        setup(
            app=['src/apps/snuffler.py'],
            options={
                'py2app': {
                    'argv_emulation': False,
                    'iconfile': 'src/data/snuffler.icns',
                    'packages': ['chardet'],
                    'excludes': ['test'],
                    'plist': {
                        'CFBundleDisplayName': 'Snuffler',
                        'CFBundleExecutable': 'Snuffler',
                        'CFBundleName': 'Snuffler',
                    },
                },
            },
            setup_requires=['py2app', 'chardet'],
        )


def _check_for_openmp():
    '''Check  whether the default compiler supports OpenMP.
    This routine is adapted from pynbody // yt.
    Thanks to Nathan Goldbaum and Andrew Pontzen.
    '''
    import distutils.sysconfig
    import subprocess

    tmpdir = tempfile.mkdtemp(prefix='pyrockoeost')
    try:
        compiler = os.environ.get(
            'CC', distutils.sysconfig.get_config_var('CC')).split()[0]
    except Exception:
        return False

    # Attempt to compile a test script.
    # See http://openmp.org/wp/openmp-compilers/
    tmpfile = op.join(tmpdir, 'check_openmp.c')
    with open(tmpfile, 'w') as f:
        f.write('''
#include <omp.h>
#include <stdio.h>
int main() {
    #pragma omp parallel
    printf("Hello from thread %d", omp_get_thread_num());
}
''')

    try:
        with open(os.devnull, 'w') as fnull:
            exit_code = subprocess.call([compiler, '-fopenmp', '-o%s'
                                         % op.join(tmpdir, 'check_openmp'),
                                        tmpfile],
                                        stdout=fnull, stderr=fnull)
    except OSError:
        exit_code = 1
    finally:
        shutil.rmtree(tmpdir)

    if exit_code == 0:
        print_e('Continuing your build using OpenMP...')
        return True

    import multiprocessing
    import platform
    if multiprocessing.cpu_count() > 1:
        print_e('''WARNING
OpenMP support is not available in your default C compiler, even though
your machine has more than one core available.
Some routines in pyrockoeost are parallelized using OpenMP and these will
only run on one core with your current configuration.
''')
        if platform.uname()[0] == 'Darwin':
            print_e('''
Since you are running on Mac OS, it's likely that the problem here
is Apple's Clang, which does not support OpenMP at all. The easiest
way to get around this is to download the latest version of gcc from
here: http://hpc.sourceforge.net. After downloading, just point the
CC environment variable to the real gcc and OpenMP support should
get enabled automatically. Something like this -
sudo tar -xzf /path/to/download.tar.gz /
export CC='/usr/local/bin/gcc'
python setup.py clean
python setup.py build
''')
    print_e('Continuing your build without OpenMP...')
    return False


if _check_for_openmp():
    omp_arg = ['-fopenmp']
    omp_lib = ['-lgomp']
else:
    omp_arg = []
    omp_lib = []


subpacknames = [
    'pyrockoeost.gf',
    'pyrockoeost.fomosto',
    'pyrockoeost.fomosto.report',
    'pyrockoeost.client',
    'pyrockoeost.apps',
    'pyrockoeost.io',
    'pyrockoeost.model',
    'pyrockoeost.modelling',
    'pyrockoeost.plot',
    'pyrockoeost.gui',
    'pyrockoeost.gui.snuffler',
    'pyrockoeost.gui.snuffler',
    'pyrockoeost.gui.snuffler.snufflings',
    'pyrockoeost.gui.snuffler.snufflings.map',
    'pyrockoeost.gui.sparrow',
    'pyrockoeost.gui.sparrow.elements',
    'pyrockoeost.gui.drum',
    'pyrockoeost.dataset',
    'pyrockoeost.dataset.topo',
    'pyrockoeost.streaming',
    'pyrockoeost.scenario',
    'pyrockoeost.scenario.targets',
    'pyrockoeost.scenario.sources',
    'pyrockoeost.obspy_compat',
    'pyrockoeost.squirrel',
    'pyrockoeost.squirrel.io',
    'pyrockoeost.squirrel.io.backends',
    'pyrockoeost.squirrel.client',
    'pyrockoeost.squirrel.tool',
    'pyrockoeost.squirrel.tool.commands',
    'pyrockoeost.squirrel.operators',
    'pyrockoeost.data',
    'pyrockoeost.data.colortables',
    'pyrockoeost.data.earthmodels',
    'pyrockoeost.data.tectonics',
    'pyrockoeost.data.fomosto_report',
]

cmdclass = {
    'build_py': CustomBuildPyCommand,
    'py2app': CustomBuildAppCommand,
    'build_ext': CustomBuildExtCommand}


if is_windows:
    extra_compile_args = []
else:
    extra_compile_args = ['-Wextra']

ext_modules = [
    Extension(
        'datacube_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args,
        sources=[op.join('src', 'io', 'ext', 'datacube_ext.c')]),

    Extension(
        'signal_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args,
        sources=[op.join('src', 'ext', 'signal_ext.c')]),

    Extension(
        'mseed_ext',
        include_dirs=[get_numpy_include(),
                      get_build_include('libmseed')],
        extra_compile_args=extra_compile_args + (
            ['-D_CRT_SECURE_NO_WARNINGS', '-DWIN32'] if
            is_windows else ['-fno-strict-aliasing']),
        sources=[
            op.join('src', 'io', 'ext', 'mseed_ext.c')] + libmseed_sources),

    Extension(
        'ims_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args,
        sources=[op.join('src', 'io', 'ext', 'ims_ext.c')]),

    Extension(
        'avl',
        sources=[op.join('src', 'ext', 'pyavl-1.12', 'avl.c'),
                 op.join('src', 'ext', 'pyavl-1.12', 'avlmodule.c')],
        define_macros=[('HAVE_AVL_VERIFY', None),
                       ('AVL_FOR_PYTHON', None)],
        extra_compile_args=['-Wno-parentheses', '-Wno-uninitialized']
        if not is_windows else [],
        extra_link_args=[] if sys.platform != 'sunos5' else ['-Wl,-x']),

    Extension(
        'eikonal_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args + omp_arg,
        extra_link_args=[] + omp_lib,
        sources=[op.join('src', 'ext', 'eikonal_ext.c')]),

    Extension(
        'orthodrome_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args,
        sources=[op.join('src', 'ext', 'orthodrome_ext.c')]),

    Extension(
        'parstack_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args + omp_arg,
        extra_link_args=[] + omp_lib,
        sources=[op.join('src', 'ext', 'parstack_ext.c')]),

    Extension(
        'autopick_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args,
        sources=[op.join('src', 'ext', 'autopick_ext.c')]),

    Extension(
        'gf.store_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args
        + ['-D_FILE_OFFSET_BITS=64'] + omp_arg,
        extra_link_args=[] + omp_lib,
        sources=[op.join('src', 'gf', 'ext', 'store_ext.c')]),

    Extension(
        'ahfullgreen_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args,
        sources=[op.join('src', 'ext', 'ahfullgreen_ext.c')]),

    Extension(
        'modelling.okada_ext',
        include_dirs=[get_numpy_include()],
        extra_compile_args=extra_compile_args + omp_arg,
        extra_link_args=[] + omp_lib,
        sources=[op.join('src', 'modelling', 'ext', 'okada_ext.c')])]


ext_modules_non_windows = [
    Extension(
        'util_ext',
        extra_compile_args=extra_compile_args,
        sources=[op.join('src', 'ext', 'util_ext.c')]),

    Extension(
        'evalresp_ext',
        include_dirs=[get_numpy_include(),
                      get_build_include('evalresp-3.3.0/include/')],
        library_dirs=[get_build_include('evalresp-3.3.0/lib/')],
        libraries=['evresp'],
        extra_compile_args=extra_compile_args + [
            '-I%s' % get_build_include('evalresp-3.3.0/include')],
        sources=[op.join('src', 'ext', 'evalresp_ext.c')])]

if not is_windows:
    ext_modules.extend(ext_modules_non_windows)


if not have_pep621_support:
    metadata = dict(
        description='A versatile seismology toolkit for Python. EOST VERSION',
        long_description=open(
            'maintenance/readme-pip.rst', 'rb').read().decode('utf8'),
        author='The pyrockoeost Developers',
        author_email='info@pyrocko.org',
        url='https://pyrocko.org',
        license='GPLv3',
        classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: C',
            'Programming Language :: Python :: Implementation :: CPython',
            'Operating System :: POSIX',
            'Operating System :: MacOS',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Physics',
            'Topic :: Scientific/Engineering :: Visualization',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Software Development :: Libraries :: Application '
            'Frameworks'],
        keywords=[
            'seismology, waveform analysis, earthquake modelling, geophysics,'
            ' geophysical inversion'],
        python_requires='>=3.7, <4',
        install_requires=[
            'numpy==1.26.4',
            'scipy>=1.0',
            'pyyaml==6.0.1',
            'matplotlib<3.9',
            'requests==2.32.3',
            'PyQt5==5.15.10',
            'PyQtWebEngine==5.15.6',
            'vtk==9.3.1',
        ],

        # extras_require={
        #     'gui_scripts': ['PyQt5', 'PyQtWebEngine', 'vtk'],
        # },

        entry_points={
            'console_scripts':
                ['pyrockoeost = pyrockoeost.apps.pyrockoeost:main',
                 'fomosto = pyrockoeost.apps.fomosto:main',
                 'cake = pyrockoeost.apps.cake:main',
                 'automap = pyrockoeost.apps.automap:main',
                 'hamster = pyrockoeost.apps.hamster:main',
                 'jackseis = pyrockoeost.apps.jackseis:main',
                 'colosseo = pyrockoeost.apps.colosseo:main',
                 'squirrel = pyrockoeost.apps.squirrel:main'],
            'gui_scripts':
                ['snuffler = pyrockoeost.apps.snuffler:main',
                 'sparrow = pyrockoeost.apps.sparrow:main',
                 'drum = pyrockoeost.apps.drum:main'],
        },
    )

else:
    metadata = {}

setup(
    cmdclass=cmdclass,
    name=packname,
    version=version,
    packages=[packname] + subpacknames,
    package_dir={'pyrockoeost': 'src'},
    ext_package=packname,
    ext_modules=ext_modules,
    scripts=['src/apps/gmtpy-epstopdf'],
    include_package_data=False,
    package_data={
        packname: [
            'data/*.png',
            'data/*.html',
            'data/earthmodels/*.nd',
            'data/colortables/*.cpt',
            'data/tectonics/*.txt',
            'data/fomosto_report/gfreport.*',
            'gui/snuffler/snufflings/map/*.kml',
            'gui/snuffler/snufflings/map/*.html',
            'gui/snuffler/snufflings/map/*.js'],
        '': ['README.md', 'windows-install-compiler.bat']},
    **metadata,
)
