import shutil
import tempfile
from os.path import isdir, join

from ll.utils import tar_cf, tar_xf, rm_rf
from bt.build import tar_recipe

from anaconda_verify.package import validate_package


def repack(tar_path):
    tmp_dir = tempfile.mkdtemp()
    info_dir = join(tmp_dir, 'info')
    tar_xf(tar_path, tmp_dir)
    assert isdir(info_dir)

    for fn in 'git', 'files.json', 'recipe.json':
        rm_rf(join(info_dir, fn))
    tar_recipe(info_dir)

    tar_cf(tar_path, tmp_dir, mode='w:bz2')
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
