import sys
import json
import time
from collections import defaultdict
from pprint import pprint

import trans

import pycosat


with open('joined.json') as fi:
    index = json.load(fi)

trans.add_all_depends(index)

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

clauses = []

for filenames in groups.itervalues():
    # ensure packages with the same name conflict
    for fn1 in filenames:
        v1 = v[fn1]
        for fn2 in filenames:
            v2 = v[fn2]
            if v1 < v2:
                clauses.append([-v1, -v2])

def split_requirement(s):
    parts = s.split()
    while len(parts) < 3:
        parts.append(None)
    assert len(parts) == 3
    return tuple(parts)

def find_matches(name, version, build):
    assert name is not None
    if version is None:
        assert build is None
        for fn2, unused_info in itergroup(name):
            yield fn2

    elif name in ('python', 'numpy') and len(version) == 3:
        assert build is None
        for fn2, info2 in itergroup(name):
            if info2['version'].startswith(version):
                yield fn2

    elif build is None:
        for fn2, info2 in itergroup(name):
            if info2['version'] == version:
                yield fn2

    else:
        fn2 = '%s-%s-%s.tar.bz2' % (name, version, build)
        assert fn2 in index, fn2
        yield fn2

def add_clauses(fn1):
    # translate the requirements of package `fn` to clauses
    info1 = index[fn1]
    for r in info1['requires']:
        name, version, build = split_requirement(r)
        assert name and name != info1['name']

        clause = [-v[fn1]]
        for fn2 in find_matches(name, version, build):
            clause.append(v[fn2])

        assert len(clause) > 1, fn1
        clauses.append(clause)

    for name in info1.get('conflicts', []):
        for fn2 in find_matches(name, None, None):
            clauses.append([-v[fn1], -v[fn2]])


for fn in index.iterkeys():
    add_clauses(fn)


if __name__ == '__main__':
    print len(v), len(w), len(clauses)
    #pprint([' V '.join(('-' if i<0 else '') + w[abs(i)] for i in clause)
    #        for clause in clauses])

    clauses.append(None)
    for fn in sorted(index):
        if not fn.startswith('anaconda-'):
            continue
        clauses[-1] = [v[fn]]
        sol = pycosat.solve(clauses)
        if not isinstance(sol, list):
            print fn, sol
