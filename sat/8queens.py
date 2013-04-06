import pycosat

N = 8
allN = range(N)


def v(i, j):
    return N * i + j + 1

def to_cnf(vs, eq=False):
    if eq:
        yield list(vs)
    for v1 in vs:
        for v2 in vs:
            if v1 < v2:
                yield [-v1, -v2]

def queens_clauses():
    res = []
    # rows and columns
    for i in allN:
        res.extend(to_cnf([v(i, j) for j in allN], True))
        res.extend(to_cnf([v(j, i) for j in allN], True))
    # diagonal
    for i in range(N - 1):
        res.extend(to_cnf([v(j, i + j) for j in range(N - i)]))
    for i in range(1, N - 1):
        res.extend(to_cnf([v(j + i, j) for j in range(N - i)]))
    for i in range(N - 1):
        res.extend(to_cnf([v(j, N - 1 - (i + j)) for j in range(N - i)]))
    for i in range(1, N - 1):
        res.extend(to_cnf([v(j + i, N - 1 - j) for j in range(N - i)]))

    return res

def solve():
    clauses = queens_clauses()

    # solve the SAT problem
    for sol in pycosat.itersolve(clauses):
        sol = set(sol)
        for i in range(N):
            print ''.join('Q' if v(i, j) in sol else '.' for j in range(N))
        print

if __name__ == '__main__':
    solve()
