from pprint import pprint
from copy import deepcopy

import pycosat


def v(i, j, d):
    "return the number of the variable of cell i, j and d"
    assert 1 <= i <= 9
    assert 1 <= j <= 9
    assert 1 <= d <= 9
    return d + 9 * ((j - 1) + 9 * (i - 1))

def cls_valid(cells):
    assert len(cells) == 9
    cls = []
    for d in xrange(1, 10):
        cls.append([v(i, j, d) for i, j in cells])
    return cls

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
    # sudoku
    for i in xrange(1, 10):
        cnf.extend(cls_valid([(i, j) for j in xrange(1, 10)]))
    for j in xrange(1, 10):
        cnf.extend(cls_valid([(i, j) for i in xrange(1, 10)]))
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            cnf.extend(cls_valid([(i,   j), (i,   j+1), (i,   j+2),
                                  (i+1, j), (i+1, j+1), (i+1, j+2),
                                  (i+2, j), (i+2, j+1), (i+2, j+2)]))
    return cnf

def solve(S):
#    pprint(S)
    cnf = mk_clauses()
    for i in xrange(1, 10):
        for j in xrange(1, 10):
            d = S[i-1][j-1]
            if d:
                cnf.append([v(i, j, d)])
    sol = pycosat.solve(cnf)
    #print sol
    for i in xrange(1, 10):
        for j in xrange(1, 10):
            d = 0
            for dp in xrange(1, 10):
                if v(i, j, dp) in sol:
                    d = dp
                    break
            S[i-1][j-1] = d
    #pprint(cnf)
    #print len(list(pycosat.itersolve(cnf)))
    pprint(S)

Result = 0
fi=open('hard.dat')
for grid in range(1):
    if fi.readline()[0:4] != 'Grid':
        raise 'Error while reading.'
    M=[]
    for j in range(9):
        M.append([int(c) for c in fi.readline().strip()])
    solve(M)
    Result += 100 * M[0][0] + 10 * M[0][1] + M[0][2]
fi.close()
print Result
