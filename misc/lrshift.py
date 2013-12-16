from bitarray import bitarray


def lshift(a):
    a.append(a.pop(0))

def rshift(a):
    a.insert(0, a.pop())

if __name__ == '__main__':
    a = bitarray('0111011010111')
    print a
    lshift(a)
    print a
    rshift(a)
    print a
