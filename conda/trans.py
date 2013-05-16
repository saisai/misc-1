


def add_depends(info):
    depends = []
    for s in info['requires']:
        parts = s.split()
        while len(parts) < 3:
            parts.append(None)
        assert len(parts) == 3
        name, version, build = parts
        assert name is not None
        assert version is not None

        if build:
            depends.append(name + ' ' + version + ' ' + build)

        elif name in ('python', 'numpy') and len(version) == 3:
            depends.append('%s %s*' % (name, version))

        elif name in ('nose', 'pytz', 'dateutil', 'distribute', 'docutils'):
            depends.append(name)

        elif (info['name'] == ('gevent-websocket', 'gevent_zeromq') and
                   name == 'gevent'):
            depends.append('gevent 0.13.7|0.13.8')

        elif info['name'] == 'statsmodels' and name == 'pandas':
            depends.append('pandas')

        else:
            depends.append(name + ' ' + version)

    info['depends'] = depends


def add_all_depends(index):
    for info in index.itervalues():
        add_depends(info)
