import json
from io import IOBase, BufferedIOBase
from struct import Struct
from typing import get_type_hints, Sequence, Any, Type, Dict, Union

from .basic_type import BaseType, BaseTypeMeta, create_struct
from ..exceptions.type import TypeJSONEncodeException, ElementCountException


class BaseStructMeta(BaseTypeMeta):
    @property
    def struct(cls) -> Struct:
        fmt = ''
        annotations = get_type_hints(cls)
        for (var, annotation) in annotations.items():
            # TODO: Function to build the full struct format for unpacking
            # TODO: use asdict/astuple to build in the end - two dicts with the same keys should have the same order
            fmt += annotation.struct.format
        return create_struct(fmt)


class BasicStruct(BaseType, metaclass=BaseStructMeta):
    """
    Basic struct type to be used with dataclasses
    e.g

    @dataclass
    class Message(BasicStruct):
        type: uint32_t
        data: Array(uint8_t, 128)

    print(Message(1, [0] * 128))
    print(Message.parse('\x01' + '\x00' * 128))
    """
    def __post_init__(self):
        for (field, annotation) in self.annotations().items():
            self.__dict__[field] = annotation(*self.__dict__[field])

    @classmethod
    def annotations(cls) -> Dict[str, Type]:
        return get_type_hints(cls)

    @classmethod
    def element_count(cls) -> int:
        return len(cls.annotations())

    @classmethod
    def _rec_element_count(cls):
        return sum(a._rec_element_count() for (_, a) in cls.annotations().items())

    @classmethod
    def build_tuple_tree(cls, values: Sequence[Any]) -> Sequence[Any]:
        if len(values) != cls._rec_element_count():
             raise ElementCountException(f'build_tuple_tee received {len(values)} elements, expected: {cls._rec_element_count()}')
        args = []
        for (_, annotation) in cls.annotations().items():
            args.append(annotation.build_tuple_tree(values[:annotation._rec_element_count()]))
            values = values[annotation._rec_element_count():]
        return args

    @classmethod
    def parse(cls, buffer: Union[BufferedIOBase, Sequence]) -> 'BasicStruct':
        if isinstance(buffer, BufferedIOBase):
            buffer = buffer.read(len(cls))
        buffer = bytearray(buffer)
        unpacked = cls.struct.unpack(buffer)
        args = cls.build_tuple_tree(unpacked)
        return cls(*args)

    def to_json(self) -> str:
        def default_handle(x):
            if hasattr(x, 'to_json'):
                return x.to_json()
            if hasattr(x, '__dict__'):
                return x.__dict__
            raise TypeJSONEncodeException(f'Can\'t encode {type(x)}')

        return json.dumps(self.__dict__, default=default_handle)
