import os
from subprocess import call
from os.path import join


prefix = join(os.getcwd(), 500 * 'a')[:260]
print len(prefix)

env = dict(os.environ)
env['CIO_TEST'] = '3'
call(['conda', 'create', '-p', prefix, 'openssl'], env=env)
