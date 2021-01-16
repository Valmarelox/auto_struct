from ..basic_type import BaseType
from ...exceptions.type import ElementCountException


class Char(BaseType):
    """
        8-bit ASCII character
    """
    FORMAT = 'c'

    def __init__(self, value: bytes):
        super().__init__()
        if len(value) != 1:
            raise ElementCountException(f'value has invalid length: {len(value)}, expected: 1')
        self.value = value

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

    def __bytes__(self):
        return bytes(self.value)

    def __eq__(self, other):
        return bytes(self) == bytes(other)
