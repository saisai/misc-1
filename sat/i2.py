from pprint import pprint

from ll.diffutils import show_set_diff

from install import index, split_requirement, find_matches


def nvb_fn(fn):
    return tuple(fn[:-8].rsplit('-', 2))

def resolve(root_fn):
    req_names = set()
    pkgs = set()

    def add_dependents(fn1):
        for r in index[fn1]['requires']:
            name, version, build = split_requirement(r)
            if name in req_names:
                continue
            for fn2 in find_matches(name, version, build):
                pkgs.add(fn2)
                add_dependents(fn2)
            req_names.add(name)

    add_dependents(root_fn)
    return pkgs

fn = 'anaconda-1.4.1-np17py27_0.tar.bz2'
#fn = 'bitarray-0.8.0-py26_0.tar.bz2'
#
pprint(resolve(fn))
#ana_shallow = set()
#for name, version, fn in reqs_pkg(fn):
#    ana_shallow.add(fn)
#for f1 in ana_shallow:
#    print 'ana_shallow ========', f1
#    for f in resolve(f1):#
#        print f
#        #assert f in ana_shallow, f
#print list(find_matches(*nvb_fn(fn)))
