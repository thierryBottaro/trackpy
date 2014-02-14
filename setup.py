# This downloads and install setuptools if it is not installed.
from ez_setup import use_setuptools
use_setuptools()

import os
import sys
import warnings

# try bootstrapping setuptools if it doesn't exist
try:
    import pkg_resources
    try:
        pkg_resources.require("setuptools>=0.6c5")
    except pkg_resources.VersionConflict:
        from ez_setup import use_setuptools
        use_setuptools(version="0.6c5")
    from setuptools import setup, Extension
    _have_setuptools = True
except ImportError:
    # no setuptools installed
    from numpy.distutils.core import setup
    _have_setuptools = False

MAJOR = 0
MINOR = 2
MICRO = 0
ISRELEASED = False 
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
QUALIFIER = ''

FULLVERSION = VERSION
print FULLVERSION

if not ISRELEASED:
    import subprocess
    FULLVERSION += '.dev'
    
    pipe = None
    for cmd in ['git', 'git.cmd']:
        try:
            pipe = subprocess.Popen([cmd, "describe", "--always",
                                     "--match", "v[0-9\/]*"],
                                    stdout=subprocess.PIPE)
            (so, serr) = pip.communicate()
            if pipe.returncode == 0:
                break
        except:
            pass
        if pipe is None or pipe.returncode != 0:
            warnings.warn("WARNING: Couldn't get git revision, "
                          "using generic version string")
        else:
            rev = so.strip()
            # makes distutils blow up on Python 2.7
            if sys.version_info[0] >= 3:
                rev = rev.decode('ascii')

            # use result of git describe as version string
            FULLVERSION = rev.lstrip('v')

else:
    FULLVERSION += QUALIFIER

def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'
"""
    if not filename:
        filename = os.path.join(
            os.path.dirname(__file__), 'trackpy', 'version.py')

    a = open(filename, 'w')
    try:
        a.write(cnt % (FULLVERSION, VERSION))
    finally:
        a.close()

write_version_py()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# In some cases, the numpy include path is not present by default.
# Let's try to obtain it.
try:
    import numpy
except ImportError:
    ext_include_dirs = []
else:
    ext_include_dirs = [numpy.get_include(),]

setup_parameters = dict(
    name = "trackpy",
    version = FULLVERSION,
    description = "particle-tracking toolkit",
    author = "Daniel Allan and Thomas Caswell",
    author_email = "dallan@pha.jhu.edu",
    url = "https://github.com/soft-matter/trackpy",
    install_requires = ['numpy', 'scipy', 'six', 'pandas'],
    packages = ['trackpy'],
    long_description = read('README.md'),
)

setup(**setup_parameters)
