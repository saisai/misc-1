import socket

host, port = 'binstar.org', 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
req = '''\
POST /phone-home HTTP/1.1
Host: %s

installer_name=Anaconda&installer_version=2.0.0&platform=linux-64
''' % host
s.send(req.replace('\n', '\r\n'))

print s.recv(1024).replace('\r', r'\r')
