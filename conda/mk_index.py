import json

from conda.api import get_index


index = get_index()
for info in index.itervalues():
    del info['channel'], info['md5'], info['size']


for fn in index.keys():
    if fn.startswith(('accelerate-', 'mkl-devel')):
        del index[fn]


data = json.dumps(index, indent=2, sort_keys=True)
data = '\n'.join(line.rstrip() for line in data.split('\n'))
if not data.endswith('\n'):
    data += '\n'
with open('index.json', 'w') as fo:
    fo.write(data)
