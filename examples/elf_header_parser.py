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


with open('/bin/ls', 'rb') as f:
    e = (Elf64Header.parse(f.read(Elf64Header.struct.size)))
    print(e)
    print(e.e_ident)
    print(e.to_json())
