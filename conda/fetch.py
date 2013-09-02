import bz2
import json
import shelve
import urllib2
from logging import getLogger
from os.path import join

from conda.connection import connectionhandled_urlopen

log = getLogger(__name__)


def fetch_repodata(url):
    request = urllib2.Request(url + 'repodata.json.bz2')
    if url in cache:
        d = cache[url]
        if '_etag' in d:
            request.add_header('If-None-Match', d['_etag'])
        if '_mod' in d:
            request.add_header('If-Modified-Since', d['_mod'])

    try:
        u = connectionhandled_urlopen(request)
        data = u.read()
        u.close()
        d = json.loads(bz2.decompress(data).decode('utf-8'))
        etag = u.info().getheader('Etag')
        if etag:
            d['_etag'] = etag
        timestamp = u.info().getheader('Last-Modified')
        if timestamp:
            d['_mod'] = timestamp
        cache[url] = d

    except urllib2.HTTPError as e:
        print e.code, e.msg
        if e.code != 304:
            raise

    except urllib2.URLError:
        print "host unknown"

    return cache[url]


if __name__ == '__main__':
    cache = shelve.open('etags')

    URL = 'http://repo.continuum.io/pkgs/free/osx-64/'
    d = fetch_repodata(URL)
    print len(d['packages'])
