import os
from subprocess import call
from os.path import join


prefix = join(os.getcwd(), 500 * 'a')[:260]
print len(prefix)

call(['conda', 'create', '-p', prefix, 'openssl'])
