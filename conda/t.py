import json


d = {'abc': 123,
     'def': [u'a', str('b'), 'lkjiuh', 4]}

with open('about.json', 'w') as fo:
    json.dump(d, fo, indent=2, sort_keys=True)
