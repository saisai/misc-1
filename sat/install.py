import json
from collections import defaultdict
from pprint import pprint

import pycosat


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

clauses = []

for filenames in groups.itervalues():
    # ensure packages with the same name conflict
    for fn1 in filenames:
        v1 = v[fn1]
        for fn2 in filenames:
            v2 = v[fn2]
            if v1 < v2:
                clauses.append([-v1, -v2])

for fn1, info1 in index.iteritems():
    for r in info1['requires']:
        parts = r.split()
        clause = [-v[fn1]]
        if len(parts) == 2:
            parts.append(None)
        name, version, build = parts
        assert name != info1['name']

        if name in ('python', 'numpy') and len(version) == 3:
            assert build is None
            for fn2 in groups[name]:
                info2 = index[fn2]
                assert info2['name'] == name
                if info2['version'].startswith(version):
                    clause.append(v[fn2])

        elif build is None:
            for fn2 in groups[name]:
                info2 = index[fn2]
                assert info2['name'] == name
                if info2['version'] == version:
                    clause.append(v[fn2])

        else:
            fn2 = '%s-%s-%s.tar.bz2' % tuple(parts)
            clause.append(v[fn2])

        assert len(clause) > 1
        clauses.append(clause)


#pprint([' V '.join(('-' if i<0 else '') + w[abs(i)] for i in clause)
#        for clause in clauses])

clauses.append([v['anaconda-1.4.0-np17py27_0.tar.bz2']])

for sol in pycosat.itersolve(clauses):
    pprint(sorted(w[i] for i in sol if i > 0))
