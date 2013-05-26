import json
import unittest
from os.path import dirname, join

from resolve import MatchSpec, Package, Resolve



with open(join(dirname(__file__), 'index.json')) as fi:
    r = Resolve(json.load(fi))

f_mkl = set(['mkl'])


class TestMatchSpec(unittest.TestCase):

    def test_match(self):
        for mspec, res in [('numpy 1.7*', True),
                           ('numpy 1.7.1', True),
                           ('numpy 1.7', False),
                           ('numpy 1.5*', False),
                           ('numpy 1.6*|1.7*', True),
                           ('numpy 1.6*|1.8*', False),
                           ('numpy 1.6.2|1.7*', True),
                           ('numpy 1.6.2|1.7.1', True),
                           ('numpy 1.6.2|1.7.0', False),
                           ('numpy 1.7.1 py27_0', True),
                           ('numpy 1.7.1 py26_0', False),
                           ('python', False)]:
            m = MatchSpec(mspec)
            self.assertEqual(m.match('numpy-1.7.1-py27_0.tar.bz2'), res)

    def test_hash(self):
        a, b = MatchSpec('numpy 1.7*'), MatchSpec('numpy 1.7*')
        self.assertTrue(a is not b)
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))
        c, d = MatchSpec('python'), MatchSpec('python 2.7.4')
        self.assertNotEqual(a, c)
        self.assertNotEqual(hash(a), hash(c))


class TestPackage(unittest.TestCase):

    def test_llvm(self):
        ms = MatchSpec('llvm')
        pkgs = [Package(fn, r.index[fn]) for fn in r.find_matches(ms)]
        pkgs.sort()
        self.assertEqual([p.fn for p in pkgs],
                         ['llvm-3.1-0.tar.bz2',
                          'llvm-3.1-1.tar.bz2',
                          'llvm-3.2-0.tar.bz2'])

    def test_different_names(self):
        pkgs = [Package(fn, r.index[fn]) for fn in [
                'llvm-3.1-1.tar.bz2', 'python-2.7.5-0.tar.bz2']]
        self.assertRaises(ValueError, pkgs.sort)


class TestSolve(unittest.TestCase):

    def setUp(self):
        r.msd_cache = {}

    def test_iopro_nomkl(self):
        self.assertEqual(
            r.solve2(['iopro 1.4*', 'python 2.7*', 'numpy 1.7*'],
                     set()),
            ['iopro-1.4.3-np17py27_p0.tar.bz2',
             'numpy-1.7.1-py27_0.tar.bz2',
             'openssl-1.0.1c-0.tar.bz2',
             'python-2.7.5-0.tar.bz2',
             'readline-6.2-0.tar.bz2',
             'sqlite-3.7.13-0.tar.bz2',
             'system-5.8-1.tar.bz2',
             'tk-8.5.13-0.tar.bz2',
             'unixodbc-2.3.1-0.tar.bz2',
             'zlib-1.2.7-0.tar.bz2'])

    def test_iopro_mkl(self):
        self.assertEqual(
            r.solve2(['iopro 1.4*', 'python 2.7*', 'numpy 1.7*'],
                    f_mkl),
            ['iopro-1.4.3-np17py27_p0.tar.bz2',
             'mkl-rt-11.0-p0.tar.bz2',
             'numpy-1.7.1-py27_p0.tar.bz2',
             'openssl-1.0.1c-0.tar.bz2',
             'python-2.7.5-0.tar.bz2',
             'readline-6.2-0.tar.bz2',
             'sqlite-3.7.13-0.tar.bz2',
             'system-5.8-1.tar.bz2',
             'tk-8.5.13-0.tar.bz2',
             'unixodbc-2.3.1-0.tar.bz2',
             'zlib-1.2.7-0.tar.bz2'])

    def test_mkl(self):
        self.assertEqual(r.solve(['mkl'], set()),
                         r.solve(['mkl'], f_mkl))

    def test_accelerate(self):
        self.assertEqual(
            r.solve(['accelerate'], set()),
            r.solve(['accelerate'], f_mkl))

    def test_anaconda_nomkl(self):
        dists = r.solve(['anaconda 1.5.0', 'python 2.7*', 'numpy 1.7*'])
        self.assertEqual(len(dists), 107)
        self.assertTrue('scipy-0.12.0-np17py27_0.tar.bz2' in dists)

    def test_anaconda_mkl_2(self):
        # to test "with_features_depends"
        dists = r.solve(['anaconda 1.5.0', 'python 2.7*', 'numpy 1.7*'],
                        f_mkl)
        self.assertTrue('scipy-0.12.0-np17py27_p0.tar.bz2' in dists)
        self.assertTrue('mkl-rt-11.0-p0.tar.bz2' in dists)
        self.assertEqual(len(dists), 108)

        dists2 = r.solve(['anaconda 1.5.0',
                          'python 2.7*', 'numpy 1.7*', 'mkl'])
        self.assertTrue(set(dists).issubset(set(dists2)))
        self.assertEqual(len(dists2), 110)

    def test_anaconda_mkl_3(self):
        # to test "with_features_depends"
        dists = r.solve(['anaconda 1.5.0', 'python 3*'], f_mkl)
        self.assertTrue('scipy-0.12.0-np17py33_p0.tar.bz2' in dists)
        self.assertTrue('mkl-rt-11.0-p0.tar.bz2' in dists)
        self.assertEqual(len(dists), 61)


class TestFindSubstitute(unittest.TestCase):

    def setUp(self):
        r.msd_cache = {}

    def test1(self):
        installed = r.solve(['anaconda 1.5.0', 'python 2.7*', 'numpy 1.7*'],
                            features=f_mkl)
        for old, new in [('numpy-1.7.1-py27_p0.tar.bz2',
                          'numpy-1.7.1-py27_0.tar.bz2'),
                         ('scipy-0.12.0-np17py27_p0.tar.bz2',
                          'scipy-0.12.0-np17py27_0.tar.bz2'),
                         ('mkl-rt-11.0-p0.tar.bz2', None)]:
            self.assertTrue(old in installed)
            self.assertEqual(r.find_substitute(old, installed, f_mkl), new)


if __name__ == '__main__':
    unittest.main()
