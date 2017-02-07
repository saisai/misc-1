import json
import time
from collections import defaultdict
from os.path import join

from repo.filedb import find_repo_dirs
from repo.utils import meta_from_index


def read_repodatas():
    for dir_path in sorted(find_repo_dirs()):
        #print dir_path
        with open(join(dir_path, 'repodata.json')) as fi:
            index = json.load(fi)['packages']
        for fn in sorted(index):
            yield join(dir_path, fn)


res = defaultdict(int)

for path in read_repodatas():
    meta = meta_from_index(path)
    if meta is None:
        continue
    ctime = meta['ctime']
    date = time.strftime("%Y-%m-%d", time.localtime(ctime))
    res[date] += 1

for date in sorted(res):
    print date, res[date]
