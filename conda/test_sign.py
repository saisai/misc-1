import sign
import shutil
import tempfile
from os.path import join

from Crypto.PublicKey import RSA


PRIVATE_KEY = '''\
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDP2EHuYMftjf3dYODMif1s1eWj7+He5Y7LYaH27E6Kw3vr/yaY
6R6G1AjyAPD+7i13AjSjYPeNfNmTk99HbYJFIX3Mi+muS+7yOU9ItobZ/4btJbN/
HScR9jPKBv3V/1QEjhFbtNNUoeZz9xZYgbkDrJo4O4NaRivYsorIPxK37QIDAQAB
AoGAfEgABJ5ybiX9qyaGxUet9ipgyopiMXpqzEpxIslina8OpqtHVR/wVQbs4miV
spqRLRxwhVEyNbR2FbzSQk/FGKUi5aQ8Mmdc1MFSIOo3HeAa+BDk+qkQHtvpwjjW
2ifnPSR3yF+b9fkUKIA/6S34ktCBaKNW+G7lGbaQiIQ3fLECQQDbydWTMU0GecqU
Q3jG91mL46FOsr+3U/7MHZoJiPdb4AdMW7UaK1979rxpuAukOXTCuA97gtO3jjxV
ganOejGXAkEA8haq2/b4pduckH0gGgxnm1MTHI4rJXkiZfKOxjxh2Pw6AwrvYaMj
p1IJGkmEaAEbnngxV4+rcOvkxeiXriILGwJAbOqncSrkTco7DqAlEQxwjrc+L766
7QGt6b7dn84FLr1lQHzN0WsfBVJvakBvXHGwn/IQkhdyDatp0MHRwWWifwJBAKDI
GTX58u4EyxjTYWyrbGwmYn0GlvVOXGAlFlnmZH3+FnFK4+2OsfFAdLc2uG9yvOsk
nHCxBIX8xXYDoimOhp0CQQCBNBosaiAFPpN9p/yFwKY7eVfIOggqTEHcWE9OktdW
j9RIDhVSoSxhkGtO5Pyf2DX4yo7I9fvSoopqnrsRwsbn
-----END RSA PRIVATE KEY-----
'''

PUBLIC_KEY = '''\
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDP2EHuYMftjf3dYODMif1s1eWj
7+He5Y7LYaH27E6Kw3vr/yaY6R6G1AjyAPD+7i13AjSjYPeNfNmTk99HbYJFIX3M
i+muS+7yOU9ItobZ/4btJbN/HScR9jPKBv3V/1QEjhFbtNNUoeZz9xZYgbkDrJo4
O4NaRivYsorIPxK37QIDAQAB
-----END PUBLIC KEY-----
'''

SIGNATURE = 'Pb8+ax78X5lbyei7tThELaDkodwL5XdJ6uOGDZE6aBlzJZ89XhwP6GpePwsR0D45Z4MoESN75DP0IkIEU891t8y7RG1afGt5+6/RKBM8V4Xh8zCVvnIOszysNeXA2uI2AhoE+R62KzRt9GzSKTRm5qTgnUtJHKxZJ5UxuXRIc04='

def write_message(path):
    with open(path, 'wb') as fo:
        fo.write(b'This message needs to be signed.\n')

def test_sig2ascii():
    assert sign.sig2ascii(64) == 'QA=='
    assert sign.sig2ascii(1234567890123) == 'AR9x+wTL'

def test_ascii2sig():
    assert sign.ascii2sig('QA==') == 64
    assert sign.ascii2sig('AR9x+wTL') == 1234567890123

def test_sign():
    key = RSA.importKey(PRIVATE_KEY)
    tmp_dir = tempfile.mkdtemp()
    data_path = join(tmp_dir, 'data')
    write_message(data_path)
    assert sign.sign(data_path, key) == SIGNATURE

def test_verify():
    key = RSA.importKey(PRIVATE_KEY)
    tmp_dir = tempfile.mkdtemp()
    data_path = join(tmp_dir, 'data')
    write_message(data_path)
    assert sign.verify(data_path, key, SIGNATURE)

def test_roundabout():
    tmp_dir = tempfile.mkdtemp()
    key_path = join(tmp_dir, 'key')
    data_path = join(tmp_dir, 'data')
    write_message(data_path)
    sign.keygen(key_path)
    key = RSA.importKey(open('%s.priv' % key_path).read())
    sig = sign.sign(data_path, key)
    assert sign.verify(data_path, key, sig)
    shutil.rmtree(tmp_dir)
