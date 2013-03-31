"""
The implementation of this Sudoku solver is based on the paper:
https://www.lri.fr/~conchon/mpri/weber.pdf
"""
from pprint import pprint

import pycosat


def v(i, j, d):
    """
    return the number of the variable of cell i, j and digit d
    """
    return d + 9 * ((j - 1) + 9 * (i - 1))


def valid(cls, cells):
    """
    Append 324 clauses, corresponding to the 9 cells, to `cls`.
    The 9 cells are represented by a list tuples.  The new clauses
    ensure that the cells contain distinct values.
    """
    for i, xi in enumerate(cells):
        for j, xj in enumerate(cells):
            if i < j:
                for d in range(1, 10):
                    cls.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])


def mk_clauses():
    """
    Create (the 11745) Sudoku clauses, and return them as a list.
    """
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d) for d in range(1, 10)])
            # does not denote two different digits at once (36 clauses)
            for d in xrange(1, 10):
                for dp in xrange(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])

    # ensure rows and columns have distinct values
    for i in xrange(1, 10):
        valid(res, [(i, j) for j in range(1, 10)])
        valid(res, [(j, i) for j in range(1, 10)])
    # ensure 3x3 subgrids "regions" have distinct values
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            valid(res, [(i + k % 3, j + k / 3) for k in range(9)])

    assert len(res) == 81 * (1 + 36) + 27 * 324
    return res


def read_cell(sol, i, j):
    for d in xrange(1, 10):
        if v(i, j, d) in sol:
            return d


def solve(S):
    pprint(S)
    clauses = mk_clauses()
    print len(clauses)
    for i in xrange(1, 10):
        for j in xrange(1, 10):
            d = S[i-1][j-1]
            if d:
                clauses.append([v(i, j, d)])

    sol = set(pycosat.solve(clauses))
    #print sol
    for i in xrange(1, 10):
        for j in xrange(1, 10):
            S[i-1][j-1] = read_cell(sol, i, j)

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
