from pprint import pprint

from ll.diffutils import show_set_diff
import verlib

from install import index, groups, itergroup, split_requirement, find_matches


def nvb_fn(fn):
    return tuple(fn[:-8].rsplit('-', 2))

def shallow_deps(fn):
    pkgs = set()
    for r in index[fn]['requires']:
        for fn2 in find_matches(*split_requirement(r)):
            pkgs.add(fn2)
    return pkgs

def all_deps(root_fn):
    pkgs = set()

    def add_dependents(fn1):
        for r in index[fn1]['requires']:
            for fn2 in find_matches(*split_requirement(r)):
                pkgs.add(fn2)
                add_dependents(fn2)

    add_dependents(root_fn)
    return pkgs

def foo():
    fn = 'anaconda-1.4.1-np17py27_0.tar.bz2'
    sd = shallow_deps(fn)
    for fn in sd:
        print fn
        print all_deps(fn)

class Package(object):

    def __init__(self, fn):
        self.fn = fn
        self.info = index[fn]
        self.name = self.info['name']
        self.version = self.info['version']
        self.build_number = self.info['build_number']
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

def show_sorted_versions():
    for name in sorted(groups):
        pkgs = [Package(fn) for fn, unused_info in itergroup(name)]
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

def max_pkg_fn(name, py_ver='2.7', npy_ver='1.7'):
    pkgs = []
    for fn2, info2 in itergroup(name):
        if any((r.startswith('python ') and r != 'python %s' % py_ver) or
               (r.startswith('numpy ') and r != 'numpy %s' % npy_ver)
               for r in info2['requires']):
            continue
        pkgs.append(Package(fn2))

    return max(pkgs).fn


if __name__ == '__main__':
    #show_sorted_versions()

    fn = 'anaconda-1.4.1-np17py27_0.tar.bz2'
    sd = shallow_deps(fn)
    ad = all_deps(fn)
    for fn1 in sd:
        name, unused_version, unused_buid = nvb_fn(fn1)
        max_fn = max_pkg_fn(name)
        if fn1 != max_fn:
            print fn1, max_fn
