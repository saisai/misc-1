import hashlib
from Crypto import Random
from Crypto.Cipher import AES


BS = AES.block_size
assert BS == 16
KEY = hashlib.sha256('PassW0rd').digest()


def pad(s):
    pad_len = BS - len(s) % BS
    return s + pad_len * chr(pad_len)

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
    return unpad(cipher.decrypt(enc[BS:])).decode('utf-8')


for n in range(20):
    msg = ''.join(chr(i) for i in range(n))
    print len(msg),
    enc = encrypt(msg)
    print len(enc)
    assert decrypt(enc) == msg
