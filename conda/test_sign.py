import sign
import shutil
import tempfile
from os.path import join

from Crypto.PublicKey import RSA


def test_sig2ascii():
    assert sign.sig2ascii(64) == b'QA=='
    assert sign.sig2ascii(1234567890123) == b'AR9x+wTL'

def test_ascii2sig():
    assert sign.ascii2sig(b'QA==') == 64
    assert sign.ascii2sig(b'AR9x+wTL') == 1234567890123

def test_roundabout():
    tmp_dir = tempfile.mkdtemp()

    data_path = join(tmp_dir, 'data')
    with open(data_path, 'wb') as fo:
        fo.write(b'ASDF\n')

    key_path = join(tmp_dir, 'key')
    sign.keygen(key_path)
    key = RSA.importKey(open('%s.priv' % key_path).read())
    sig = sign.sign(data_path, key)
    assert sign.verify(data_path, key, sig)
    shutil.rmtree(tmp_dir)
