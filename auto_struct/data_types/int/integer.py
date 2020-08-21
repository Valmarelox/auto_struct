from ..basic_type import BaseType


class Integer(BaseType, int):
    BITS = 0
    SIGNED = True
    FORMAT = 'i'

    def __init__(self, value):
        LOWER_BOUND = -(1 << (self.BITS - 1)) if self.SIGNED else 0
        UPPER_BOUND = (1 << (self.BITS - 1)) if self.SIGNED else (1 << self.BITS)
        assert LOWER_BOUND <= value < UPPER_BOUND
        self = value


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