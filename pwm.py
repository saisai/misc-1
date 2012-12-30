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

import sys
import hashlib
import string
import getopt
from getpass import getpass
from random import random
from os.path import expanduser


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
    if typ in 'aAxXzZ':
        pool += string.ascii_lowercase
    if typ in 'AXZ':
        pool += string.ascii_uppercase
    if typ in '9xXzZ':
        pool += string.digits
    if typ in 'pzZ':
        pool += '!@#$%^&-+=;:,.'
    if pool=='':
        pool = typ
    return pool[int(hashlib.md5(hashin).hexdigest(), 16) % len(pool)]


MASTER = ''
def passwd(tmpl, hashin):
    """
    Returns a password which is calculated from the md5sum
    of the string `hashin`.
    The string `tmpl` is a template which describes the form of the password.

    Example:
    >>> passwd('999 aaa AAAAAA xxxxxx XXXXXX pppp zzzzzz ZZZZZZZZZZ', 'g')
    '131 wuo mympmK 3swcih Fb5lYA ..%, 5-1;kf jkKkJ;06f0'
    """
    return ''.join(char(t, hashin+str(i) + MASTER)
                   for i, t in enumerate(tmpl))


def rmcomm(line):
    """
    >>> rmcomm('foo bar ## Comment')
    'foo bar'
    >>> rmcomm('example')
    'example'
    """
    return (line.split('#', 1)[0] if line.count('#') else line).strip()


class Site:
    """
    >>> a = Site('example.com (1)  XXX  # Comment')
    >>> a.name
    'example.com (1)'
    >>> a.tmpl
    'XXX'
    >>> print a
    example.com (1) --> T6B
    """
    def __init__(self, line):
        self.line = line
        self.name, self.tmpl = [
            x.strip() for x in rmcomm(line).rsplit(None, 1)]

    def __str__(self):
        return '%s --> %s' % (self.name,  passwd(self.tmpl, self.name))


def sites(filename):
    """
    Return list of Site instances corresponding to the template file.
    """
    res = []
    for line in file(filename):
        line = line.expandtabs().strip()
        if not rmcomm(line):
            continue
        if line[0]=='!':
            tmpl, chck = line[1:].split()
            passwd = str(Site('a ' + tmpl)).split()[-1]
            if passwd != chck:
                print 'You entered a wrong master password.', passwd
                sys.exit(1)
            continue
        res.append(Site(line))
    return res


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
            try:
                print sites(rcfile)[int(cmd)-1]
            except IndexError:
                print '%s not found in list.' % cmd
        elif cmd=='a':
            for s in sites(rcfile): print s
        elif cmd=='q':
            sys.exit(0)
        elif cmd=='':
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
        if o == '-t': test()

    # if an argument is given, use it as a template and print the
    # created password before exiting:
    if len(args)==1:
        print passwd(args[0], '%.15f' % random())
        return

    # Set master password:
    global MASTER
    try:
        MASTER = getpass('Master password: ')
    except EOFError:
        print
        return

    # Print the entries of the template file:
    for i, site in enumerate(sites(rcfile)):
        print '%4d %s' % (i+1, site.line)

    cmdloop(rcfile)


if __name__ == '__main__':
    main()
