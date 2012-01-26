
a = 1

def mkadder(n):
    b = 2
    def adder(m):
        c = 3 + b
        return n + m
    
    return adder


print mkadder(3)(4)
