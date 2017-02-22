from libconda.fetch import fetch_index

from repo.config import SUBDIRS


for channel in 'free', 'pro':
    for subdir in list(SUBDIRS) + ['noarch']:
        urls1 = 'https://repo.continuum.io/pkgs/%s/%s/' % (channel, subdir),
        print urls1
        index1 = fetch_index(urls1)
        urls2 = 'http://bremen/pkgs/%s/%s/' % (channel, subdir),
        print urls2
        index2 = fetch_index(urls2)

        print channel, subdir, len(index1), len(index2)
