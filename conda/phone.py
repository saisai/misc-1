import socket


HOST, PORT = 'binstar.org', 80


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    req = '''\
POST /phone-home HTTP/1.1
Host: %s

name=__NAME__&version=__VERSION__&platform=__PLATFORM__
''' % HOST
    print req
    s.send(req.replace('\n', '\r\n'))

    print s.recv(1024).replace('\r', r'\r')


if __name__ == '__main__':
    main()
