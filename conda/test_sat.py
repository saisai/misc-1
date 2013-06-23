import re

import pycosat
from conda.resolve import Package, Resolve



def nvb_fn(fn):
    return tuple(fn[:-8].rsplit('-', 2))


class Resolve2(Resolve):

    def create_var_map(self):
        self.v = {} # map fn to variable number
        self.w = {} # map variable number to fn
        for i, fn in enumerate(self.index.iterkeys()):
            self.v[fn] = i + 1
            self.w[i + 1] = fn

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
            for ms in self.ms_depends(fn1):
                clause = [-self.v[fn1]]
                for fn2 in self.find_matches(ms):
                    clause.append(self.v[fn2])

                assert len(clause) > 1, fn1
                clauses.append(clause)

        return clauses

    def meta_pkg_deps(self, fn):
        return ['%s-%s-%s.tar.bz2' % tuple(r.split())
                for r in self.index[fn]['depends']]

    def shallow_deps(self, fn):
        res = set()
        for ms in self.ms_depends(fn):
            for fn2 in self.find_matches(ms):
                res.add(fn2)
        return res

    def filter(self, dists, py_ver='2.7', npy_ver='1.7'):
        res = []
        for fn in dists:
            if any((fn.startswith(name + '-') and
                    not fn.startswith(name + '-' + ver))
                   for name, ver in (('python', py_ver), ('numpy', npy_ver))):
                continue
            info = self.index[fn]
            if any((r.startswith('python ') and r != 'python %s' % py_ver) or
                   (r.startswith('numpy ') and r != 'numpy %s' % npy_ver)
                   for r in info['requires']):
                continue
            res.append(fn)
        return res

    def show_inconsistencies(self, meta_fn):
        pat = re.compile(r'np(\d{2})py(\d{2})_0$')
        b = nvb_fn(meta_fn)[2]
        m = pat.match(b)
        py_ver  = '.'.join(m.group(2))
        npy_ver = '.'.join(m.group(1))

        mp_deps = self.meta_pkg_deps(meta_fn)
        res = set()
        for fn1 in mp_deps:
            deps = self.filter(self.shallow_deps(fn1), py_ver, npy_ver)
            pkgs = [Package(fn, self.index[fn]) for fn in deps]
            names = set(p.name for p in pkgs)
            for name in names:
                fn2 = max(p for p in pkgs if p.name == name).fn
                if fn2 not in mp_deps:
                    res.add('%s required by %s' % (fn2, fn1))
        for msg in res:
            print msg


def test_sat(index):
    r = Resolve2(index)
    r.create_var_map()

    clauses = r.get_clauses()
    clauses.append(None)
    a_versions = set()
    for fn in sorted(index):
        name, version, build = nvb_fn(fn)
        if name != 'anaconda' or version < '1.5':
            continue

        a_versions.add(version)
        clauses[-1] = [r.v[fn]]
        sol = pycosat.solve(clauses)
        print fn, 'SAT' if isinstance(sol, list) else sol
        if not isinstance(sol, list):
            r.show_inconsistencies(fn)

    print 'size index', len(index)
    for es in [
        ['numpy 1.7*', 'python 2.7*', 'conda'],
        ['numpy 1.7*', 'python 2.7*'],
        ['numpy 1.7*', 'python 2.6*'],
        #['numpy 1.7*', 'python 3.3*'],
        ['numpy 1.6*', 'python 2.7*'],
        ['numpy 1.6*', 'python 2.6*'],
        ]:
        for a_version in sorted(a_versions):
            specs = ['anaconda %s' % a_version]
            specs.extend(es)

            for features in set(), set(['mkl']):
                print specs, features
                r.msd_cache = {}
                assert r.solve(specs, features=features)


if __name__ == '__main__':
    import json
    from pprint import pprint
    from optparse import OptionParser

    with open('./index.json') as fi:
        index = json.load(fi)

    test_sat(index)
