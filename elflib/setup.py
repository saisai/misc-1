import re
from os.path import abspath
from distutils.core import setup


kwds = {}

# Read the long description from README
kwds['long_description'] = open(abspath('README')).read()

d = {}
execfile(abspath('elflib/__init__.py'), d)
kwds['version'] = d['__version__']


setup(
    name = "elflib",
    author = "Ilan Schnell",
    author_email = "ilanschnell@gmail.com",
    url = "http://pypi.python.org/pypi/elflib/",
    license = "PSF",
    classifiers = [
        "License :: OSI Approved :: Python Software Foundation License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ],
    description = "library for working with ELF files",
    packages = ["elflib"],
    **kwds
)
