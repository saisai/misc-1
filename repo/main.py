from pprint import pprint
import json

from ll.diffutils import show_set_diff


index = json.load(open('index.json'))
repodata = json.load(open('repodata.json'))['packages']

print len(index), len(repodata)

for fn in sorted(index):
    info1 = index[fn]
    info2 = repodata[fn]
    dep1 = info1.get('depends', [])
    dep2 = info2['depends']
    if dep1 and dep1 != dep2:
        print fn
        show_set_diff(set(dep1), set(dep2))
