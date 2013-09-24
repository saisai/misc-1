from bitarray import bitarray


def f(s):
    s = s.replace(' ', '')
    a = bitarray(s)
    print a
    b = a.tobytes()
    print repr(b)
    c = b.decode('utf-8')
    print repr(c)
    print c

f('010 00001')
f('110 01111  10 000001')
f('1110 0111  10 000001  10 100111')
