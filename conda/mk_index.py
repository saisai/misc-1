import json

from conda.api import get_index


index = get_index()
for info in index.itervalues():
    del info['md5'], info['size']
    channel = info['channel']
    channel = channel.split('/')[-3]
    assert channel in ('pro', 'free', 'test-pkgs'), channel
    info['channel'] = channel

print len(index)

data = json.dumps(index, indent=2, sort_keys=True)
data = '\n'.join(line.rstrip() for line in data.split('\n'))
if not data.endswith('\n'):
    data += '\n'
with open('index.json', 'w') as fo:
    fo.write(data)
