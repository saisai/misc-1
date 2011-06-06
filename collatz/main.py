m = 0
for i in xrange(3, 67108864, 2):
    n = i
    while n >= i:
        n = 3 * n + 1 if n % 2 else n / 2
        if n > m:
            m = n

print m
