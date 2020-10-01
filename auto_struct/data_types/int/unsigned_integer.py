from .integer import Integer


class UnsignedInteger(Integer):
    BITS = 0
    SIGNED = False
    FORMAT = 'I'


class uint8_t(UnsignedInteger):
    BITS = 8
    FORMAT = 'B'


class uint16_t(UnsignedInteger):
    BITS = 16
    FORMAT = 'H'


class uint32_t(UnsignedInteger):
    BITS = 32
    FORMAT = 'I'


class uint64_t(UnsignedInteger):
    BITS = 64
    FORMAT = 'Q'
