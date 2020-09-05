from .integer import Integer


class UnsignedInteger(Integer):
    BITS = 0
    SIGNED = False
    FORMAT = 'I'


class uint8_t(UnsignedInteger):
    FORMAT = 'B'
    BITS = 8


class uint16_t(UnsignedInteger):
    FORMAT = 'H'
    BITS = 16


class uint32_t(UnsignedInteger):
    FORMAT = 'I'
    BITS = 32


class uint64_t(UnsignedInteger):
    FORMAT = 'Q'
    BITS = 64
