from pprint import pprint
from collections import defaultdict

import pycosat

import verlib

from install import index, find_matches


class Package(object):

    def __init__(self, fn):
        self.fn = fn
        info = index[fn]
        self.name = info['name']
        self.version = info['version']
        self.build_number = info['build_number']
        self.add_norm_version()

    def add_norm_version(self):
        v = self.version
        v = v.replace('rc', '.dev99999')
        if v.endswith('.dev'):
            v += '0'
        try:
            self.norm_version = verlib.NormalizedVersion(v)
        except verlib.IrrationalVersionError:
            self.norm_version = self.version

    def __cmp__(self, other):
        assert self.name == other.name
        try:
            return cmp((self.norm_version, self.build_number),
                       (other.norm_version, other.build_number))
        except TypeError:
            return cmp((self.version, self.build_number),
                       (other.version, other.build_number))

    def __repr__(self):
        return self.fn


def get_dists(ms):
    pkgs = set(Package(fn) for fn in find_matches(ms))
    assert pkgs
    maxpkg = max(pkgs)
    for pkg in pkgs:
        if pkg == maxpkg:
            yield pkg.fn

def all_deps(root_fn):
    res = set()

    def add_dependents(fn1):
        for ms in index[fn1]['ms_depends']:
            for fn2 in get_dists(ms):
                if fn2 in res:
                    continue
                res.add(fn2)
                add_dependents(fn2)

    add_dependents(root_fn)
    return res


min_candidate = 10000,

def solve(root_fn, features):
    #print '*** %s %r ***' % (root_fn, features)

    dists = all_deps(root_fn)
    #pprint(dists)
    dists.add(root_fn)

    v = {} # map fn to variable number
    w = {} # map variable number to fn
    for i, fn in enumerate(sorted(dists)):
        v[fn] = i + 1
        w[i + 1] = fn

    groups = defaultdict(list) # map name to list of filenames
    for fn in dists:
        groups[index[fn]['name']].append(fn)

    clauses = []

    for filenames in groups.itervalues():
        # ensure packages with the same name conflict
        for fn1 in filenames:
            v1 = v[fn1]
            for fn2 in filenames:
                v2 = v[fn2]
                if v1 < v2:
                    clauses.append([-v1, -v2])

    for fn1 in dists:
        info1 = index[fn1]
        for ms in info1['ms_depends']:
            clause = [-v[fn1]]
            for fn2 in find_matches(ms):
                if fn2 in dists:
                    clause.append(v[fn2])

            assert len(clause) > 1, fn1
            clauses.append(clause)

    clauses.append([v[root_fn]])
    #pprint(clauses)
    candidates = defaultdict(list)
    for sol in pycosat.itersolve(clauses):
        fsd = 0
        pkgs = [w[lit] for lit in sol if lit > 0]
        for fn in pkgs:
            fsd += len(features ^ index[fn]['features'])
        key = fsd, len(pkgs)
        candidates[key].append(pkgs)

    global min_candidate
    if len(candidates) < min_candidate[0]:
        min_candidate = len(candidates), root_fn, features

    minkey = min(candidates)

    mc = candidates[minkey]
    if len(mc) != 1:
        print root_fn, features
        print 'minkey =', minkey
        pprint(mc)

    return candidates[minkey][0]


def main():
    ignore = set(['statsmodels-0.4.3-np16py26_0.tar.bz2',
                  'statsmodels-0.4.3-np16py27_0.tar.bz2',
                  'statsmodels-0.4.3-np17py27_0.tar.bz2',
                  'statsmodels-0.4.3-np17py26_0.tar.bz2',
                  'anaconda-launcher-0.0-py27_0.tar.bz2',
                  ])
    for fn in index:
        if fn in ignore or '-np15py' in fn:
            continue
        if index[fn]['name'] == 'anaconda':
            continue
        for features in set([]), set(['mkl']):
            solve(fn, features)
    print 'OK'
    print min_candidate

if __name__ == '__main__':
    #pprint(solve('accelerate-1.1.0-np17py26_p0.tar.bz2', ['mkl']))
    main()
