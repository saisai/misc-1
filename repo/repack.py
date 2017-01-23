import json
import shutil
import tempfile
from pprint import pprint
from os.path import basename, dirname, join

from ll.utils import tar_cf, tar_xf, rm_rf
from ll.diffutils import show_dict_diff
from bt.build import tar_recipe

from anaconda_verify.package import validate_package


def repack(tar_path):
    repo_dir = dirname(tar_path)
    index = json.load(open(join(repo_dir, 'repodata.json')))['packages']
    meta1 = index[basename(tar_path)]
    for key in 'md5', 'size':
        del meta1[key]
    pprint(meta1)

    tmp_dir = tempfile.mkdtemp()
    info_dir = join(tmp_dir, 'info')
    tar_xf(tar_path, tmp_dir)

    meta2 = json.load(open(join(info_dir, 'index.json')))
    pprint(meta2)

    show_dict_diff(meta1, meta2)

    for fn in 'git', 'files.json', 'recipe.json':
        rm_rf(join(info_dir, fn))
    tar_recipe(info_dir)

    tar_cf(basename(tar_path), tmp_dir, mode='w:bz2')
    shutil.rmtree(tmp_dir)


def main():
    from optparse import OptionParser

    p = OptionParser(
        usage="usage: %prog [options] TAR [TAR ...]",
        description="repack conda packages")

    opts, args = p.parse_args()

    for path in args:
        if not path.endswith('.tar.bz2'):
            print 'ignoring:', path
            continue
        repack(path)
        validate_package(path)


if __name__ == '__main__':
    main()
