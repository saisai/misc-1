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

        try:
            self.norm_version = verlib.NormalizedVersion(self.version)
        except verlib.IrrationalVersionError:
            self.norm_version = self.version

    def  __cmp__(self, other):
        assert self.name == other.name
        try:
            return cmp((self.norm_version, self.build_number),
                       (other.norm_version, other.build_number))
        except TypeError:
            return cmp((self.version, self.build_number),
                       (other.version, other.build_number))

def main():
    for name in groups:
        print name

        pkgs = []
        for fn, info in itergroup(name):
            pkgs.append(Package(fn))
        pkgs.sort()
        for pkg in pkgs:
            print pkg.version, pkg.build_number


if __name__ == '__main__':
    main()
