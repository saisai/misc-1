from dateutil.parser import parse


for line in open('op.txt'):
    if line and line[0].isdigit():
        v, d1, d2 = line.split()[:3]
        delta = parse(d2) - parse(d1)
        print '%10s %s %s %s' % (v, d1, d2, delta)
