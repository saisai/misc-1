#client example
import socket

host, port = 'repo.continuum.io', 80
req = '''\
GET /pkgs/rss.xml HTTP/1.1
Host: %s
Connection: keep-alive
User-Agent: Test-User-Agent/1.0.0

''' % host
#If-Modified-Since: Mon, 06 Apr 2015 18:33:45 GMT\r
#If-None-Match: "5522d189-9b"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(req.replace('\n', '\r\n'))
print s.recv(1024).replace('\r', r'\r')
