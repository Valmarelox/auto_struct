from ..basic_type import BaseType


class Char(bytes, BaseType):
    FORMAT = 'c'

    def __init__(self, value: bytes):
        assert len(value) == 1
        super().__init__(value)
