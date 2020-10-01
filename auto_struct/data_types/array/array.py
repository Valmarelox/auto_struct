from typing import Sequence, Type, Any

from ..basic_type import BaseType
from ...exceptions.type import ElementCountException


def Array(element: Type[BaseType], size: int):
    if not isinstance(size, int) or size <= 0:
        raise ElementCountException(f'Invalid size for array: {size}')

    class Array(BaseType):
        FORMAT = element.struct.format * size

        def __init__(self, *values: Sequence[element]):
            super().__init__()
            if len(values) != self.element_count():
                raise ElementCountException(f'Array received {len(values)} elements, expected: {self.element_count()}')
            self.values = [element(*x) if element.element_count() > 1 else element(x) for x in values]

        def __getitem__(self, item: int) -> element:
            return self.values[item]

        def __setitem__(self, key: int, value: element):
            self.values = self.values[:key] + value + self.values[key + 1:]

        @classmethod
        def element_type(cls) -> Type[BaseType]:
            return element

        @classmethod
        def element_count(cls) -> int:
            return size

        @classmethod
        def _rec_element_count(cls):
            return cls.element_count() * cls.element_type()._rec_element_count()

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
        def build_tuple_tree(cls, values) -> Sequence[Any]:
            if len(values) != cls._rec_element_count():
                raise ElementCountException(f'build_tuple_tree received {len(values)} elements, expected: {cls._rec_element_count()}')
            if cls.element_type().element_count() == 1:
                return values
            e = cls.element_type()
            ers = e._rec_element_count()
            return tuple(e.build_tuple_tree(values[x:x+ers]) for x in range(0, len(values), e._rec_element_count()))

        def to_json(self):
            return self.values

    return Array
