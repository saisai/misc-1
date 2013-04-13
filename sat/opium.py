from pprint import pprint

import pycosat

index = {
    'a': {'requires': ['b', 'c', 'z']},
    'b': {'requires': ['d']},
    'c': {'requires': ['d|e', 'f|g']},
    'd': {'conflicts': ['e']},
    'e': {'conflicts': ['d']},
    'f': {'conflicts': ['g']},
    'g': {'conflicts': ['f']},
    'y': {'requires': ['z']},
    'z': {},
}

v = {} # map names to variable numbers
w = {} # map variable numbers to names
for i, name in enumerate(index.iterkeys()):
    v[name] = i + 1
    w[i + 1] = name

clauses = []
def to_cnf(name):
    requires = index[name].get('requires', [])
    for r in requires:
        clauses.append([-v[name]] + [v[n] for n in r.split('|')])

    conflicts = index[name].get('conflicts', [])
    for c in conflicts:
        clauses.append([-v[name], -v[c]])

for name in index.iterkeys():
    to_cnf(name)

print v
clauses.append([v['a']])

pprint([' V '.join(('-' if i<0 else '') + w[abs(i)] for i in clause)
        for clause in clauses])

for sol in pycosat.itersolve(clauses):
    print sorted(w[i] for i in sol if i > 0)
