import urllib2

url = 'http://repo.continuum.io/pkgs/gpl/osx-64/repodata.json'

request = urllib2.Request(url)
request.add_header('If-None-Match', '2f1bf63044f924c048e0dce972929c4b')
try:
    u = urllib2.urlopen(request)
except urllib2.HTTPError as e:
    print e.code, e.msg
except urllib2.URLError:
    print "host unknown"

content = u.read()
u.close()

print content