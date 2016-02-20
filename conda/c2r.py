import os
import sys
import json
from collections import defaultdict
from os.path import join, getsize
from pprint import pprint

from conda import config



pkgs_dir = config.pkgs_dirs[0]
cache_dir = join(pkgs_dir, 'cache')

pkgs = defaultdict(list)

for fn in os.listdir(cache_dir):
    if not (len(fn) == 13 and fn.endswith('.json')):
        continue
    sys.stdout.write('.')
    sys.stdout.flush()
    d = json.load(open(join(cache_dir, fn)))
    for fn, info in d['packages'].iteritems():
        pkgs[fn].append(info)
print

def find_info(fn):
    if fn not in pkgs:
        return None
    size = getsize(join(pkgs_dir, fn))
    for info in pkgs[fn]:
        if info.get('size') == size:
            assert '%(name)s-%(version)s-%(build)s.tar.bz2' % info == fn, fn
            return info
    return None

index = {}
for fn in os.listdir(pkgs_dir):
    info = find_info(fn)
    if info:
        index[fn] = info
    
pprint(index)
