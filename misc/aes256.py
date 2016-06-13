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
    pad_len = ord(s[-1])
    assert 1 <= pad_len <= BS 
    return s[:-pad_len]

def encrypt(raw):
    raw = pad(raw)
    assert len(raw) % BS == 0
    iv = Random.new().read(BS)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(raw)

def decrypt(enc):
    assert len(enc) >= 2 * BS
    iv = enc[:BS]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[BS:]))

for n in range(1000):
    msg = Random.new().read(n)
    enc = encrypt(msg)
    #print('%d %d' % (len(msg), len(enc)))
    assert decrypt(enc) == msg

if len(sys.argv) == 2:
    path = sys.argv[1]
    if path.endswith('x'):
        with open(path, 'rb') as fi:
            enc = fi.read()
        with open(path[:-1], 'wb') as fo:
                fo.write(decrypt(enc))
    else:
        with open(path, 'rb') as fi:
            raw = fi.read()
        with open(path + 'x', 'wb') as fo:
            fo.write(encrypt(raw))
