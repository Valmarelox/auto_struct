from .base_enum import BaseEnum, BaseEnumMeta
from ..int.unsigned_integer import UnsignedInteger, uint32_t


class BitFlagMeta(BaseEnumMeta):
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        if not issubclass(cls.__ELEMENT_TYPE__, UnsignedInteger):
            raise TypeError('BitFlag can only use UnsignedInteger types as __ELEMENT_TYPE__ (got: {0})'.format(
                cls.__ELEMENT_TYPE__))
        cls.__BITS__ = {item[1]: item[0] for item in cls.__VALUES__.items()}
        return cls


class BitFlag(BaseEnum, metaclass=BitFlagMeta):
    __ELEMENT_TYPE__ = uint32_t

    def __init__(self, value):
        super().__init__(value)

    def verify(self):
        assert all(x in self.__VALUES__.values() for x in self)

    def __or__(self, other):
        return BitFlag(self.__ELEMENT_TYPE__(self) | self.__ELEMENT_TYPE__(other))

    def __and__(self, other):
        return BitFlag(self.__ELEMENT_TYPE__(self) & self.__ELEMENT_TYPE__(other))

    def __invert__(self):
        return BitFlag(~self.__ELEMENT_TYPE__(self))

    def __iter__(self):
        for idx in range(0, self.__ELEMENT_TYPE__.BITS):
            if bit := self.value & (1 << idx):
                yield bit

    def __repr__(self):
        return '({0})'.format('|'.join(self.__BITS__[bit] for bit in self))
