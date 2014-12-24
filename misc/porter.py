from bitarray import bitarray


DATA = """
01000111 01110010 01100101 01100001
01110100 01100101 01110010 00100000
01001100 01101001 01100110 01100101
00100000 01100110 01101111 01110010
00100000 01000001 01101100 01101100
"""

for s in DATA.split():
    print s, bitarray(s).tobytes()
