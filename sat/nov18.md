SAT Solvers
===========

Austin Machine Learning Group
Ilan Schnell - November 18, 2013

Outline:
  * what is the SAT problem?
  * a brief history of SAT solvers
  * what problems can be translated into SAT problems?
  * examples: 8 Queen, Sudoku, install problem
  * the conda package installer and Anaconda
  * summary


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

Many of-the-shelf Solvers:
  * PicoSAT (C with Python bindings pycosat)
  * MiniSAT (C++)
  * RSat, BooleForce, SATzilla, ...


8 Queens problem:
=================

One variable per checker board field (Queen = True; no Queen = False) = 64
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
Clauses:
  * rows or columns 16 * (1 + 28)
  * diagonal clauses 280
  * total: 744

<a href="https://github.com/ContinuumIO/pycosat/blob/master/examples/8queens.py">Exmaple code to generate clauses</a>


Sudoku problem:
===============

One variable for each digit (1..9) in each field: 729

<img src="http://3.bp.blogspot.com/_Kh0CZuWd0T8/Sn_y7ihXuyI/AAAAAAAAFC4/DB1NpTv3gbk/s400/printable+sudoku+%281%29.jpg">

11745 clauses

<a href="https://www.lri.fr/~conchon/mpri/weber.pdf">
"A SAT-based Sudoku solver" by Tjark Weber</a>

<a href="https://github.com/ContinuumIO/pycosat/blob/master/examples/sudoku.py">Exmaple code to generate clauses</a>


Install problem:
================

  * each package represented by boolean


Conda package manager and Anaconda:
===================================


Summary:
========

  *
