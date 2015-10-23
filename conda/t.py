from conda.api import get_index
from conda.plan import add_defaults_to_specs
from conda.resolve import Resolve
from conda.cli.common import specs_from_args



def main():
    from optparse import OptionParser

    p = OptionParser(usage="usage: %prog SPEC [SPEC ...]",
                     description="""\
creates explicit file from SPECs.""")

    opts, args = p.parse_args()

    specs = specs_from_args(args)
    index = get_index(())
    r = Resolve(index)
    add_defaults_to_specs(r, [], specs)
    dists = list(r.solve(specs))

    print
    print
    print '@EXPLICIT'
    for dist in dists:
        url = index[dist]['channel'] + dist
        print url


if __name__ == '__main__':
    main()
