#client example
import socket

host, port = 'repo.continuum.io', 80
req = '''\
GET /pkgs/gpl/osx-64/repodata.json HTTP/1.1
Host: %s
Connection: keep-alive
If-Modified-Since: Sat, 04 Apr 2015 00:40:14 GMT
If-None-Match: "551f32ee-9b"
User-Agent: Test User Agent

''' % host

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(req.replace('\n', '\r\n'))
print s.recv(1024).replace('\r', r'\r')
