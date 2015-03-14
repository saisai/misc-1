import base64

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random


def sig2ascii(i):
    ret = []
    while i:
        i, r = divmod(i, 256)
        ret.append(r)
    return base64.b64encode(''.join(chr(n) for n in ret[::-1]))

def ascii2sig(s):
    res = 0
    for c in base64.b64decode(s):
        res *= 256
        res += ord(c)
    return res

random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
private_key_text = key.exportKey()
public_key_text = key.publickey().exportKey()
print private_key_text
print public_key_text

k2 = RSA.importKey(private_key_text)
assert k2.publickey().exportKey() == public_key_text

cnt = 0
while 1:
    cnt += 1
    data = Random.new().read(100)
    hash = SHA256.new(data).digest()
    sig = key.sign(hash, '')[0]
    #print sig
    s = sig2ascii(sig)
    #print s
    assert ascii2sig(s) == sig, sig
    assert key.verify(hash, (ascii2sig(s),))
    print cnt
