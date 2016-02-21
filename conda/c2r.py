import os
import re
import sys
import json
import shutil
from collections import defaultdict
from os.path import isdir, isfile, join, getsize
from pprint import pprint

from conda import config
from conda.utils import md5_file


pkgs_dir = config.pkgs_dirs[0]
cache_dir = join(pkgs_dir, 'cache')
crd = defaultdict(list) # cached repo data - maps fn to list of info
repo_path = join('repo', config.subdir)
repodata_path = join(repo_path, 'repodata.json')


def crd_append(path):
    d = json.load(open(path))
    for fn, info in d.get('packages', {}).iteritems():
        crd[fn].append(info)

def read_cached_repodata(): # populates 'crd'
    pat = re.compile(r'[0-9a-f]{8}\.json$')
    for fn in os.listdir(cache_dir):
        if pat.match(fn):
            crd_append(join(cache_dir, fn))
            sys.stdout.write('.')
            sys.stdout.flush()
    print

def find_info(fn):
    if fn not in crd:
        return None
    path = join(pkgs_dir, fn)
    md5 = md5_file(path)
    for info in crd[fn]:
        if md5 == info.get('md5'):
            return info
    return None

def create_repo():
    if not isdir(repo_path):
        os.makedirs(repo_path)
    try:
        d = json.load(open(repodata_path))
        index = d['packages']
    except IOError:
        index = {}
    read_cached_repodata()
    for fn in os.listdir(pkgs_dir):
        if not fn.endswith('.tar.bz2') or fn in index:
            continue
        info = find_info(fn)
        if not info:
            continue
        sys.stdout.write('.')
        sys.stdout.flush()
        shutil.copyfile(join(pkgs_dir, fn),
                        join(repo_path, fn))
        index[fn] = info

    repodata = {'packages': index}
    with open(repodata_path, 'w') as fo:
        json.dump(repodata, fo, indent=2, sort_keys=True)
    print

def test_repo():
    d = json.load(open(repodata_path))
    index = d['packages']
    files = set()
    for fn in os.listdir(repo_path):
        if not fn.endswith('.tar.bz2'):
            continue
        files.add(fn)
        info = index[fn]
        path = join(repo_path, fn)
        assert '%(name)s-%(version)s-%(build)s.tar.bz2' % info == fn
        assert getsize(path) == info['size']
        assert md5_file(path) == info['md5']

    assert files == set(index)


if __name__ == '__main__':
    create_repo()
    test_repo()
