import json
import time
from collections import defaultdict
from pprint import pprint

import pycosat
from ll.diffutils import show_set_diff


with open('index.json') as fi:
    index = json.load(fi)

v = {} # map fn to variable number
w = {} # map variable number to fn
for i, fn in enumerate(index.iterkeys()):
    v[fn] = i + 1
    w[i + 1] = fn

groups = defaultdict(list) # map name to list of filenames
for fn, info in index.iteritems():
    groups[info['name']].append(fn)

def itergroup(name):
    for fn in groups[name]:
        info = index[fn]
        assert info['name'] == name
        yield fn, info

def split_requirement(s):
    parts = s.split()
    while len(parts) < 3:
        parts.append(None)
    assert len(parts) == 3
    return tuple(parts)

def reqs_pkg(fn):
    "given a package, return all possible requirements"
    for r in index[fn]['requires']:
        name, version, build = split_requirement(r)
        if version is None:
            raise
            assert build is None
            for fn2, unused_info in itergroup(name):
                yield name, version, fn2

        elif name in ('python', 'numpy') and len(version) == 3:
            assert build is None
            for fn2, info2 in itergroup(name):
                if info2['version'].startswith(version):
                    yield name, version, fn2

        elif build is None:
            for fn2, info2 in itergroup(name):
                if info2['version'] == version:
                    yield name, version, fn2

        else:
            fn2 = '%s-%s-%s.tar.bz2' % (name, version, build)
            assert fn2 in index
            yield name, version, fn2

def resolve(root_fn):
    req_names = set()
    pkgs = set()

    def add_dependents(fn1):
        for name, version, fn2 in reqs_pkg(fn1):
            if name in req_names:
                continue
            req_names.add(name)
            for f in files:
                pkgs.add(f)
                add_dependents(f)

    add_dependents(root_fn)
    return pkgs

if 1:
    fn = 'anaconda-1.4.1-np17py27_0.tar.bz2'
    #pprint(index[fn])
    ana_shallow = set()
    for name, version, fn in reqs_pkg(fn):
        ana_shallow.add(fn)
    for f1 in ana_shallow:
        print 'ana_shallow ========', f1
        for f in resolve(f1):
            print f
            #assert f in ana_shallow, f
