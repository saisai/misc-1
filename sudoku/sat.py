# https://www.lri.fr/~conchon/mpri/weber.pdf
from pprint import pprint

import pycosat


def v(i, j, d):
    "return the number of the variable of cell i, j and d"
    assert 1 <= i <= 9
    assert 1 <= j <= 9
    assert 1 <= d <= 9
    return d + 9 * ((j - 1) + 9 * (i - 1))

def valid(cls, cells):
    for d in xrange(1, 10):
        cls.append([v(i, j, d) for i, j in cells])

def lemma1(cls, cells):
    for i, xi in enumerate(cells):
        for j, xj in enumerate(cells):
            if i < j:
                for d in xrange(1, 10):
                    cls.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

def mk_clauses():
    res = []
    for i in xrange(1, 10):
        for j in xrange(1, 10):
            # ensure that cell denotes (at least) one of the 9 digits
            res.append([v(i, j, d) for d in xrange(1, 10)])
            # ensure a cell does not denote two different digits at once
            for d in xrange(1, 10):
                for dp in xrange(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])
    # sudoku
    for i in xrange(1, 10):
        lemma1(res, [(i, j) for j in xrange(1, 10)])
    for j in xrange(1, 10):
        lemma1(res, [(i, j) for i in xrange(1, 10)])
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            lemma1(res, [(i + k % 3, j + k / 3) for k in xrange(9)])
    return res

def solve(S):
#    pprint(S)
    cnf = mk_clauses()
    print len(cnf)
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
