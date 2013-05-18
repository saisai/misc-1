import itertools
from pprint import pprint
from collections import defaultdict
from optparse import OptionParser

import pycosat

import verlib
from utils import iter_pairs, memoized
from install import index, find_matches
from matcher import MatchSpec


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
        assert self.name == other.name, '%r %r' % (self.fn, other.fn)
        try:
            return cmp((self.norm_version, self.build_number),
                       (other.norm_version, other.build_number))
        except TypeError:
            return cmp((self.version, self.build_number),
                       (other.version, other.build_number))

    def __repr__(self):
        return self.fn


def get_max_dists(ms):
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
            for fn2 in get_max_dists(ms):
                if fn2 in res:
                    continue
                res.add(fn2)
                if ms.strictness < 3:
                    add_dependents(fn2)

    add_dependents(root_fn)
    return res


def solve(root_dists, features, verbose=False):
    #print '*** %s %r ***' % (root_fn, features)

    dists = set()
    for root_fn in root_dists:
        dists.update(all_deps(root_fn))
        dists.add(root_fn)

    #pprint(dists)

    groups = defaultdict(list) # map name to list of filenames
    for fn in dists:
        groups[index[fn]['name']].append(fn)

    if len(groups) == len(dists):
        assert all(len(filenames) == 1 for filenames in groups.itervalues())
        if verbose:
            print "No duplicate name, no SAT needed."
        return sorted(dists)

    v = {} # map fn to variable number
    w = {} # map variable number to fn
    for i, fn in enumerate(sorted(dists)):
        v[fn] = i + 1
        w[i + 1] = fn

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

    for root_fn in root_dists:
        clauses.append([v[root_fn]])

    #pprint(clauses)
    candidates = defaultdict(list)
    for sol in pycosat.itersolve(clauses):
        pkgs = [w[lit] for lit in sol if lit > 0]
        fsd = sum(len(features ^ index[fn]['features']) for fn in pkgs)
        key = fsd, len(pkgs)
        #print key, pkgs
        candidates[key].append(pkgs)

    if not candidates:
        print "Error: UNSAT"
        return []

    minkey = min(candidates)

    mc = candidates[minkey]
    if len(mc) != 1:
        print 'WARNING:', len(mc), root_dists, features

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
        for features in set([]), set(['mkl']):
            solve([fn], features)
    print 'OK'

verscores = {}
def select_dists_spec(spec):
    mspec = spec.replace('=', ' ')
    if spec.count('=') == 1:
        mspec += '*'
    ms = MatchSpec(mspec)

    pkgs = [Package(fn) for fn in find_matches(ms)]
    pkgs.sort()
    vs = 0
    for p1, p2 in iter_pairs(pkgs):
        verscores[p1.fn] = vs
        if p2 and p2 > p1:
            vs += 1
    #pprint(verscores)
    return [p.fn for p in pkgs]

@memoized
def sum_matches(fn1, fn2):
    return sum(ms.match(fn2[:-8]) for ms in index[fn1]['ms_depends'])

def select_root_dists(specs, features, installed):
    args = [select_dists_spec(spec) for spec in specs]

    @memoized
    def installed_matches(fn):
        return sum(sum_matches(fn, fn2) for fn2 in installed)

    candidates = defaultdict(list)
    for dists in itertools.product(*args):
        fsd = olx = svs = sim = 0
        for fn1 in dists:
            fsd += len(features ^ index[fn1]['features'])
            olx += sum(sum_matches(fn1, fn2) for fn2 in dists if fn1 != fn2)
            svs += verscores[fn1]
            sim += installed_matches(fn1)

        key = -fsd, olx, svs, sim
        #print dists, key
        candidates[key].append(dists)

    maxkey = max(candidates)
    print 'maxkey:', maxkey

    mc = candidates[maxkey]
    if len(mc) != 1:
        print 'WARNING:', len(mc)
        for c in mc:
            print '\t', c

    return set(candidates[maxkey][0])


if __name__ == '__main__':
    p = OptionParser(usage="usage: %prog [options] SPEC")
    p.add_option("--mkl", action="store_true")
    opts, args = p.parse_args()

    if len(args) == 0:
        main()
    else:
        features = set(['mkl']) if opts.mkl else set()
        installed = solve({'anaconda-1.5.0-np17py27_0.tar.bz2'}, set())

        files = select_root_dists(args, features, installed)
        print files, features
        pprint(solve(files, features, verbose=True))
