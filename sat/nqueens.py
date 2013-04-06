from pprint import pprint

import pycosat


N = 8


def v(i, j):
    assert 0 <= i < N
    assert 0 <= j < N
    return N * i + j + 1


def queens_clauses():
    allN = range(N)

    def one(vs, eq=False):
        if eq:
            yield list(vs)
        for v1 in vs:
            for v2 in vs:
                if v1 < v2:
                    yield [-v1, -v2]

    res = []
    for i in allN:
        res.extend(one([v(i, j) for j in allN], True))
        res.extend(one([v(j, i) for j in allN], True))
    # diagonal
    for i in range(N - 1):
        res.extend(one([v(j, i + j) for j in xrange(N - i)]))
    for i in range(1, N - 1):
        res.extend(one([v(j + i, j) for j in xrange(N - i)]))
    for i in range(N - 1):
        res.extend(one([v(j, N - 1 - (i + j)) for j in xrange(N - i)]))
    for i in range(1, N - 1):
        res.extend(one([v(j + i, N - 1 - j) for j in xrange(N - i)]))

    return res


def solve(n):
    global N
    N = n
    clauses = queens_clauses()

    # solve the SAT problem
    sol = set(pycosat.solve(clauses))
    for i in range(N):
        print ''.join('Q' if v(i, j) in sol else '.' for j in range(N))
    print n, len(clauses)


if __name__ == '__main__':
    for n in range(10, 110, 10):
        solve(n)
