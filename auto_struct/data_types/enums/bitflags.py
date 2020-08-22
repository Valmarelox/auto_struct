from .base_enum import BaseEnum, BaseEnumMeta
from ..int.unsigned_integer import UnsignedInteger, uint32_t


class BitFlagMeta(BaseEnumMeta):
    def __new__(metacls, *args, **kwargs):
        cls = super().__new__(metacls, *args, **kwargs)
        if not issubclass(cls.__ELEMENT_TYPE__, (UnsignedInteger)):
            raise TypeError('BitFlag can only use UnsignedInteger types as __ELEMENT_TYPE__ (got: {0})'.format(
                cls.__ELEMENT_TYPE__))
        return cls


class BitFlag(BaseEnum, metaclass=BitFlagMeta):
    __ELEMENT_TYPE__ = uint32_t

    def __verify(self):
        assert all(x in self.__VALUES__.values() for x in self)

    def __or__(self, other):
        return BitFlag(self.__ELEMENT_TYPE__(self) | self.__ELEMENT_TYPE__(other))

    def __and__(self, other):
        return BitFlag(self.__ELEMENT_TYPE__(self) & self.__ELEMENT_TYPE__(other))

    def __invert__(self):
        return BitFlag(~self.__ELEMENT_TYPE__(self))

    def __iter__(self):
        for idx in range(0, self.__ELEMENT_TYPE__.BITS):
            if bit := self._value & (1 << idx):
                yield bit

    def __repr__(self):
        return '({0})'.format('|'.format(bit for bit in self))