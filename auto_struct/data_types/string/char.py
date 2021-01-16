from typing import Union

from ..int.integer import Integer
from ..int import uint8_t
from ...exceptions.type import ElementCountException


class Char(uint8_t):
    """
        8-bit ASCII character
    """
    FORMAT = 'c'

    def __init__(self, value: Union[bytes,Integer,int]):
        if isinstance(value, (Integer, int)):
            value = int(value)
        else:
            value = bytes(value)
            if len(value) != 1:
                raise ElementCountException(f'value has invalid length: {len(value)}, expected: 1')
            value = ord(value)
        super(Char, self).__init__(value)

    def __repr__(self):
        return repr(bytes(self.value))

    def __str__(self):
        return chr(self.value)

    def __bytes__(self):
        return bytes(chr(self.value), 'ascii')

    def __int__(self):
        return self.value

    def __index__(self):
        return int(self)
    
    def __eq__(self, other):
        if isinstance(other, bytes):
            other = ord(other)
        return super(Char, self).__eq__(other)

    def __hash__(self):
        return super(Char, self).__hash__()
