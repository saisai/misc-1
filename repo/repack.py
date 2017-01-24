import copy
import json
import shutil
import tempfile
from pprint import pprint
from os.path import basename, dirname, join

from ll.utils import tar_cf, tar_xf, tar_recipe, rm_rf, memoized
from ll.diffutils import show_dict_diff

from anaconda_verify.package import validate_package


VERBOSITY = 0


@memoized
def meta_from_repodata(tar_path):
    repodata = json.load(open(join(dirname(tar_path), 'repodata.json')))
    index = repodata['packages']
    meta = index[basename(tar_path)]
    for key in 'date', 'md5', 'size':
        del meta[key]
    return meta


def cleanup_info_dir(info_dir):
    for fn in 'git', 'files.json', 'recipe.json':
        rm_rf(join(info_dir, fn))
    tar_recipe(info_dir)


def update_meta(meta1, meta2):
    for key in 'name', 'version', 'build', 'build_number':
        # sanity check
        assert meta1[key] == meta2[key], key

    old_meta2 = copy.deepcopy(meta2)
    for key in 'depends', 'license':
        meta2[key] = meta1[key]

    for key in 'license_family', :
        if key in meta1:
            meta2[key] = meta1[key]

    res = bool(old_meta2 != meta2)
    if VERBOSITY > 0:
        print '  Changes: %s  %s' % (res, '*' * 5 * int(res))
    if VERBOSITY > 1:
        show_dict_diff(old_meta2, meta2)
    # return if changes have been made to meta2
    return res


def repack(tar_path, force=False, dry=False):
    if VERBOSITY > 0:
        print '==> %s <==' % tar_path
    meta1 = meta_from_repodata(tar_path)
    if VERBOSITY > 2:
        pprint(meta1)

    tmp_dir = tempfile.mkdtemp()
    info_dir = join(tmp_dir, 'info')
    tar_xf(tar_path, tmp_dir)

    meta2 = json.load(open(join(info_dir, 'index.json')))
    if VERBOSITY > 2:
        pprint(meta2)
        show_dict_diff(meta1, meta2)

    changes = update_meta(meta1, meta2)
    if dry or (not changes and not force):
        shutil.rmtree(tmp_dir)
        return

    if VERBOSITY > 2:
        pprint(meta2)

    with open(join(info_dir, 'index.json'), 'w') as fo:
        json.dump(meta2, fo, indent=2, sort_keys=True)
    cleanup_info_dir(info_dir)
    out_path = basename(tar_path)
    tar_cf(out_path, tmp_dir, mode='w:bz2')
    shutil.rmtree(tmp_dir)
    validate_package(out_path)


def main():
    global VERBOSITY
    from optparse import OptionParser

    p = OptionParser(
        usage="usage: %prog [options] TAR [TAR ...]",
        description="repack conda packages")

    p.add_option('-f', '--force',
                 action="store_true",
                 help="force repack, even when not necessary from metadata "
                      "perspective")

    p.add_option('-n', '--dry-run',
                 action="store_true",
                 help="only show what metadata would have been changed")

    p.add_option('-v', '--verbosity',
                 action="store",
                 default=1,
                 help='verbosity level, 0..3, defaults to %default',
                 metavar='LEVEL')

    opts, args = p.parse_args()
    try:
        VERBOSITY = int(opts.verbosity)
    except TypeError:
        p.error('integer expected')

    for path in args:
        if not path.endswith('.tar.bz2'):
            print 'ignoring:', path
            continue
        repack(path, force=opts.force, dry=opts.dry_run)


if __name__ == '__main__':
    main()
