import itertools
from pprint import pprint
from collections import defaultdict
from optparse import OptionParser

import pycosat

import verlib
from utils import iter_pairs, memoized, memoize
from matcher import MatchSpec


class Package(object):

    def __init__(self, fn, info):
        self.fn = fn
        self.name = info['name']
        self.version = info['version']
        self.build_number = info['build_number']

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

class Resolve(object):

    def __init__(self, index):
        self.index = index
        self.groups = defaultdict(list) # map name to list of filenames
        for fn, info in index.iteritems():
            self.groups[info['name']].append(fn)
        self.msd = {}

    def find_matches(self, ms):
        for fn in self.groups[ms.name]:
            if ms.match(fn):
                yield fn

    def ms_depends(self, fn):
        try:
            res = self.msd[fn]
        except KeyError:
            res = self.msd[fn] = [MatchSpec(d)
                                  for d in self.index[fn]['depends']]
        return res

    @memoize
    def features(self, fn):
        return set(self.index[fn].get('features', '').split())

    @memoize
    def get_pkgs(self, ms):
        #print ms, isinstance(ms, collections.Hashable)
        return [Package(fn, self.index[fn]) for fn in self.find_matches(ms)]

    def get_max_dists(self, ms):
        pkgs = self.get_pkgs(ms)
        assert pkgs
        maxpkg = max(pkgs)
        for pkg in pkgs:
            if pkg == maxpkg:
                yield pkg.fn

    def all_deps(self, root_fn):
        res = set()

        def add_dependents(fn1):
            for ms in self.ms_depends(fn1):
                for fn2 in self.get_max_dists(ms):
                    if fn2 in res:
                        continue
                    res.add(fn2)
                    if ms.strictness < 3:
                        add_dependents(fn2)

        add_dependents(root_fn)
        return res

    def solve2(self, root_dists, features, verbose=False):
        dists = set()
        for root_fn in root_dists:
            dists.update(self.all_deps(root_fn))
            dists.add(root_fn)

        groups = defaultdict(list) # map name to list of filenames
        for fn in dists:
            groups[self.index[fn]['name']].append(fn)

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
            for ms in self.ms_depends(fn1):
                clause = [-v[fn1]]
                for fn2 in self.find_matches(ms):
                    if fn2 in dists:
                        clause.append(v[fn2])

                assert len(clause) > 1, fn1
                clauses.append(clause)

        for root_fn in root_dists:
            clauses.append([v[root_fn]])

        candidates = defaultdict(list)
        for sol in pycosat.itersolve(clauses):
            pkgs = [w[lit] for lit in sol if lit > 0]
            fsd = sum(len(features ^ self.features(fn)) for fn in pkgs)
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

    verscores = {}
    def select_dists_spec(self, spec):
        mspec = spec.replace('=', ' ')
        if spec.count('=') == 1:
            mspec += '*'
        ms = MatchSpec(mspec)

        pkgs = sorted(self.get_pkgs(ms))
        vs = 0
        for p1, p2 in iter_pairs(pkgs):
            self.verscores[p1.fn] = vs
            if p2 and p2 > p1:
                vs += 1
        #pprint(self.verscores)
        return [p.fn for p in pkgs]

    @memoize
    def sum_matches(self, fn1, fn2):
        return sum(ms.match(fn2) for ms in self.ms_depends(fn1))

    def select_root_dists(self, specs, features, installed):
        args = [self.select_dists_spec(spec) for spec in specs]

        @memoized
        def installed_matches(fn):
            return sum(self.sum_matches(fn, fn2) for fn2 in installed)

        candidates = defaultdict(list)
        for dists in itertools.product(*args):
            fsd = olx = svs = sim = 0
            for fn1 in dists:
                fsd += len(features ^ self.features(fn1))
                olx += sum(self.sum_matches(fn1, fn2)
                           for fn2 in dists if fn1 != fn2)
                svs += self.verscores[fn1]
                sim += installed_matches(fn1)

            key = -fsd, olx, svs, sim
            #print dists, key
            candidates[key].append(dists)

        maxkey = max(candidates)
        #print 'maxkey:', maxkey

        mc = candidates[maxkey]
        if len(mc) != 1:
            print 'WARNING:', len(mc)
            for c in mc:
                print '\t', c

        return set(candidates[maxkey][0])

    def tracked_features(self, installed):
        res = set()
        for fn in installed:
            try:
                res.update(self.features(fn))
            except KeyError:
                pass
        return res

    def update_with_features(self, fn, features):
        info = self.index[fn]
        for fs, depends_updates in info.get('with_features', {}).iteritems():
            if not set(fs.split()).issubset(features):
                continue
            updates = {ms.name: ms for ms in [MatchSpec(mspec)
                                              for mspec in depends_updates]}
            for i, ms in enumerate(self.msd[fn]):
                if ms.name in updates:
                    self.msd[fn][i] = updates[ms.name]

    def solve(self, specs, installed=None, features=None, verbose=False):
        if installed is None:
            installed = []
        if features is None:
            features = self.tracked_features(installed)
        dists = self.select_root_dists(specs, features, installed)
        for fn in dists:
            track_features = set(
                       self.index[fn].get('track_features', '').split())
            features.update(track_features)
        if verbose:
            print dists, features
        for fn in dists:
            self.update_with_features(fn, features)
        return self.solve2(dists, features, verbose)


def test_all():
    ignore = set(['statsmodels-0.4.3-np16py26_0.tar.bz2',
                  'statsmodels-0.4.3-np16py27_0.tar.bz2',
                  'statsmodels-0.4.3-np17py27_0.tar.bz2',
                  'statsmodels-0.4.3-np17py26_0.tar.bz2',
                  'anaconda-launcher-0.0-py27_0.tar.bz2',
                  ])
    r = Resolve(get_index())
    for fn in r.index:
        if fn in ignore or '-np15py' in fn:
            continue
        for features in set([]), set(['mkl']):
            r.solve2([fn], features)
    print 'OK'

def get_index():
    import json
    import trans
    with open('joined.json') as fi:
        index = json.load(fi)
    trans.add_all_depends(index)
    return index

if __name__ == '__main__':
    p = OptionParser(usage="usage: %prog [options] SPEC")
    p.add_option("--mkl", action="store_true")
    opts, args = p.parse_args()

    if len(args) == 0:
        test_all()
    else:
        features = set(['mkl']) if opts.mkl else set()
        installed = ['numpy-1.7.1-py27_0.tar.bz2',
                     'python-2.7.5-0.tar.bz2']
        r = Resolve(get_index())
        pprint(r.solve(args, installed, features, verbose=True))
