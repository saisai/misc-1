import json
from collections import defaultdict


d = defaultdict(list)


for line in open('sorted'):
    if not line.startswith("./w_"):
        continue
    s = line[4:].rstrip()
    #print s
    if '/' in s:
        user, file = line[4:].rstrip().split('/', 1)
        #if file.startswith('.anaconda/'):
            #print user, file
        d[user].append(file)

print len(d)

with open('users.json', 'w') as fo:
    json.dump(d, fo, indent=2, sort_keys=True)
