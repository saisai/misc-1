#!/usr/bin/env python
"""\
Usage: passwdmgr [-f File] | [template]

This program manages password for a list of accounts in a secure way.

Options:
    -f, --file File   Explicitly specify the password template file,
                      the defualt is ~/.passwdmgr

    -h, --help        Print this info and exit.

    -t                Perform some self tests and exit.

The template format:

     typ   |   output character selected from
    -------+------------------------------------
     '9'   |   0..9
     'a'   |   a..z
     'A'   |   a..z + A..Z
     'x'   |   0..9 + a..z
     'X'   |   0..9 + a..z + A..Z
     'p'   |   punctuation
     'z'   |   punctuation + 0..9 + a..z
     'Z'   |   punctuation + 0..9 + a..z + A..Z
     ' '   |   whitespace

To create a one-time password:
$ ./passwdmgr aaa99aaa
zms32rml

With no arguments, you will enter the manager itself.
"""
__author__ = 'Ilan Schnell <ilanschnell@gmail.com>'
__copyright__ = '(c) Ilan Schnell, 2007'
__license__ = 'GNU GPL 2'
__version__ = '0.1'

import os
import re
import sys
import hashlib
import string
import getopt
from getpass import getpass
from os.path import expanduser

SLOW = 2 ** 14

def char(typ, hashin):
    """
    Returns one character which is calculated from the md5sum
    of the string `hashin`.
    The string `typ` determines the type of character the output
    should be.

    Examples:
    >>> char('9', 'some text from which only the md5sum is calculated.')
    '2'
    >>> ''.join(char('Z', 'foo:'+str(n)) for n in xrange(20))
    'k,2wy-SBt%yl3PQiujhb'
    """
    pool=''
    if typ in 'aAxXzZ': pool += string.ascii_lowercase
    if typ in 'AXZ':    pool += string.ascii_uppercase
    if typ in '9xXzZ':  pool += string.digits
    if typ in 'pzZ':    pool += '!@#$%^&-+=;:,.'
    if pool == '':
        pool = typ
    r = hashin
    for _ in xrange(SLOW):
        r = hashlib.sha512(r).digest()
    return pool[long(hashlib.md5(r).hexdigest(), 16) % len(pool)]


MASTER = ''
def passwd(tmpl, hashin):
    """
    Returns a password which is calculated from the md5sum
    of the string `hashin`.
    The string `tmpl` is a template which describes the form of the password.

    Example:
    >>> tmpl = '999 aaa AAAAAA xxxxxx XXXXXX pppp zzzzzz ZZZZZZZZZZ'
    >>> ''.join(passwd(tmpl, 'g'))
    '131 wuo mympmK 3swcih Fb5lYA ..%, 5-1;kf jkKkJ;06f0'
    """
    for i, t in enumerate(tmpl):
        yield char(t, hashin + str(i) + MASTER)


def output_password(tmpl, hashin):
    for c in passwd(tmpl, hashin):
        sys.stdout.write(c)
        sys.stdout.flush()
    sys.stdout.write('\n')


line_pat = re.compile(r'(.+?)\s+(\w+)(?:\s*#.*)?$')
def parse_line(line):
    """
    >>> parse_line('foo  bar ## Comment')
    ('foo', 'bar')
    >>> parse_line('foo  bar  baz')
    ('foo  bar', 'baz')
    """
    m = line_pat.match(line)
    if not m:
        sys.exit('Error: could not parse: %r' % line)
    return m.groups()

def parse(filename):
    """
    Return list of Site instances corresponding to the template file.
    """
    for line in file(filename):
        line = line.expandtabs().strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('!'):
            global MASTER
            MASTER = parse_line(line)[1]
            continue
        yield parse_line(line)


def usage():
    print __doc__
    sys.exit(0)

def test():
    print 'Performing self tests.'
    import doctest
    doctest.testmod()
    sys.exit(0)

def cmdloop(rcfile):
    print "Enter number, 'q' to quit, or 'a' to display all passwords."
    while True:
        try:
            cmd = raw_input('>>> ').strip()
        except EOFError:
            print
            sys.exit(0)
        if cmd.isdigit():
            sites = list(parse(rcfile))
            try:
                name, tmpl = sites[int(cmd) - 1]
            except IndexError:
                print 'not in list: %s' % cmd
                continue
            print name, '--> ',
            output_password(tmpl, name)
        elif cmd == 'a':
            for name, tmpl in parse(rcfile):
                print name, '--> ',
                output_password(tmpl, name)
        elif cmd == 'q':
            sys.exit(0)
        elif cmd == '':
            pass
        else:
            print 'Unknown command %r.' % cmd


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:ht', ['file', 'help'])
    except getopt.GetoptError:
        usage()
    if len(args) > 1:
        usage()

    rcfile = expanduser('~/.passwdmgr')
    for o, v in opts:
        if o in ('-f', '--file'): rcfile = v
        if o in ('-h', '--help'): usage()
        if o == '-t':
            global SLOW
            SLOW = 0
            test()

    # if an argument is given, use it as a template and print the
    # created password before exiting:
    if len(args) == 1:
        output_password(args[0], os.urandom(128))
        return

    # Set master password:
    """
    global MASTER
    try:
        MASTER = getpass('Master password: ')
    except EOFError:
        print
        return
    """

    # Print the entries of the template file:
    for i, (name, tmpl) in enumerate(parse(rcfile)):
        print '%4d %-30s %s' % (i + 1, name, tmpl)

    cmdloop(rcfile)


if __name__ == '__main__':
    main()
