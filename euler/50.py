#! /usr/bin/env python
from lib import Prime

P=Prime(1000000)

ls=0
for s in range(len(P.L)-2000):
    r=P.L[s]
    for t in range(1, 2000):
        r += P.L[s+t]
        if r>1000000: break
        if P.isprime(r):
            if t+1 > ls:
                print r, t+1
                ls = t+1
