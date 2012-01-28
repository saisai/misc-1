for i in xrange(5):
    print 2 * i == i + i

print "HEJ"

def fac(n):
    return 1 if n < 2 else fac(n - 1) * n

print fac(2) == 2

print "AJK"

t = 1
for n in xrange(5):
    if n >= 1:
        t = t * n
    print fac(n) == t

x = 8
def chx(y):
    global x
    x = y
chx(19)
print x == 19

print divmod(x, 7) == (2, 5)

def add(x, y=7):
    return x + y
print add(x=3) == 10
print add(4) == 11
print add(12, 5) == 17

lst = [2, 5, 8]
print lst[1:] == [5, 8][:]
print lst[1:2] == [5]
print lst[:2] == [2, 5]

lst[1:] = [50, 60]
print lst == [2, 50, 60]

del lst[-1:]
print lst == [2, 50]

lst[:] = [77]
print lst == [77]

d = {1: 'a', 2: 'b'}
print d[1] == 'a'
del d[1]
print len(d) == 1

for i in xrange(10):
    lst = [2, 3, 5]
    lst[1] = 4
    assert lst == [2, 4, 5]
    lst[1:] = [7]
    assert lst == [2, 7]
    del lst[:1]
    del lst

print [i*i for i in xrange(5) if i != 3] == [0, 1, 4, 16]
