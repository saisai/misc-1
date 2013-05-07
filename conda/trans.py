


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

        #if name in ('nose', 'pytz', 'distribute'):
        #    depends.append(name)
        #    continue

        if name in ('python', 'numpy') and len(version) == 3:
            assert build is None
            depends.append(name + ' ' + version + '*')

        elif build is None:
            depends.append(name + ' ' + version)

        else:
            depends.append(name + ' ' + version + ' ' + build)

    info['depends'] = depends


def add_all_depends(index):
    for info in index.itervalues():
        add_depends(info)
