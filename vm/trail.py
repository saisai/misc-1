from __future__ import generators
import os
assert os
print os.getcwd()

def generator():
    for i in xrange(5):
        yield (i*2)

#for i in generator():
#    print i

def makeAdder(base):
    def adder(x):
        return base + x
    return adder

add5 = makeAdder(5)
assert add5(6) == 11

class Foo:
    x = 1
    def __init__(self, y):
        self.y = y
    def add(self, z):
        return self.x + self.y + z

f = Foo(2)
assert f.add(3) == 6
assert Foo.add(f, 4) == 7
print "done"
