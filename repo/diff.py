from libconda.fetch import fetch_index

from repo.config import SUBDIRS


for channel in 'free', 'pro':
    for subdir in list(SUBDIRS) + ['noarch']:
        url1 = 'https://repo.continuum.io/pkgs/%s/%s/' % (channel, subdir)
        print url1
        index1 = fetch_index(tuple(url1,))
        url2 = 'http://bremen/pkgs/%s/%s/' % (channel, subdir)
        print url2
        index2 = fetch_index(tuple(url2,))

        print channel, subdir, len(index1), len(index2)
