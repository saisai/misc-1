from dateutil.parser import parse
from pylab import plot, show


t0 = parse('2012-09-11')

res = []
for line in open('dates.txt'):
    d, c = line.split()
    t1 = parse(d)
    res.append(((t1 - t0).days, c))

plot(res)
show()
