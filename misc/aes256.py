import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


assert AES.block_size == 16
BS = AES.block_size
KEY = hashlib.sha256('PassW0rd').digest()


def pad(s):
    pad_len = BS - len(s) % BS
    return s + pad_len * chr(pad_len)

def unpad(s):
    pad_len = ord(s[len(s)-1:])
    return s[:-pad_len]

def encrypt(raw):
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:BS]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[BS:])).decode('utf-8')


msg = "Hello World!1234"
print len(msg)
print repr(pad(msg))
print unpad(pad(msg))
enc = repr(encrypt(msg))
print enc
print decrypt(enc)
