from ..basic_type import BaseType
from ...exceptions.type import ElementCountException


class Char(bytes, BaseType):
    """
        8-bit ASCII character
    """
    FORMAT = 'c'

    def __init__(self, value: bytes):
        if len(value) != 1:
            raise ElementCountException(f'value has invalid length: {len(value)}, expected: 1')
        super().__init__(value)
