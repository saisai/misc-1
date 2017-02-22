from libconda.fetch import fetch_index

from ll.diffutils import show_dict_diff
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
            assert fn in index2
            info1 = index1[fn]
            info2 = index2[fn]
            for key in 'channel', 'md5', 'size':
                del info1[key], info2[key]
            show_dict_diff(info1, info2)
