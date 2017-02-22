from libconda.fetch import fetch_index

from ll.diffutils import show_dict_diff, show_set_diff
from repo.config import SUBDIRS


for channel in 'free', 'pro':
    for subdir in list(SUBDIRS) + ['noarch']:
        urls1 = 'https://repo.continuum.io/pkgs/%s/%s/' % (channel, subdir),
        index1 = fetch_index(urls1)
        urls2 = 'http://bremen/pkgs/%s/%s/' % (channel, subdir),
        index2 = fetch_index(urls2)

        print channel, subdir, len(index1), len(index2)

        assert len(index1) == len(index2)
        for fn in index1:
            info1 = index1[fn]
            info2 = index2[fn]
            dep1 = set(info1['depends'])
            dep2 = set(info2['depends'])
            for key in 'channel', 'md5', 'size', 'depends':
                del info1[key], info2[key]
            show_dict_diff(info1, info2)
            show_set_diff(dep1, dep2)
