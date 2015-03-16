import sys
import base64
import hashlib

from Crypto.PublicKey import RSA
from Crypto import Random


py3k = bool(sys.version_info[0] == 3)


def sig2ascii(i):
    ret = []
    while i:
        i, r = divmod(i, 256)
        ret.append(r)
    if py3k:
        s = bytes(n for n in ret[::-1])
    else:
        s = ''.join(chr(n) for n in ret[::-1])
    return base64.b64encode(s).decode('utf-8')

def ascii2sig(s):
    res = 0
    for c in base64.b64decode(s):
        res *= 256
        res += (c if py3k else ord(c))
    return res

def keygen(path):
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    with open('%s.priv' % path, 'wb') as fo:
        fo.write(key.exportKey())
        fo.write(b'\n')
    with open('%s.pub' % path, 'wb') as fo:
        fo.write(key.publickey().exportKey())
        fo.write(b'\n')

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

    p.add_option('-k', '--keygen',
                 action="store_true",
                 help="generate a public-private key pair")

    p.add_option('-s', '--sign',
                 action="store_true",
                 help="sign FILE(s) using NAME.priv")

    p.add_option('-v', '--verify',
                 action="store_true",
                 help="verify a FILE(s) file using NAME.pub")

    opts, args = p.parse_args()

    if len(args) == 0:
        p.error('at least one argument (NAME) expected')

    keyname, files = args[0], args[1:]

    if opts.keygen:
        if files:
            p.error('only NAME expected for --keygen')
        keygen(keyname)
        return

    if opts.sign:
        key = RSA.importKey(open('%s.priv' % keyname).read())
        for f in files:
            print('signing:', f)
            sig = sign(f, key)
            with open('%s.sig' % f, 'w') as fo:
                fo.write(sig)
                fo.write('\n')

    if opts.verify:
        key = RSA.importKey(open('%s.pub' % keyname).read())
        for f in files:
            with open('%s.sig' % f) as fi:
                sig = fi.read().strip()
            print('%-70s %s' % (f, verify(f, key, sig)))


if __name__ == '__main__':
    main()
