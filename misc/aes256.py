import sys
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


BS = AES.block_size
assert BS == 16
KEY = hashlib.sha256(b'PassW0rd').digest()


def pad(s):
    pad_len = BS - len(s) % BS
    if sys.version_info[0] == 2:
        return s + pad_len * chr(pad_len)
    else: # Py3k
        return s + bytes(pad_len * [pad_len])

def unpad(s):
    pad_len = ord(s[len(s)-1:])
    return s[:-pad_len]

def encrypt(raw):
    raw = pad(raw)
    iv = Random.new().read(BS)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(raw)

def decrypt(enc):
    iv = enc[:BS]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[BS:]))


for n in range(2000):
    msg = Random.new().read(n)
    enc = encrypt(msg)
    #print('%d %d' % (len(msg), len(enc)))
    assert decrypt(enc) == msg
