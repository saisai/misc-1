import re

class MatchSpec(object):

    def __init__(self, spec):
        self.spec = spec
        parts = spec.split()
        self.strictness = len(parts)
        assert 1 <= self.strictness <= 3
        self.name = parts[0]

        if self.strictness == 2:
            rx = parts[1]
            rx = rx.replace('.', r'\.')
            rx = rx.replace('*', r'.*')
            rx = r'(%s)$' % rx
            self.ver_pat = re.compile(rx)

        elif self.strictness == 3:
            self.ver_build = tuple(parts[1:3])

    def match(self, fn):
        assert fn.endswith('.tar.bz2')
        name, version, build = fn[:-8].rsplit('-', 2)
        if name != self.name:
            return False
        if self.strictness == 2 and self.ver_pat.match(version) is None:
            return False
        if self.strictness == 3 and ((version, build) != self.ver_build):
            return False
        return True

    def __eq__(self, other):
        return self.spec == other.spec

    def __hash__(self):
        return hash(self.spec)

    def __repr__(self):
        return 'MatchSpec(%r)' % (self.spec)


if __name__ == '__main__':
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
                       ('python', False),
                       ]:
        m = MatchSpec(mspec)
        assert m.match('numpy-1.7.1-py27_0.tar.bz2') == res, mspec

    a, b = MatchSpec('numpy 1.7*'), MatchSpec('numpy 1.7*')
    c, d = MatchSpec('python'), MatchSpec('python 2.7*')
    assert a == b and hash(a) == hash(b)
    assert a != c and hash(a) != hash(c)
