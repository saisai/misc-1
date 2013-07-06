#! /usr/bin/env python
from math import sqrt

class Prime:
    def __init__(self,limit):  # calculates the primes up to limit
        self.limit=limit
        self.L=[]              # list of primes
        self.isp=[False]*limit # is a prime number
        tmp=[True]*limit
        for i in xrange(2,limit):
            if tmp[i]: # i is prime
                self.L.append(i)
                self.isp[i]=True
                val = i
                while val < limit:
                    tmp[val] = False
                    val += i

    def isprime(self,n):
        if n < self.limit: return self.isp[n]
        if n%6 not in [1,5]: return False
        m=int(sqrt(n))
        i=0
        mi=len(self.L)
        while i<mi:
            d=self.L[i]
            if d>m: break
            if n%d==0: return False
            i+=1
        return True

def fac(n):
    if n==0: return 1
    return fac(n-1)*n

def bico(n,r):
    if r>n:
#        print 'r>n in bico'
        return 0
    return fac(n)/fac(r)/fac(n-r)

def getPerms(a):
    if len(a)==1:
        yield a
    else:
        for i in range(len(a)):
            this = a[i]
            rest = a[:i] + a[i+1:]
            for p in getPerms(rest):
                yield [this] + p

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


class Memoize:
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args, **keywords):
        key = (args, tuple(keywords.items()))
        if key not in self.cache:
            self.cache[key] = self.func(*args, **keywords)
        return self.cache[key]
