from typing import Sequence

from src.data_types.basic_type import BaseType


def Array(element: BaseType, size: int):
    assert isinstance(size, int) and size > 0

    class Array(BaseType):
        FORMAT = '{size}{format}'.format(size=size, format=element.format())

        def __init__(self, values: Sequence[element]):
            super().__init__()
            assert len(values) == size
            self.values = values

        def __getitem__(self, item: int) -> element:
            return self.values[item]

        def __setitem__(self, key: int, value: element):
            self.values[key] = value

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

    return Array
