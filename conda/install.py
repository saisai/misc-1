import sys
import json
import time
from collections import defaultdict
from pprint import pprint

from resolve import MatchSpec

import pycosat


with open('joined.json') as fi:
    index = json.load(fi)

v = {} # map fn to variable number
w = {} # map variable number to fn
for i, fn in enumerate(index.iterkeys()):
    v[fn] = i + 1
    w[i + 1] = fn

for info in index.itervalues():
    info['ms_depends'] = [MatchSpec(mspec) for mspec in info['depends']]
    info['ms_conflicts'] = [MatchSpec(mspec)
                            for mspec in info.get('conflicts', [])]
    info['features'] = set(info.get('features', '').split())

groups = defaultdict(list) # map name to list of filenames
for fn, info in index.iteritems():
    groups[info['name']].append(fn)

def itergroup(name):
    for fn in groups[name]:
        info = index[fn]
        assert info['name'] == name
        yield fn

def find_matches(ms):
    for fn2 in itergroup(ms.name):
        if ms.match(fn2):
            yield fn2

clauses = []

for filenames in groups.itervalues():
    # ensure packages with the same name conflict
    for fn1 in filenames:
        v1 = v[fn1]
        for fn2 in filenames:
            v2 = v[fn2]
            if v1 < v2:
                clauses.append([-v1, -v2])

def add_clauses(fn1):
    # translate the requirements of package `fn` to clauses
    info1 = index[fn1]
    for ms in info1['ms_depends']:
        clause = [-v[fn1]]
        for fn2 in find_matches(ms):
            clause.append(v[fn2])

        assert len(clause) > 1, fn1
        clauses.append(clause)

    for ms in info1['ms_conflicts']:
        for fn2 in find_matches(ms):
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
