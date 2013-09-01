import bz2
import json
from logging import getLogger
from os.path import join

from conda.connection import connectionhandled_urlopen

log = getLogger(__name__)

retries = 3


def fetch_repodata(url):
    for x in range(retries):
        for fn in 'repodata.json.bz2', 'repodata.json':
            try:
                fi = connectionhandled_urlopen(url + fn)
                if fi is None:
                    raise RuntimeError("failed to fetch repo data from %s" %
                                       url)

                log.debug("fetched: %s [%s] ..." % (fn, url))
                data = fi.read()
                fi.close()
                if fn.endswith('.bz2'):
                    data = bz2.decompress(data).decode('utf-8')
                return json.loads(data)

            except IOError:
                log.debug('download failed try: %d' % x)

    raise RuntimeError("failed to fetch repodata from %r" % url)


if __name__ == '__main__':
    URL = 'http://repo.continuum.io/pkgs/free/osx-64/'
    d = fetch_repodata(URL)
    print len(d['packages'])
