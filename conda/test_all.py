import unittest

from resolve import Resolve, get_index


r = Resolve(get_index())
installed = r.solve2({'anaconda-1.5.0-np17py27_0.tar.bz2'}, set())
f_mkl = set(['mkl'])

class TestSelectRoot(unittest.TestCase):

    def test_python(self):
        self.assertEqual(r.select_root_dists(['python'], set(), []),
                         set(['python-3.3.2-0.tar.bz2']))

        self.assertEqual(r.select_root_dists(['python=2'], set(), installed),
                         set(['python-2.7.5-0.tar.bz2']))

        self.assertEqual(r.select_root_dists(['python=3'], set(), installed),
                         set(['python-3.3.2-0.tar.bz2']))

    def test_pycosat(self):
        self.assertEqual(r.select_root_dists(['pycosat'], set(), installed),
                         set(['pycosat-0.6.0-py27_0.tar.bz2']))

    def test_numpy(self):
        self.assertEqual(r.select_root_dists(['numpy'], set(), installed),
                         set(['numpy-1.7.1-py27_0.tar.bz2']))

        self.assertEqual(r.select_root_dists(['numpy'], f_mkl, installed),
                         set(['numpy-1.7.1-py27_p0.tar.bz2']))

    def test_anaconda(self):
        self.assertEqual(r.select_root_dists(['anaconda'], set(), installed),
                         set(['anaconda-1.5.0-np17py27_0.tar.bz2']))

        self.assertEqual(r.select_root_dists(['anaconda', 'python=3'],
                                           set(), installed),
                         set(['anaconda-1.5.0-np17py33_0.tar.bz2',
                              'python-3.3.1-0.tar.bz2']))

        self.assertEqual(r.select_root_dists(['anaconda=1.4',
                                              'python=2.6',
                                              'numpy=1.6'],
                                           set(), installed),
                         set(['anaconda-1.4.0-np16py26_0.tar.bz2',
                              'python-2.6.8-6.tar.bz2',
                              'numpy-1.6.2-py26_3.tar.bz2']))

class TestSolve(unittest.TestCase):

    def test_iopro(self):
        self.assertEqual(r.solve(['iopro'], installed),
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

        self.assertEqual(r.solve(['iopro'], installed, f_mkl),
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
        self.assertEqual(r.solve(['mkl'], installed, set()),
                         r.solve(['mkl'], installed, f_mkl))

    def test_accelerate(self):
        self.assertEqual(r.solve(['accelerate'], installed, set()),
                         r.solve(['accelerate'], installed, f_mkl))

if __name__ == '__main__':
    unittest.main()
