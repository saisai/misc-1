import time
from collections import defaultdict

from repo.filedb import read_repodatas
from repo.utils import meta_from_index


d = defaultdict(list)


for path, unused_md5 in read_repodatas():
    if '/free/' not in path:
        continue
    if '/noarch/' in path:
        continue
    meta = meta_from_index(path)
    name = meta['name']
    if name not in ('python', 'openssl'):
        continue
    ctime = time.strftime("%Y-%m-%d %H:%M",
                          time.localtime(meta.get('ctime')))
    print ctime, path[22:]

