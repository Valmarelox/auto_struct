from ..basic_type import BaseType


class Integer(BaseType, int):
    BITS = 0
    SIGNED = True
    FORMAT = 'i'

    def __init__(self, value):
        super().__init__()
        lower_bound = -(1 << (self.BITS - 1)) if self.SIGNED else 0
        upper_bound = (1 << (self.BITS - 1)) if self.SIGNED else (1 << self.BITS)
        assert lower_bound <= value < upper_bound

    # Sign extended operations
    def __invert__(self):
        return super().__invert__() & ((1 << self.BITS) - 1)


class int8_t(Integer):
    BITS = 8
    FORMAT = 'b'


class int16_t(Integer):
    BITS = 16
    FORMAT = 'h'


class int32_t(Integer):
    BITS = 32
    FORMAT = 'i'


class int64_t(Integer):
    BITS = 64
    FORMAT = 'q'
