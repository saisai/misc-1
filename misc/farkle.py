import itertools


tot = 0
n = 0

for x in itertools.product(range(1, 7), repeat=6):
    tot += 1
    if sorted(x) == range(1, 7):
        n += 1

print n, tot, 1.0 * tot / n
print 1*2*3*4*5*6, 6**6
