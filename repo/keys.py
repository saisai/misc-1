import json
from collections import defaultdict
from os.path import join

from repo.filedb import find_repo_dirs


KEYS = defaultdict(int)


for dir_path in sorted(find_repo_dirs()):
    print dir_path
    with open(join(dir_path, 'repodata.json')) as fi:
        index = json.load(fi)['packages']
    for meta in index.itervalues():
        for key in meta.iterkeys():
            KEYS[key] += 1

for key in sorted(KEYS):
    print key, KEYS[key]
