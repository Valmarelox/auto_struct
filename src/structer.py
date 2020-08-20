import struct
from dataclasses import *
from enum import Enum
from typing import TypeVar, NewType, Generic, List, Any, get_type_hints

uint8_t = NewType('uint8_t', int)
uint16_t = NewType('uint16_t', int)
uint32_t = NewType('uint32_t', int)

T = TypeVar('T')


class ArrayTypeBase(List):
    length = None
    type = None


def ArrayType(element_type: T, size: int):
    class _ArrayType(ArrayTypeBase):
        type = element_type
        length = size

    return _ArrayType


class AbstractTypeConvertor(Generic[T]):
    def validator(self, value: T) -> bool:
        raise NotImplementedError()

    @property
    def format(self) -> str:
        raise NotImplementedError()

    @property
    def args_creator(self, value: T) -> List[Any]:
        raise NotImplementedError()


class UIntegerTypeConvertor(AbstractTypeConvertor[T]):
    def __init__(self, bitsize):
        assert bitsize in (8, 16, 32, 64)
        self.bitsize = bitsize
        self.maxvalue = 1 << bitsize

    def validator(self, value: int) -> bool:
        return isinstance(value, int) and 0 <= value <= self.maxvalue

    @property
    def format(self) -> str:
        print(self.bitsize)
        return {1: 'B', 2: 'H', 4: 'I', 8: 'Q'}[int(self.bitsize / 8)]

    def args_creator(self, value: int) -> List[Any]:
        return [value]


class ArrayConvertor(AbstractTypeConvertor):
    def __init__(self, value: T, arr_type: ArrayTypeBase):
        self.size = arr_type.length
        self.type = arr_type.type
        self._value = value

    def validator(self, value: List[Any]) -> bool:
        assert self._value == value
        assert len(value) == self.size
        assert all([get_convertor(v, self.type).validator(v) for v in value])
        return True

    @property
    def format(self) -> str:
        return ''.join((get_convertor(v, self.type).format for v in self._value))

    def args_creator(self, value: T) -> List[Any]:
        assert self._value == value
        return sum([get_convertor(v, self.type).args_creator(v) for v in value], [])


def get_convertor(value, annotation):
    if is_dataclass(value):
        return DataClassTypeConvertor(value)
    if isinstance(annotation, type) and issubclass(annotation, ArrayTypeBase):
        return ArrayConvertor(value, annotation)
    else:
        return Convertors[annotation]


class EnumTypeConvertor(AbstractTypeConvertor):
    def __init__(self, _: T, type: Enum):
        self.size = type.REP

    def validator(self, value: T) -> bool:
        pass

    @property
    def format(self) -> str:
        pass

    @property
    def args_creator(self, value: T) -> List[Any]:
        pass


Convertors = {
    uint8_t: UIntegerTypeConvertor(8),
    uint16_t: UIntegerTypeConvertor(16),
    uint32_t: UIntegerTypeConvertor(32),
}


def handle(annotation, value):
    convertor = get_convertor(value, annotation)
    assert convertor.validator(value)
    format = convertor.format

    args = convertor.args_creator(value)
    print(annotation, args)
    return format, args


class DataClassTypeConvertor(AbstractTypeConvertor):
    def __init__(self, obj: dataclass):
        """ It is more efficient here to calculate it all ahead"""
        args = []
        format = ''
        annotations = get_type_hints(obj)
        obj_values = {key.name: obj.__dict__[key.name] for key in fields(obj)}
        for (var, annotation) in annotations.items():
            # TODO: Function to build the full struct format for unpacking
            # TODO: use asdict/astuple to build in the end - two dicts with the same keys should have the same order
            print(var, annotation, obj_values[var])
            f, a = handle(annotation, obj_values[var])
            format += f
            args += a

        self._obj = obj
        self._format = format
        self._args = args

    def validator(self, value: T) -> bool:
        assert value == self._obj
        return True

    @property
    def format(self) -> str:
        return self._format

    def args_creator(self, value: dataclass) -> List[Any]:
        assert value == self._obj
        return self._args


def internal_pack(obj: dataclass):
    d = DataClassTypeConvertor(obj)
    return d.format, d.args_creator(obj)


def pack(obj: dataclass, endianess='<'):
    format, args = internal_pack(obj)
    print(format)
    print(struct.calcsize(format))
    return struct.pack(endianess + format, *args)


def unpack(data: bytes, obj: dataclass):
    d = DataClassTypeConvertor((obj))
    return obj(struct.unpack(d.format, data))


@dataclass
class Shallom:
    lala: uint32_t


@dataclass
class Nino:
    a: uint8_t
    b: uint16_t
    c: ArrayType(ArrayType(uint8_t, 5), 2)
    s: Shallom


@dataclass
class Fuck:
    a: uint8_t

print(pack(Nino(15, 16, [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]], Shallom(0xffffefff))))

print(unpack('\xe8', Fuck))
