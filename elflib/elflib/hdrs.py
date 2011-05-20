from struct import pack, unpack, calcsize


# see /usr/include/elf.h for more details

class Base_hdr(object):

    def _read(self, fi):
        self.fmt = ''.join(self.typmap[typ] for typ, name, des in self.vars)

        tmp = unpack(self.fmt, fi.read(calcsize(self.fmt)))
        for i, (typ, name, des) in enumerate(self.vars):
            setattr(self, name, tmp[i])

    def _write(self, fo):
        args = [self.fmt]
        args.extend(getattr(self, name) for typ, name, des in self.vars)
        fo.write(pack(*args))

    def _display(self):
        for i, (typ, name, des) in enumerate(self.vars):
            val = getattr(self, name)
            if typ == 'Addr':
                val = hex(val)
            print '    %-35s%-12s (%s %i) %s' % (
                    des + ':', val, typ, calcsize(self.fmt[i]), name)


class Elf_Ehdr(Base_hdr):

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
        self._read(fi)
        assert self.EI_NIDENT + calcsize(self.fmt) == self.e_ehsize

    def write(self, fo):
        fo.write(self.e_ident)
        self._write(fo)

    def display(self):
        print 'ELF Header:'
        print '    Magic: %r' % self.e_ident
        self._display()


class Elf_Shdr(Base_hdr):

    vars = [
        ('Word', 'sh_name',      'Section name (string tbl index)'),
        ('Word', 'sh_type',      'Section type'),
        ('Word', 'sh_flags',     'Section flags'),
        ('Addr', 'sh_addr',      'Section virtual addr at execution'),
        ('Off',	 'sh_offset',    'Section file offset'),
        ('Word', 'sh_size',      'Section size in bytes'),
        ('Word', 'sh_link',      'Link to another section'),
        ('Word', 'sh_info',      'Additional section information'),
        ('Word', 'sh_addralign', 'Section alignment'),
        ('Word', 'sh_entsize',   'Entry size if section holds table'),
    ]

    def read(self, fi):
        self._read(fi)

    def display(self):
        print 'Section Header:'
        for i, (typ, name, des) in enumerate(self.vars):
            val = getattr(self, name)
            if typ == 'Addr':
                val = hex(val)
            print '    %-35s%-12s (%s %i) %s' % (
                    des + ':', val, typ, calcsize(self.fmt[i]), name)


if __name__ == '__main__':
    import sys
    from ehdr import Elf_Ehdr

    fi = open(sys.argv[1], 'rb')
    eh = Elf_Ehdr()
    eh.read(fi)
    eh.display()

    sh = Elf_Shdr()
    sh.typmap = eh.typmap
    fi.seek(eh.e_shoff)
    sh.read(fi)
    sh.display()
    fi.close()
