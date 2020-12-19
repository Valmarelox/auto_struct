from .integer import Integer


class UnsignedInteger(Integer):
    """
        Basic unsigned integer type, shouldn't be used directly
    """
    BITS = 0
    SIGNED = False
    FORMAT = 'I'


class uint8_t(UnsignedInteger):
    """
        8-bit unsigned int
    """
    BITS = 8
    FORMAT = 'B'


class uint16_t(UnsignedInteger):
    """
        16-bit unsigned int
    """
    BITS = 16
    FORMAT = 'H'


class uint32_t(UnsignedInteger):
    """
        32-bit unsigned int
    """
    BITS = 32
    FORMAT = 'I'


class uint64_t(UnsignedInteger):
    """
        64-bit unsigned int
    """
    BITS = 64
    FORMAT = 'Q'
