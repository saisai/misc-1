import os
import re
import sys
import json
import shutil
from collections import defaultdict
from os.path import isdir, isfile, join, getsize

from conda import config


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
    size = getsize(join(pkgs_dir, fn))
    for info in crd[fn]:
        if info.get('size') == size:
            assert '%(name)s-%(version)s-%(build)s.tar.bz2' % info == fn, fn
            return info
    return None

def create_new_index():
    read_cached_repodata()
    index = {}
    for fn in os.listdir(pkgs_dir):
        if not fn.endswith('.tar.bz2'):
            continue
        info = find_info(fn)
        if info:
            index[fn] = info
    return index

def create_repo():
    if not isdir(repo_path):
        os.makedirs(repo_path)
    index = create_new_index()
    for fn, info in index.iteritems():
        dst = join(repo_path, fn)
        if isfile(dst) and getsize(dst) == info.get('size'):
            continue
        sys.stdout.write('.')
        sys.stdout.flush()
        src = join(pkgs_dir, fn)
        shutil.copyfile(src, dst)
    repodata = {'packages': index}
    with open(repodata_path, 'w') as fo:
        json.dump(repodata, fo, indent=2, sort_keys=True)
    print

if __name__ == '__main__':
    create_repo()
