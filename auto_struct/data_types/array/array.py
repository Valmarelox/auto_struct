from typing import Sequence, Type

from ..basic_type import BaseType


def Array(element: Type[BaseType], size: int):
    assert isinstance(size, int) and size > 0

    class Array(BaseType):
        FORMAT = '{size}{format}'.format(size=size, format=element.struct.format)

        def __init__(self, *values: Sequence[element]):
            super().__init__()
            assert len(values) == size
            self.values = values

        def __getitem__(self, item: int) -> element:
            return self.values[item]

        def __setitem__(self, key: int, value: element):
            self.values = self.values[:key] + value + self.values[key + 1:]

        @classmethod
        def element_type(cls):
            return element

        @classmethod
        def element_count(cls) -> int:
            return size

        def __repr__(self):
            return repr(self.values)

        def __str__(self):
            return str(self.values)

        def __bytes__(self):
            return bytes(self.values)

        def __iter__(self):
            for x in self.values:
                yield x

        def __eq__(self, other):
            return all((x == element(y)) for (x, y) in zip(self, other))

        @classmethod
        def build_tuple_tree(cls, values):
            assert len(values) == cls.element_count()
            return values

        def to_json(self):
            return self.values

    return Array
