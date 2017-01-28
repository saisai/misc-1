import json
from os.path import basename, dirname, join

from ll.utils import memoized
from repo.filedb import read_repodatas
from repo.repack import meta_from_repodata
from repo.utils import normalize_depends


@memoized
def read_index(dir_path):
    try:
        return json.load(open(join(dir_path, 'index.json')))
    except IOError:
        return None

def meta_from_index(tar_path):
    index = read_index(dirname(tar_path))
    if index is None:
        return None
    return index[basename(tar_path)]


for path, unused_md5 in read_repodatas():
    meta2 = meta_from_index(path)
    if meta2 is None:
        continue
    meta1 = meta_from_repodata(path)

    changes = (meta1['depends'] !=
               normalize_depends(meta2.get('depends', [])))
    print '%-60s %s' % (path[17:], changes)
