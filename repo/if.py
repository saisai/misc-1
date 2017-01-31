import json
from collections import defaultdict


with open('/home/ilan/anaconda/repo/filedb.json') as fi:
    d = json.load(fi)

names = defaultdict(int)

for files in d.itervalues():
    for f in files:
        if f.startswith('info/'):
            names[f] += 1

for f in sorted(names):
    print f, names[f]
