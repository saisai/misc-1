"""
This module was created in an attempt to improve conda's offline behavior.
It contains functionality for creating (and updating) a local channel (located
in `~/.conda/offline/`) from the package cache (`<root>/pkgs`).
It should be noted that the package cache is NOT a channel (it was never
designed to be a channel).
The idea is that when using conda in offline mode, this local channel is
first updated, and the used (instead of the http:// channels).
This means that NONE of the existing functionality for resolving, downloading,
extracting, and linking packages is going to have to change.
"""
from __future__ import print_function, division, absolute_import

import os
import re
import sys
import bz2
import json
import shutil
from collections import defaultdict
from os.path import abspath, expanduser, isdir, join, getsize

from conda import config
from conda.utils import md5_file
from conda.compat import iteritems


pkgs_dir = config.pkgs_dirs[0]
repo_path = join(pkgs_dirs, 'offline', config.subdir)
crd = defaultdict(list) # cached repo data - maps fn to list of info


def crd_append(path):
    d = json.load(open(path))
    for fn, info in iteritems(d.get('packages', {})):
        crd[fn].append(info)

def read_cached_repodata(): # populates 'crd'
    dir_path = join(pkgs_dir, 'cache')
    pat = re.compile(r'[0-9a-f]{8}\.json$')
    for fn in os.listdir(dir_path):
        if pat.match(fn):
            crd_append(join(dir_path, fn))
            sys.stdout.write('.')
            sys.stdout.flush()
    print()

def read_index():
    try:
        d = json.load(open(join(repo_path, 'repodata.json')))
        return d['packages']
    except IOError:
        return {}

def write_index(index):
    repodata = {'packages': index}
    data = json.dumps(repodata, indent=2, sort_keys=True)
    with open(join(repo_path, 'repodata.json'), 'w') as fo:
        fo.write(data)
    with open(join(repo_path, 'repodata.json.bz2'), 'wb') as fo:
        fo.write(bz2.compress(data.encode('utf-8')))

def iter_dir(path):
    for fn in os.listdir(path):
        if fn.endswith('.tar.bz2'):
            yield fn

def find_info(fn):
    if fn not in crd:
        return None
    md5 = md5_file(join(pkgs_dir, fn))
    for info in crd[fn]:
        if md5 == info.get('md5'):
            return info
    return None

def update_repo():
    if not isdir(repo_path):
        os.makedirs(repo_path)
    index = read_index()
    read_cached_repodata()
    for fn in iter_dir(pkgs_dir):
        if fn in index:
            continue
        info = find_info(fn)
        if info:
            sys.stdout.write('.')
            sys.stdout.flush()
            shutil.copyfile(join(pkgs_dir, fn), join(repo_path, fn))
            index[fn] = info

    write_index(index)
    print()

def test_repo():
    index = read_index()
    files = set()
    for fn in iter_dir(repo_path):
        files.add(fn)
        info = index[fn]
        path = join(repo_path, fn)
        assert '%(name)s-%(version)s-%(build)s.tar.bz2' % info == fn
        assert getsize(path) == info['size']
        assert md5_file(path) == info['md5']

    assert files == set(index)


if __name__ == '__main__':
    update_repo()
    test_repo()
