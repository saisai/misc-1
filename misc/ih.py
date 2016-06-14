import sys
import imp
from os.path import isfile, join


class Importer(object):

    def find_module(self, fullname, path=None):
        name = fullname.rsplit('.', 1)[-1]
        for dir_path in path or sys.path:
            self.path = join(dir_path, name + '.pye')
            if isfile(self.path):
                return self
        return None

    def load_module(self, fullname):
        print 'loading:', self.path
        mod = imp.new_module(fullname)
        mod.__file__ = self.path
        mod.__loader__ = self
        with open(self.path) as fi:
            code = fi.read()
        exec code in mod.__dict__
        #sys.modules[name] = mod
        return mod

sys.meta_path.append(Importer())

import bitarray
print bitarray

import porter
print porter
print porter.DATA
