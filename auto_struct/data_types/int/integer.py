from ..base.base_single_value_type import BaseSingleValueType
from ...exceptions.integer import IntegerOutOfBounds


class Integer(BaseSingleValueType):
    """
        Basic Integer type, should not be used directly
    """
    BITS = 0
    SIGNED = True
    FORMAT = 'i'

    def __init__(self, value):
        value = int(value)
        lower_bound = -(1 << (self.BITS - 1)) if self.SIGNED else 0
        upper_bound = (1 << (self.BITS - 1)) if self.SIGNED else (1 << self.BITS)
        if not (lower_bound <= value < upper_bound):
            raise IntegerOutOfBounds(f'Integer {value} is out of the range {lower_bound}-{upper_bound}')
        super().__init__(value)

    # Sign extended operations
    def __invert__(self):
        """
            Invert the bits of the integer (dependson the bitsize)
        """
        return super().__invert__() & ((1 << self.BITS) - 1)

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return int(self) == int(other)

    def __int__(self):
        return self.value

    def __index__(self):
        return self.value

    def __add__(self, other):
        return type(self)(int(self) + int(other))

    def __mul__(self, other):
        return type(self)(int(self) * int(other))

    def __and__(self, other):
        return type(self)(int(self).__and__(int(other)))

    def __or__(self, other):
        return type(self)(int(self).__or__(int(other)))

    def __repr__(self):
        return repr(int(self))

    def __bool__(self):
        return bool(int(self))

    def __lt__(self, other):
        return int(self) < int(other)


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
