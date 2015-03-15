import json
import shutil
import hashlib
import tarfile
import tempfile
from os.path import join

from Crypto.PublicKey import RSA

from ll.utils import tar_update


def info_m(t, m):
    if m.isfile():
        h = hashlib.new('sha256')
        f = t.extractfile(m.path)
        while True:
            chunk = f.read(262144)
            if not chunk:
                break
            h.update(chunk)
        return h.hexdigest()
    if m.isdir():
        return 'DIR'
    if m.issym():
        return '-> %s' % m.linkname
    return '<UNKNOWN>'

def list_t(t):
    for m in sorted(t.getmembers(), key=lambda m: m.path):
        if m.path == 'info/signatures.json':
            continue
        yield '%s %s\n' % (m.path, info_m(t, m))

def sha256_t(t):
    h = hashlib.new('sha256')
    for line in list_t(t):
        h.update(line)
    return h

def sign(path, name):
    key = RSA.importKey(open('%s.priv' % name).read())
    t = tarfile.open(path)
    h = sha256_t(t)
    signatures = {} # read from tar
    t.close()
    sig = key.sign(h.digest(), '')[0]
    signatures[name] = str(sig)

    tmp_dir = tempfile.mkdtemp()
    sig_path = join(tmp_dir, 'signatures.json')
    with open(sig_path, 'w') as fo:
        json.dump(signatures, fo, indent=2, sort_keys=True)
    tar_update(path, {'info/signatures.json': sig_path})
    shutil.rmtree(tmp_dir)


sign("python-2.7.4-1.tar.bz2", 'cio')
