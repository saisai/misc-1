from struct import pack, unpack, calcsize


# see /usr/include/elf.h for more details

class Elf_Ehdr(object):

    EI_NIDENT = 16

    vars = [
        ('Half', 'e_type',       'Object file type'),
        ('Half', 'e_machine',    'Architecture'),
        ('Word', 'e_version',    'Object file version'),
        ('Addr', 'e_entry',      'Entry point virtual address'),
        ('Off',  'e_phoff',      'Program header table file offset'),
        ('Off',  'e_shoff',      'Section header table file offset'),
        ('Word', 'e_flags',      'Processor-specific flags'),
        ('Half', 'e_ehsize',     'ELF header size in bytes'),
        ('Half', 'e_phentsize',  'Program header table entry size'),
        ('Half', 'e_phnum',      'Program header table entry count'),
        ('Half', 'e_shentsize',  'Section header table entry size'),
        ('Half', 'e_shnum',      'Section header table entry count'),
        ('Half', 'e_shstrndx',   'Section header string table index'),
    ]

    def read(self, fi):
        self.e_ident = fi.read(self.EI_NIDENT)
        if self.e_ident[0:4] != '\x7fELF':
            print 'WARNING: Not an ELF header'
            return False

        self.ELFCLASS = ord(self.e_ident[4])
        if self.ELFCLASS == 1: # 32bit
            pt = 'I'
        elif self.ELFCLASS == 2: # 64bit
            pt = 'Q'
        else:
            raise NotImplementedError

        self.typmap = {'Half': 'H', 'Word': 'I', 'Addr': pt, 'Off': pt}
        self.fmt = ''.join(self.typmap[typ] for typ, name, des in self.vars)

        tmp = unpack(self.fmt, fi.read(calcsize(self.fmt)))
        for i, (typ, name, des) in enumerate(self.vars):
            setattr(self, name, tmp[i])

        assert self.EI_NIDENT + calcsize(self.fmt) == self.e_ehsize

    def write(self, fo):
        fo.write(self.e_ident)
        args = [self.fmt]
        args.extend(getattr(self, name) for typ, name, des in self.vars)
        fo.write(pack(*args))

    def display(self):
        print 'ELF Header:'
        print '    Magic: %r' % self.e_ident
        for i, (typ, name, des) in enumerate(self.vars):
            val = getattr(self, name)
            if typ == 'Addr':
                val = hex(val)
            print '    %-35s%-12s (%s %i) %s' % (
                    des + ':', val, typ, calcsize(self.fmt[i]), name)


if __name__ == '__main__':
    import sys

    eh = Elf_Ehdr()

    fi = open(sys.argv[1], 'rb')
    eh.read(fi)
    fi.close()

    eh.display()

    fo = open('out', 'wb')
    eh.write(fo)
    fo.close()
