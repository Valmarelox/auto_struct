from struct import Struct
from typing import Optional, Sequence, Any

from auto_struct.exceptions.type import ElementCountException


def create_struct(fmt: str) -> Struct:
    return Struct('=' + fmt.replace('=', ''))


class BaseTypeMeta(type):
    FORMAT = None

    @property
    def struct(cls) -> Optional[Struct]:
        if cls.FORMAT:
            return create_struct(cls.FORMAT)
        return None

    def __len__(self) -> int:
        return self.struct.size


class BaseType(metaclass=BaseTypeMeta):
    """
        BasicType the entire module inherits, allows automatic packing and unpacking of datatypes
    """

    @classmethod
    def parse(cls, data: bytes):
        if len(cls) != len(data):
            raise ElementCountException(f'{cls.__name__} received {len(data)} elements, expected: {len(cls)}')
        return cls(*cls.struct.unpack(data))

    @classmethod
    def element_count(cls) -> int:
        return 1

    @classmethod
    def _rec_element_count(cls):
        return cls.element_count()

    @classmethod
    def build_tuple_tree(cls, values) -> Sequence[Any]:
        if len(values) != 1:
            raise ElementCountException(f'{cls.__name__} received {len(values)} elements, expected: 1')
        return values

    def __hash__(self):
        return hash(self._rec_element_count()) + hash(type(self))

    @property
    def struct(self):
        return type(self).struct

    def __len__(self):
        return len(type(self))
