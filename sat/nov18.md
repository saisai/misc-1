SAT Solvers
===========

Austin Machine Learning Group
Ilan Schnell - November 18, 2013

Outline:
  * what is the SAT problem?
  * a brief history of SAT solvers
  * what problems can be translated into SAT problems?
  * Examples: 8 Queen, Sudoku, install problem
  * The conda package installer and Anaconda


What is the SAT problem?
========================

  * Boolean satisfiability problem
  * NP-complete problem
  * conjunctive normal form (CNF).  Example
      * (x1 ∨ ¬x5 ∨ x4) ∧ (¬x1 ∨ x5 ∨ x3 ∨ x4) ∧ (¬x3 ∨ ¬x4)
      * DIMACS cnf format
        <pre>p cnf 5 3
        1 -5 4 0
        -1 5 3 4 0
        -3 -4 0</pre>
      * (A) solution: x1 = x5 = True, x2 = x3 = x4 = False
