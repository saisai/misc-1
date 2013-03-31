from pprint import pprint
from copy import deepcopy

import pycosat


def v(i, j, d):
    "return the number of the variable of cell i, j and d"
    assert 1 <= i <= 9
    assert 1 <= j <= 9
    assert 1 <= d <= 9
    return d + 9 * ((j - 1) + 9 * (i - 1))

def mk_clauses():
    cnf = []
    for i in xrange(1, 10):
        for j in xrange(1, 10):
            # ensure that cell denotes (at least) one of the 9 digits
            cnf.append([v(i, j, d) for d in xrange(1, 10)])
            # ensure a cell does not denote two different digits at once
            for d in xrange(1, 10):
                for dp in xrange(d + 1, 10):
                    cnf.append([-v(i, j, d), -v(i, j, dp)])
    # Lemma 1
    #...
    cnf=[]
    for i in xrange(1, 10):
        for j in xrange(i + 1, 10):
            for d in xrange(1, 10):
                cnf.append([-v(i, j, d), -v(i, j, dp)]) # ???
    print(len(cnf))
#    pprint(cnf)
    return cnf


def solve(S):
    pprint(S)
    cnf = mk_clauses()

    return
    for sol in pycosat.itersolve(cnf):
        print sol
    #pprint(S)


Result = 0
fi=open('euler.dat')
for grid in range(1):
    if fi.readline()[0:4] != 'Grid':
        raise 'Error while reading.'
    M=[]
    for j in range(9):
        M.append([int(c) for c in fi.readline().strip()])
    solve(M)
fi.close()
#print Result
