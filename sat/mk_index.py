import json

from conda.api import get_index


index = get_index()
with open('index.json', 'w') as fo:
    json.dump(index, fo, indent=2, sort_keys=True)
