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

<a href="https://github.com/ContinuumIO/pycosat/blob/master/examples/8queens.py">
Example code</a> to generate clauses


Sudoku problem:
===============

One variable for each digit (1..9) in each field: 729

<img src="http://3.bp.blogspot.com/_Kh0CZuWd0T8/Sn_y7ihXuyI/AAAAAAAAFC4/DB1NpTv3gbk/s400/printable+sudoku+%281%29.jpg">

11745 clauses

Extremely efficient (compared to backtracking algorithms), see
<a href="http://continuum.io/blog/sudoku>blog post</a>.

<a href="https://www.lri.fr/~conchon/mpri/weber.pdf">
"A SAT-based Sudoku solver" by Tjark Weber</a> (2005)

<a href="https://github.com/ContinuumIO/pycosat/blob/master/examples/sudoku.py">
Example code</a> to generate clauses


Install problem:
================

Find consistent set of packages to be installed given a requirement

  * packages with same name (usually) *conflict*
  * each package *depends* on other packages

Solution:

  * represent each package represented by Boolean
  * create clauses for conflicts and dependencies

<a href="http://www.cs.ucsd.edu/~lerner/papers/opium.pdf">
OPIUM: Optimal Package Install/Uninstall Manager</a>

<a href="https://github.com/ContinuumIO/pycosat/blob/master/examples/opium.py">
Example code</a> to generate clauses


Conda package manager and Anaconda:
===================================

<a href="https://github.com/ContinuumIO/conda">Conda</a>:

  * package manager
  * cross platform
  * multiple environments
  * build packages from recipes

<a href="http://continuum.io/downloads">Anaconda</a>:

  * free scientific Python distribution
  * uses conda package manager
  * Linux, Mac OS X, Windows


Summary:
========

  * SAT solvers provide real solutions for many industrial problems
  * Your problem only need to be *rephrased* as a Boolean problem
  * Many of-the-shelf SAT solvers available
  * When programming in Python, use PycoSAT (part of Anaconda)
