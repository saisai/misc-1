import sys
from distutils.core import setup
from distutils.extension import Extension


sys.argv[1:] = ['build_ext', '--inplace']
setup(name="spam", ext_modules=[Extension("spam", ["spam.c"])])

from random import randint
import spam

for dummy in xrange(1000000):
    a = randint(0, 100)
    b = randint(0, 100)
    c = spam.foo(a, b)
    assert c == a + b

print spam.foo(42, 1)
print spam.foo(3, 4)
