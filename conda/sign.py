import base64
import hashlib

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

def keygen(name):
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    with open('%s.priv' % name, 'w') as fo:
        fo.write(key.exportKey())
        fo.write('\n')
    with open('%s.pub' % name, 'w') as fo:
        fo.write(key.publickey().exportKey())
        fo.write('\n')

def hash_file(path):
    h = hashlib.new('sha256')
    with open(path, 'rb') as fi:
        while True:
            chunk = fi.read(262144)
            if not chunk:
                break
            h.update(chunk)
    return h.digest()

def sign(path, key):
    return sig2ascii(key.sign(hash_file(path), '')[0])

def verify(path, key, sig):
    return key.verify(hash_file(path),
                      (ascii2sig(sig),))

def main():
    from optparse import OptionParser

    p = OptionParser(
        usage="usage: %prog [option] NAME [FILE ...]",
        description="tool for signing")

    p.add_option('--keygen',
                 action="store_true",
                 help="generate a public-private key pair")

    p.add_option('--sign',
                 action="store_true",
                 help="sign FILE(s) using NAME.priv")

    p.add_option('--verify',
                 action="store_true",
                 help="verify a FILE(s) file using NAME.pub")

    opts, args = p.parse_args()

    if len(args) == 0:
        p.error('at least one argument (NAME) expected')

    keyname, files = args[0], args[1:]

    if opts.keygen:
        keygen(keyname)
        return

    if opts.sign:
        key = RSA.importKey(open('%s.priv' % keyname).read())
        for f in files:
            sig = sign(f, key)
            with open('%s.sig' % f, 'w') as fo:
                fo.write(sig)

    if opts.verify:
        key = RSA.importKey(open('%s.pub' % keyname).read())
        for f in files:
            with open('%s.sig' % f) as fi:
                sig = fi.read().strip()
            print verify(f, key, sig)


if __name__ == '__main__':
    main()
