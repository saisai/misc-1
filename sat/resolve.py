from pprint import pprint

from ll.diffutils import show_set_diff

from install import index, split_requirement, find_matches


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

fn = 'anaconda-1.4.1-np17py27_0.tar.bz2'

sd = shallow_deps(fn)
for fn in sd:
    print fn
    print all_deps(fn)
