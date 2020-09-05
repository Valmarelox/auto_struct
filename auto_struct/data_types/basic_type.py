from struct import Struct
from typing import Optional


class BaseTypeMeta(type):
    FORMAT = None

    @property
    def struct(cls) -> Optional[Struct]:
        if cls.FORMAT:
            return Struct(cls.FORMAT)
        return None

    def __len__(self):
        return self.struct.size


class BaseType(metaclass=BaseTypeMeta):
    @classmethod
    def parse(cls, data: bytes):
        assert len(cls) == len(data)
        return cls(*cls.struct.unpack(data))

    @classmethod
    def element_count(cls) -> int:
        return 1

    @classmethod
    def build_tuple_tree(cls, values):
        assert len(values) == 1, values
        return values
