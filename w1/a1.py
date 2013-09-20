import json
from pprint import pprint
from collections import defaultdict


with open('users.json') as fi:
    d = json.load(fi)

#print len(d)

inames = defaultdict(set)

n = 0
for user, files in d.iteritems():
    if not any(file.startswith('.anaconda') for file in files):
        n += 1
        continue

    for f in files:
        if not f.startswith('.anaconda/'):
            continue
        if f.startswith('.anaconda/.unionfs/'):
            continue
        s = f.split('/site-packages/')
        if len(s) == 2:
            spf = s[1].split('/')[0]
            inames[spf].add(user)

for spf in sorted(inames):
    users = inames[spf]
    if spf.endswith(('.egg-info', '.egg')):
        continue
    print '%4d  %s' % (len(users), spf)
