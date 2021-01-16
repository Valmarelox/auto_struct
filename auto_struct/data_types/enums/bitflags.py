from .base_enum import BaseEnum, BaseEnumMeta
from ..int.unsigned_integer import UnsignedInteger, uint32_t
from ...exceptions import BitNotDefined


class BitFlagMeta(BaseEnumMeta):
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        if not issubclass(cls.__ELEMENT_TYPE__, UnsignedInteger):
            raise TypeError(
                f'BitFlag can only use UnsignedInteger types as __ELEMENT_TYPE__ (got: {cls.__ELEMENT_TYPE__})')
        cls.__BITS__ = {cls.__ELEMENT_TYPE__(item[1]): item[0] for item in cls.__VALUES__.items()}
        return cls


class BitFlag(BaseEnum, metaclass=BitFlagMeta):
    """
        Bitflag field with default size == sizeof(uint32_t)

        Example:
        class RWX(BitFlag):
            __ELEMENT_TYPE__ = uint8_t
            X = (1 << 0)
            W = (1 << 1)
            R = (1 << 2)

        print(RWX(3)) # Result: (X|W)
    """

    __ELEMENT_TYPE__ = uint32_t

    def __or__(self, other):
        return BitFlag(self.__ELEMENT_TYPE__(self) | self.__ELEMENT_TYPE__(other))

    def __and__(self, other):
        return BitFlag(self.__ELEMENT_TYPE__(self) & self.__ELEMENT_TYPE__(other))

    def __invert__(self):
        return BitFlag(~self.__ELEMENT_TYPE__(self))

    def __iter__(self):
        for idx in range(0, self.__ELEMENT_TYPE__.BITS):
            if bit := self.value & (1 << idx):
                yield self.__ELEMENT_TYPE__(bit)

    def __repr__(self):
        return f'({"|".join(self.__BITS__[bit] for bit in self)})'

    def verify(self):
        if not all(x in self.__VALUES__.values() for x in self):
            raise BitNotDefined(f'{hex(int(self))} contains bits not defined in {type(self).__name__}')
