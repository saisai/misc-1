import os
from os.path import basename, join, isfile, isdir
from optparse import OptionParser


ASCII_ONLY = False


def cleanup(data, expand_tabs=True):
    if data == '':
        return ''

    data = data.replace('\r', '')
    data = '\n'.join(line.rstrip() for line in data.split('\n'))
    if expand_tabs:
        data = data.expandtabs()

    if ASCII_ONLY:
        allowed = set('\t\n' + ''.join(chr(n) for n in xrange(32, 127)))
        data = ''.join(c for c in data if c in allowed)

    # make sure we have newline at the end
    if not data.endswith('\n'):
        data += '\n'

    return data


def clean_file(path, dry_run=False):
    if not isfile(path):
        print "Ignoring non-existing file:", path
        return
    with open(path) as fi:
        old_data = fi.read()
    new_data = cleanup(old_data, 'makefile' not in basename(path).lower())
    if new_data == old_data:
        return
    if dry_run:
        print "Dry-run: rewriting", path
        return
    print "Rewriting", path
    with open(path, 'wb') as fo:
        fo.write(new_data)


def clean_dir(dir_path, dry_run=False):
    if not isdir(dir_path):
        print "Not a directory:", dir_path
        return
    for root, dirs, files in os.walk(dir_path):
        parts = root.split(os.sep)
        if '.svn' in parts or '.git' in parts:
            continue
        for fn in files:
            if fn.endswith(('.py', '.txt', '.c', '.pyx', '.pxi')):
                path = join(root, fn)
                clean_file(path, dry_run)


def main():
    p = OptionParser(
        usage="usage: %prog [options] FILE [FILE ...]",
        description=("Cleanup whitespace in FILE, that is: "
                     "remove carriage returns; "
                     "remove excess whitespace at the end of each line; "
                     "expand tabs (to 8 spaces), but not a Makefile; "
                     "make sure file has a newline at the end"))

    p.add_option("--ascii-only",
        action="store_true",
        help="allow only ASCII bytes (removes others)")

    p.add_option('-n', "--dry-run",
        action="store_true",
        help="show which files would have been rewritten")

    p.add_option('-r', "--recur",
        action="store_true",
        help="cleanup recursively")

    opts, args = p.parse_args()

    global ASCII_ONLY
    ASCII_ONLY = opts.ascii_only

    if opts.recur:
        if len(args) == 0:
            args = ['.']
        for path in args:
            clean_dir(path, opts.dry_run)
    else:
        for path in args:
            clean_file(path, opts.dry_run)


if __name__ == '__main__':
    main()
