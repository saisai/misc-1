from struct import pack, unpack, calcsize


class Elf_Shdr(object):

    vars = [
        ('Word', 'sh_name',      'Section name (string tbl index)'),
        ('Word', 'sh_type',      'Section type'),
        ('Word', 'sh_flags',     'Section flags'),
        ('Addr', 'sh_addr',      'Section virtual addr at execution'),
        ('Off',  'sh_offset',    'Section file offset'),
        ('Word', 'sh_size',      'Section size in bytes'),
        ('Word', 'sh_link',      'Link to another section'),
        ('Word', 'sh_info',      'Additional section information'),
        ('Word', 'sh_addralign', 'Section alignment'),
        ('Word', 'sh_entsize',   'Entry size if section holds table'),
    ]

    def read(self, fi):
        self.fmt = ''.join(self.typmap[typ] for typ, name, des in self.vars)

        tmp = unpack(self.fmt, fi.read(calcsize(self.fmt)))
        for i, (typ, name, des) in enumerate(self.vars):
            setattr(self, name, tmp[i])

    def write(self, fo):
        args = [self.fmt]
        args.extend(getattr(self, name) for typ, name, des in self.vars)
        fo.write(pack(*args))

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
    print eh.e_shoff
    fi.seek(eh.e_shoff)
    print fi.tell()
    print repr(fi.read(40))
    sh.read(fi)
    sh.display()
    fi.close()
