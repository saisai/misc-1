#client example
import socket

host, port = 'repo.continuum.io', 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
req = '''\
GET /pkgs/gpl/osx-64/repodata.json HTTP/1.1
Host: %s
Connection: keep-alive
If-Modified-Since: Thu, 04 Jul 2013 06:37:11 GMT
If-None-Match: "2f1bf63044f924c048e0dce972929c4b"

''' % host
s.send(req.replace('\n', '\r\n'))

print s.recv(1024).replace('\r', r'\r')
