from ..basic_type import BaseType
from ...exceptions.integer import IntegerOutOfBounds


class Integer(BaseType, int):
    """
        Basic Integer type, should not be used directly
    """
    BITS = 0
    SIGNED = True
    FORMAT = 'i'

    def __init__(self, value):
        super().__init__()
        lower_bound = -(1 << (self.BITS - 1)) if self.SIGNED else 0
        upper_bound = (1 << (self.BITS - 1)) if self.SIGNED else (1 << self.BITS)
        if not (lower_bound <= value < upper_bound):
            raise IntegerOutOfBounds(f'Integer {value} is out of the range {lower_bound}-{upper_bound}')

    # Sign extended operations
    def __invert__(self):
        """
            Invert the bits of the integer (dependson the bitsize)
        """
        return super().__invert__() & ((1 << self.BITS) - 1)


class int8_t(Integer):
    """
        8-bit signed int
    """
    BITS = 8
    FORMAT = 'b'


class int16_t(Integer):
    """
        16-bit signed int
    """
    BITS = 16
    FORMAT = 'h'


class int32_t(Integer):
    """
        32-bit signed int
    """
    BITS = 32
    FORMAT = 'i'


class int64_t(Integer):
    """
        64-bit signed int
    """
    BITS = 64
    FORMAT = 'q'
