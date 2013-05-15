import re

import verlib

from install import index, groups, itergroup, find_matches


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


def nvb_fn(fn):
    return tuple(fn[:-8].rsplit('-', 2))

def split_requirement(s):
    parts = s.split()
    while len(parts) < 3:
        parts.append(None)
    assert len(parts) == 3
    return tuple(parts)

def get_dist(ms):
    pkgs = set(Package(fn) for fn in find_matches(ms))
    if not pkgs:
       return None
    maxpkg = max(pkgs)
    print '   ', ms
    for pkg in pkgs:
        if pkg == maxpkg:
            print '\t', pkg
    return maxpkg.fn

def shallow_deps(fn):
    pkgs = set()
    for ms in index[fn]['ms_depends']:
        for fn2 in find_matches(ms):
            pkgs.add(fn2)
    return pkgs

def all_deps(root_fn):
    res = set()

    def add_dependents(fn1):
        for ms in index[fn1]['ms_depends']:
            fn2 = get_dist(ms)
            assert fn2 is not None
            res.add(fn2)
            add_dependents(fn2)

    add_dependents(root_fn)
    return res


def show_sorted_versions():
    for name in sorted(groups):
        pkgs = [Package(fn) for fn in itergroup(name)]
        pkgs.sort()
        disp = []
        for pkg in pkgs:
            x = '%s-%d' % (pkg.version, pkg.build_number)
            if str(pkg.norm_version) != pkg.version:
                x += '          %s' % pkg.norm_version
            if x not in disp:
                disp.append(x)
        if len(disp) > 1:
            print name
            for x in disp:
                print '\t' + x

def meta_pkg_deps(fn):
    return ['%s-%s-%s.tar.bz2' % split_requirement(r)
            for r in index[fn]['requires']]

def filter(dists, py_ver='2.7', npy_ver='1.7'):
    res = []
    for fn in dists:
        info = index[fn]
        if info.get('features'):
            continue
        if any((ms.name == 'python' and not ms.match('python-%s-0' % py_ver) or
                (ms.name == 'numpy') and not ms.match('numpy-%s-0' % npy_ver))
               for ms in info['ms_depends']):
            continue
        res.append(fn)
    return res

def show_inconsistencies(meta_fn):
    pat = re.compile(r'np(\d{2})py(\d{2})_')
    b = nvb_fn(meta_fn)[2]
    m = pat.match(b)
    py_ver  = '.'.join(m.group(2))
    npy_ver = '.'.join(m.group(1))

    mp_deps = meta_pkg_deps(meta_fn)
    res = set()
    for fn1 in mp_deps:
        deps = filter(shallow_deps(fn1), py_ver, npy_ver)
        #print fn1, len(deps)
        pkgs = [Package(fn) for fn in deps]
        names = set(p.name for p in pkgs)
        for name in names:
            fn2 = max(p for p in pkgs if p.name == name).fn
            if fn2.startswith(('python-', 'numpy-')):
                continue
            if fn2 not in mp_deps:
                res.add('%s required by %s' % (fn2, fn1))
    for fn in res:
        print fn


if __name__ == '__main__':
    #show_sorted_versions()
    #for fn in index:
    #    if not fn.startswith(('anaconda-1.5.0-', 'anaconda-1.4.0-np17py27')):
    #        continue
    #    print fn
    #    show_inconsistencies(fn)
    for fn in sorted(all_deps('scipy-0.12.0-np15py26_0.tar.bz2')):
        print fn
