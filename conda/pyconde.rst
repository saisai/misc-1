Conda packaging
===============

(Lightning Talk, PyCon DE 2013 Köln)
------------------------------------

ANACONDA:
---------
  * freie Python Distribution
  * für Linux, MacOSX, Windows
  * supports Python 2.6, 2.7 and 3.3
  * Python, NumPy, SciPy, matplotlib, Qt, Erlang, HDF5, ...
  * maintained by Continuum Analytics

Conda:
------
  * open source package management tool
  * platform agnostic
  * packages are tarballs
  * meta-data is stored in a json file
  * Python agnostic!!!
  * allows multiple environments (using hard links)
  * uses SAT solver (PicoSAT) for dependency resolution
  * allows building packages using "conda recipes"

Conda recipe:
-------------
  * for conda what a .spec file is for rpm
  * a single (usually flat) directory
  * has a meta-data file
  * build scripts
  * patches (if any)
  * tests

binstar.org:
------------
  * free package hosting
  * user accounts
  * different package formats:
      - conda
      - rpm
      - PyPI

Goals for this sprint:
----------------------
  * enable YOU to build conda packages and upload them to binstar.org
  * get your feedback on usability of the tools
  * create conda-recipes
