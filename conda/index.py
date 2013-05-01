import json
from collections import defaultdict
from pprint import pprint

import pycosat


def split_requirement(s):
    parts = s.split()
    while len(parts) < 3:
        parts.append(None)
    assert len(parts) == 3
    return tuple(parts)


class Index(object):

    def __init__(self, index):
        self.index = index
        self.create_var_map()
        self.create_groups()

    def create_var_map(self):
        self.v = {} # map fn to variable number
        self.w = {} # map variable number to fn
        for i, fn in enumerate(self.index.iterkeys()):
            self.v[fn] = i + 1
            self.w[i + 1] = fn

    def create_groups(self):
        self.groups = defaultdict(list) # map name to list of filenames
        for fn, info in self.index.iteritems():
            self.groups[info['name']].append(fn)

    def itergroup(self, name):
        for fn in self.groups[name]:
            info = self.index[fn]
            assert info['name'] == name
            yield fn, info

    def find_matches(self, name, version, build):
        assert name is not None
        if version is None:
            assert build is None
            for fn2, unused_info in self.itergroup(name):
                yield fn2

        elif name in ('python', 'numpy') and len(version) == 3:
            assert build is None
            for fn2, info2 in self.itergroup(name):
                if info2['version'].startswith(version):
                    yield fn2

        elif build is None:
            for fn2, info2 in self.itergroup(name):
                if info2['version'] == version:
                    yield fn2

        else:
            fn2 = '%s-%s-%s.tar.bz2' % (name, version, build)
            assert fn2 in self.index, fn2
            yield fn2

    def get_clauses(self):
        clauses = []

        for filenames in self.groups.itervalues():
            # ensure packages with the same name conflict
            for fn1 in filenames:
                v1 = self.v[fn1]
                for fn2 in filenames:
                    v2 = self.v[fn2]
                    if v1 < v2:
                        clauses.append([-v1, -v2])

        for fn1 in self.index.iterkeys():
            info1 = self.index[fn1]
            for r in info1['requires']:
                name, version, build = split_requirement(r)
                assert name and name != info1['name']
                if build is None and name == 'nose':
                    continue

                clause = [-self.v[fn1]]
                for fn2 in self.find_matches(name, version, build):
                    clause.append(self.v[fn2])

                assert len(clause) > 1
                clauses.append(clause)

            for name in info1.get('conflicts', []):
                for fn2 in self.find_matches(name, None, None):
                    clauses.append([-self.v[fn1], -self.v[fn2]])

        return clauses


if __name__ == '__main__':
    with open('index.json') as fi:
        i =  Index(json.load(fi))

    clauses = i.get_clauses()
    print len(i.v), len(i.w), len(clauses)

    clauses.append(None)
    for fn in i.index:
        clauses[-1] = [i.v[fn]]
        sol = pycosat.solve(clauses)
        if not isinstance(sol, list):
            print fn, sol
        #pprint(sorted(w[i] for i in sol if i > 0))
