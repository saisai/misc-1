


def add_depends(info):
    info['depends'] = list(info['requires'])



def add_all_depends(index):
    for info in index.itervalues():
        add_depends(info)
