import cStringIO
import hashlib
import struct


BLOCKSIZE = 1024
INODESIZE = 128


def md5(s):
    return hashlib.md5(s).hexdigest()


f = open('image.ext2')
image = f.read()
f.close()


def block_slice(n):
    return slice(BLOCKSIZE * n, BLOCKSIZE * (n + 1), 1)


class Inode(object):
    #      0123456789     12..26    27..30   31..36
    fmt = 'HHLLLLLHHLLL' + 15*'L' + 'LLLL' + 'ccHHHL'

    def __init__(self, inode):
        self.inode = inode
        p = (inode + 543) * INODESIZE
        self.data = image[p:p + INODESIZE]
        t = struct.unpack(self.fmt, self.data)
        self.mode = t[0]
        self.uid = t[1]
        self.size = t[2]
        self.gid = t[7]
        self.links_count = t[8]
        self.blocks = t[9]
        self.block = [t[j] for j in xrange(12, 27)]

    def __str__(self):
        return '%4s %7s %s' % (self.inode, self.size, self.blocks)

    def add_block(self, n):
        self._size += BLOCKSIZE
        self.f.write(image[block_slice(n)])
        return self._size >= self.size

    def get_pointer(self, data, i):
        assert len(data) == BLOCKSIZE
        t = struct.unpack('L', data[4 * i:4 * (i + 1)])
        return t[0]

    def read_file(self):
        self._size = 0
        self.f = cStringIO.StringIO()

        for n in self.block[:12]:
            if self.add_block(n):
                break

        if self.size > self._size:
            pointer_data = image[block_slice(self.block[12])]
            for i in xrange(BLOCKSIZE / 4):
                n = self.get_pointer(pointer_data, i)
                if self.add_block(n):
                    break

        if self.size > self._size:
            pointer_data0 = image[block_slice(self.block[13])]
            for i1 in xrange(BLOCKSIZE / 4):
                n1 = self.get_pointer(pointer_data0, i1)
                pointer_data1 = image[block_slice(n1)]
                for i2 in xrange(BLOCKSIZE / 4):
                    n2 = self.get_pointer(pointer_data1, i2)
                    if self.add_block(n2):
                        break

        res = self.f.getvalue()
        self.f.close()
        return res[:self.size]


class DirectoryEntry(object):
    def __init__(self, data, p):
        s = data[p:p + 8]
        if not s or s == 8*'\0':
            self.rec_len = -1
            return
        (self.inode, self.rec_len, self.name_len,
                self.file_type) = struct.unpack('LHbb', s)
        self.name = data[p + 8:p + 8 + self.name_len]

    def __str__(self):
        return '%4s %3s  %-17s' % (self.inode, self.file_type, self.name)


def read_directory(inode):
    i = Inode(inode)
    data = i.read_file()
    p = 0
    res = {}
    while True:
        de = DirectoryEntry(data, p)
        if de.rec_len < 0:
            break
        res[de.name] = de
        p += de.rec_len
    return res


def inode_path(path, inode=2):
    ls = read_directory(inode)
    fn = path.split('/')[0]
    if fn not in ls:
        return None
    de = ls[fn]
    if de.file_type == 2 and '/' in path:
        return inode_path(path[len(fn) + 1:], de.inode)
    return de.inode


def list_file(d, fn):
    de = d[fn]
    i = Inode(d[fn].inode)
    print de, '%8s %s' % (i.size, i.links_count),
    if de.file_type == 1:
        data = i.read_file()
        print md5(data) #, len(data)
    elif de.file_type == 7:
        if i.size <= 60: # fast symlink
            # 40 is the position (within the inode) where usually
            # the 15 block pointers start, and 4 * 15 = 60 which explains
            # the maximal size for fast symlinks
            print i.data[40:40 + i.size]
        else: # slow symlink
            print i.read_file()
    else:
        print


def ls(path):
    d = read_directory(inode_path(path))
    for fn in sorted(d):
        list_file(d, fn)


ls('.')
