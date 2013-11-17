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
      * A solution is: x1 = x5 = True, x2 = x3 = x4 = False
      * DIMACS cnf format
        <pre>p cnf 5 3
        1 -5 4 0
        -1 5 3 4 0
        -3 -4 0</pre>


A brief history of SAT solvers:
===============================

  * In the 80's: reduce it to SAT - This will show that nobody can solve it!
  * 21th century: reduce it to SAT - This means you can solve it in practice!

Reason:
  * dramatic progress in SAT solvers
  * not due to better hardware but mostly due to better algorithms
  * 100 variables and 200 constraints (early 90's)
  * 1 million variables and 5 million constraints (today)
  * (one can encode quite a bit in a million variables)


8 Queens problem:
=================

Encoding the 8 queens problem.  One variable per checker board field (Queen = True - no Queen = False)
<pre>
......Q.
...Q....
.Q......
....Q...
.......Q
Q.......
..Q.....
.....Q..
</pre>

