import json
from collections import defaultdict


with open('/home/ilan/anaconda/repo/filedb.json') as fi:
    d = json.load(fi)

NAMES = defaultdict(int)

for files in d.itervalues():
    for f in files:
        if f.startswith('info/'):
            name = f.split('/')[1]
            NAMES[name] += 1

for name in sorted(NAMES):
    print name, NAMES[name]
