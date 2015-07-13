import base64

from Crypto.Signature import PKCS1_PSS
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random



def keygen(path):
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    with open('%s.priv' % path, 'wb') as fo:
        fo.write(key.exportKey())
        fo.write(b'\n')
    with open('%s.pub' % path, 'wb') as fo:
        fo.write(key.publickey().exportKey())
        fo.write(b'\n')

def hash_file(path):
    h = SHA256.new()
    with open(path, 'rb') as fi:
        while True:
            chunk = fi.read(262144)
            if not chunk:
                break
            h.update(chunk)
    return h

def sign(path, key):
    signer = PKCS1_PSS.new(key)
    sig = signer.sign(hash_file(path))
    return base64.b64encode(sig).decode('utf-8')

def verify(path, key, sig):
    verifier = PKCS1_PSS.new(key)
    return verifier.verify(hash_file(path), base64.b64decode(sig))

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
