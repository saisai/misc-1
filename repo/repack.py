import sys
import json
import shutil
import tempfile
from os.path import basename, isdir, join

from ll.utils import tar_cf, tar_xf, rm_rf
from bt.build import tar_recipe

from anaconda_verify.package import validate_package


def repack(tar_path):
    tmp_dir = tempfile.mkdtemp()
    info_dir = join(tmp_dir, 'info')
    tar_xf(tar_path, tmp_dir)
    assert isdir(info_dir)

    for fn in 'git', 'files.json', 'recipe.json', 'requires':
        rm_rf(join(info_dir, fn))
    tar_recipe(info_dir)

    tar_cf(basename(tar_path), tmp_dir)
    shutil.rmtree(tmp_dir)


def main():
    repack(sys.argv[1])


if __name__ == '__main__':
    main()
