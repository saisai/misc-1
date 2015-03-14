import base64

from Crypto.PublicKey import RSA
from Crypto import Random


def long2bytes(i):
    ret = []
    while i:
        i, r = divmod(i, 256)
        ret.append(r)
    return ''.join(chr(n) for n in ret[::-1])

random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
private_key_text = key.exportKey()
public_key_text = key.publickey().exportKey()
print private_key_text
print public_key_text

k2 = RSA.importKey(private_key_text)
assert k2.publickey().exportKey() == public_key_text

x = key.sign('zxcvasdsdfhkj', '')[0]
print x
print base64.b64encode(long2bytes(x))
