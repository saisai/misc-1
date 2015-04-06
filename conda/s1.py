#client example
import socket

host, port = 'repo.continuum.io', 80
req = '''\
GET /pkgs/gpl/osx-64/repodata.json HTTP/1.1
Host: %s
Connection: keep-alive
If-Modified-Since: Mon, 06 Apr 2015 16:40:14 GMT
If-None-Match: "5522b6ee-9b"
User-Agent: Test-User-Agent/1.0.0

''' % host

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(req.replace('\n', '\r\n'))
print s.recv(1024).replace('\r', r'\r')
