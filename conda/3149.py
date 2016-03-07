import re



pat = re.compile(r'''
(?P<mod>\w+)            # actual module name
(\.cp[\w\-]+)           # py3k stuff
\.(?P<ext>so|pyd)       # extension
$
''', re.VERBOSE)


def shorten_name(fn):
    match = pat.match(fn)
    if match is None:
        return None
    else:
        return match.expand(r'\g<mod>.\g<ext>')


for fn, res in [
    ('xxlimited.cpython-35m-darwin.so', 'xxlimited.so'),
    ('_tkinter.cpython-35m.so',         '_tkinter.so'),
    ('_tkinter.cpython-35m.pyd',        '_tkinter.pyd'),
    ('_tkinter.cpython-35m.py',         None),
    ('_bitarray.cp35-win32.so',         '_bitarray.so'),
    ('bit.array.cp35-win32.so',         None),
    ('phone.so',                        None),
    ]:
    print '%s -> %s' % (fn, shorten_name(fn))
    assert shorten_name(fn) == res
