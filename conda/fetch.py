import bz2
import json
import urllib2
from logging import getLogger

from conda.connection import connectionhandled_urlopen

log = getLogger(__name__)


def fetch_repodata(url, cache={}):
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
        print "host unknown in:", url

    return cache[url]


if __name__ == '__main__':
    cache_path = 'etags.json'
    try:
        cache = json.load(open(cache_path))
    except IOError:
        cache = {}
    URL = 'http://repo.continuum.io/pkgs/free/osx-64/'
    d = fetch_repodata(URL, cache)
    print len(d['packages'])

    try:
        with open(cache_path, 'w') as fo:
            json.dump(cache, fo, indent=2, sort_keys=True)
    except IOError:
        pass
