import re

class MatchSpec(object):

    def __init__(self, spec):
        parts = spec.split()
        self.strictness = len(parts)
        assert 1 <= self.strictness <= 3
        self.name = parts[0]
        if self.strictness >= 2:
            rx = parts[1]
            rx = rx.replace('.', r'\.')
            rx = rx.replace('*', r'.*')
            rx = r'(%s)$' % rx
            self.vpat = re.compile(rx)
        else:
            self.vpat = None

        if self.strictness == 3:
            self.build = parts[2]
        else:
            self.build = None

    def match(self, dist):
        name, version, build = dist.rsplit('-', 2)
        if name != self.name:
            return False
        if self.vpat and not self.vpat.match(version):
            return False
        if self.build and build != self.build:
            return False
        return True

if __name__ == '__main__':
    for mspec, res in [('numpy 1.7*', True),
                       ('numpy 1.7.1', True),
                       ('numpy 1.7', False),
                       ('numpy 1.6*|1.7*', True),
                       ('numpy 1.6*|1.8*', False),
                       ('numpy 1.6.2|1.7*', True),
                       ('numpy 1.6.2|1.7.1', True),
                       ('numpy 1.6.2|1.7.0', False),
                       ('numpy 1.7.1 py27_0', True),
                       ('numpy 1.7.* py27_0', True),
                       ('numpy 1.7.1 py26_0', False),
                       ('python', False),
                       ]:
        m = MatchSpec(mspec)
        assert m.match('numpy-1.7.1-py27_0') == res, mspec
