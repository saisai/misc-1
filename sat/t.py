import sys
from pprint import pprint

from sudoku import sudoku_clauses

import pycosat


def write_cnf(clauses, path):
    n_vars = max(max(abs(lit) for lit in clause)
                 for clause in clauses)
    with open(path, 'w') as fo:
        fo.write('p cnf %d %d\n' % (n_vars, len(clauses)))
        for clause in clauses:
            for lit in clause:
                fo.write('%d ' % lit)
            fo.write('0\n')


write_cnf(sudoku_clauses(), 'sudoku.cnf')
