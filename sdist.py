"""\
Create a source tarball of a Python project from a (local) source tree.
All this command doing is packing up the source tree (ignoring .git,
.svn, .hg, *~, .pyc, etc... files), and giving the directory and the
tarball a good name (by calling setup.py --fullname).  This may be
overwritten using the --dst option.
"""
import os
import sys
from os.path import isfile
from optparse import OptionParser
from subprocess import Popen, PIPE
import tarfile


def exclude_func(path):
    if path.endswith(('~', '.pyc', '.pyo')):
        return True
    parts = path.split(os.sep)
    assert parts[0] == '.', path
    if len(parts) >= 2:
        if parts[1].startswith(('.git', '.hg')):
            return True
        if parts[1] in ('build', 'dist'):
            return True
        if '.svn' in parts:
            return True
    return False


def get_name_version(path='.'):
    cmd = [sys.executable, 'setup.py', '--fullname']
    p = Popen(cmd, cwd=path, stdout=PIPE, stderr=PIPE)
    fullname = p.communicate()[0].split()[-1]
    name, version = fullname.split('-')
    return dict(name=name, version=version.rstrip('.dev'))


def main():
    p = OptionParser(usage="usage: %prog [options]", description=__doc__)
    p.add_option("--dst", action="store")
    opts, args = p.parse_args()
    if opts.dst and not opts.dst.endswith('.tar.gz'):
        p.error('not a good name for a tarball: %s' % opts.dst)
    if args:
        p.error('no arguments expected')

    if not isfile('setup.py'):
        sys.exit("Error: no such file: setup.py")

    dst = opts.dst or '%(name)s-%(version)s.tar.gz' % get_name_version()
    assert dst.endswith('.tar.gz')
    print 'Creating:', dst
    t = tarfile.open(dst, 'w:gz')
    t.add('.', arcname=dst[:-7], exclude=exclude_func)
    t.close()


if __name__ == '__main__':
    main()
