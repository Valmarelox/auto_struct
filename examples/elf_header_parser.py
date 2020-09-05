from itertools import count
from mmap import mmap, ACCESS_READ
from auto_struct import *
from dataclasses import dataclass


class ElfMagic(Array(uint8_t, 4)):
    def __init__(self, *values):
        super(ElfMagic, self).__init__(*values)
        assert self == b'\x7fELF', 'Wrong elf magic {0}'.format(values)

    def __repr__(self):
        return repr(''.join(map(chr, self)))


class EIClass(BaseEnum):
    __ELEMENT_TYPE__ = uint8_t
    ELFCLASSNONE = 0
    ELFCLASS32 = 1
    ELFCLASS64 = 2


@dataclass
class ElfIdent(BasicStruct):
    ei_magic: ElfMagic
    ei_class: EIClass
    ei_data: uint8_t
    ei_version: uint8_t
    ei_osabi: uint8_t
    ei_abiversion: uint8_t
    ei_padding: Padding(7)


@dataclass
class Elf64Header(BasicStruct):
    e_ident: ElfIdent
    e_type: uint16_t
    e_machine: uint16_t
    e_version: uint32_t
    e_entry: uint64_t
    e_phoff: uint64_t
    e_shoff: uint64_t
    e_flags: uint32_t
    e_ehsize: uint16_t
    e_phentsize: uint16_t
    e_phnum: uint16_t
    e_shentsize: uint16_t
    e_shnum: uint16_t
    e_shstrndx: uint16_t


class ShdrType(BaseEnum):
    __ELEMENT_TYPE__ = uint32_t
    SHT_NULL = 0
    SHT_PROGBITS = 1
    SHT_SYMTAB = 2
    SHT_STRTAB = 3
    SHT_RELA = 4
    SHT_HASH = 5
    SHT_DYNAMIC = 6
    SHT_NOTE = 7
    SHT_NOBITS = 8
    SHT_REL = 9
    SHT_SHLIB = 10
    SHT_DYNSYM = 11
    SHT_INIT_ARRAY = 14
    SHT_FINNI_ARRAY = 15
    SHT_PREINIT_ARRAY = 16
    SHT_GROUP = 17
    SHT_SYMTAB_SHNDX = 18

    SHT_GNU_INCREMENTAL_INPUTS = 0x6fff4700
    SHT_GNU_ATTRIBUTES = 0x6ffffff5
    SHT_GNU_HASH = 0x6ffffff6
    SHT_GNU_LIBLIST = 0x6ffffff7
    SHT_GNU_verdef = 0x6ffffffd
    SHT_GNU_verneed = 0x6ffffffe
    SHT_GNU_versym = 0x6fffffff


class Shdr64Flags(BitFlag):
    __ELEMENT_TYPE__ = uint64_t
    SHF_WRITE = (1 << 0)
    SHF_ALLOC = (1 << 1)
    SHF_EXECINSTR = (1 << 2)
    SHF_MERGE = (1 << 4)
    SHF_STRINGS = (1 << 5)
    SHF_INFO_LINK = (1 << 6)
    SHF_LINK_ORDER = (1 << 7)
    SHF_OS_NONCONFORMING = (1 << 8)
    SHF_GROUP = (1 << 9)
    SHF_TLS = (1 << 10)
    SHF_COMPRESSED = (1 << 11)
    SHF_GNU_BUILD_NOTE = (1 << 20)
    SHF_GNU_MBIND = (1 << 24)
    SHF_EXCLUDE = (1 << 31)


@dataclass
class Elf64SectionHeader(BasicStruct):
    sh_name: uint32_t
    sh_type: ShdrType
    sh_flags: Shdr64Flags
    sh_addr: uint64_t
    sh_offset: uint64_t
    sh_size: uint64_t
    sh_link: uint32_t
    sh_info: uint32_t
    sh_addralign: uint64_t
    sh_entsize: uint64_t


class Section:
    def __init__(self, e, shdr: Elf64SectionHeader):
        self.e = e
        self.shdr = shdr

    @property
    def name(self):
        return self.e.shstrtab.read_str(self.shdr.sh_name)

    @property
    def start(self):
        return self.shdr.sh_offset

    @property
    def end(self):
        return self.shdr.sh_offset + self.shdr.sh_size

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.e[self.start + item.start(): self.end + item.stop()]
        else:
            return self.e[self.start + item]


class StringTableSection(Section):
    def read_str(self, offset):
        s = b''
        for i in count(0):
            c = bytes([self[offset + i]])
            if c == b'\x00':
                return s
            s += c


class PhdrType(BaseEnum):
    __ELEMENT_TYPE__ = uint32_t
    PT_NULL = 0
    PT_LOAD = 1
    PT_DYNAMIC = 2
    PT_INTERP = 3
    PT_NOTE = 4
    PT_SHLIB = 5
    PT_PHDR = 6
    PT_LOPROC = 0x70000000
    PT_HIPROC = 0x7fffffff
    PT_LOOS = 0x60000000
    PT_GNU_EH_FRAME = PT_LOOS + 0x474e550
    PT_GNU_STACK = PT_LOOS + 0x474e551
    PT_GNU_RELRO = PT_LOOS + 0x474e552
    PT_GNU_PROPERTY = PT_LOOS + 0x474e553


class PhdrFlag(BitFlag):
    __ELEMENT_TYPE__ = uint32_t
    PF_X = (1 << 0)
    PF_W = (1 << 1)
    PF_R = (1 << 2)


@dataclass
class Elf64Phdr(BasicStruct):
    p_type: PhdrType
    p_flags: PhdrFlag
    p_offset: uint64_t
    p_vaddr: uint64_t
    p_paddr: uint64_t
    p_filesz: uint64_t
    p_memsz: uint64_t
    p_align: uint64_t


class ElfFile(mmap):
    def __new__(cls, filename):
        fd = open(filename, 'rb')
        return super().__new__(cls, fd.fileno(), 0, access=ACCESS_READ)

    @property
    def header(self):
        return Elf64Header.parse(self[:len(Elf64Header)])

    @property
    def sections(self):
        yield from (self._section(i) for i in range(self.header.e_shnum))

    @property
    def phdrs(self):
        yield from (self._phdr(i) for i in range(self.header.e_phnum))

    def _read_object(self, offset, t):
        return t.parse(self[offset: offset + len(t)])

    def _section(self, idx, cls=Section):
        start = self.header.e_shoff + idx * len(Elf64SectionHeader)
        return cls(self, self._read_object(start, Elf64SectionHeader))

    def _phdr(self, idx):
        start = self.header.e_phoff + idx * len(Elf64Phdr)
        return self._read_object(start, Elf64Phdr)

    @property
    def shstrtab(self):
        return self._section(self.header.e_shstrndx, StringTableSection)


with ElfFile('/bin/ls') as f:
    print(f.header)
    for section in f.sections:
        print(section.name, section.shdr)

    for i, phdr in enumerate(f.phdrs):
        print(i, phdr)
