import base64
import json
from struct import Struct
from typing import get_type_hints

from src.data_types.basic_type import BaseType


class BasicStruct(BaseType):
    # TODO: Call proper __init__ for annotation type
    def __post_init__(self):
        for (field, annotation) in self.annotations().items():
            if issubclass(annotation, BasicStruct):
                self.__dict__[field] = annotation(*self.__dict__[field])
            else:
                self.__dict__[field] = annotation(self.__dict__[field])

    @classmethod
    def element_count(cls) -> int:
        return len(cls.annotations())

    @classmethod
    def annotations(cls):
        return get_type_hints(cls)

    @classmethod
    def parse(cls, buffer: bytes):
        s = cls._generate_struct()
        args = []
        unpacked = s.unpack(buffer)
        print(unpacked)
        for (_, annotation) in cls.annotations().items():
            print(annotation)
            if annotation.element_count() > 1:
                args.append(tuple(unpacked[:annotation.element_count()]))
                unpacked = unpacked[annotation.element_count():]
            else:
                args.append(unpacked[0])
                unpacked = unpacked[1:]
        print(cls, args)
        return cls(*args)

    @classmethod
    def _generate_struct(cls):
        format = ''
        annotations = get_type_hints(cls)
        for (var, annotation) in annotations.items():
            # TODO: Function to build the full struct format for unpacking
            # TODO: use asdict/astuple to build in the end - two dicts with the same keys should have the same order
            format += annotation.format()
        return Struct(format)

    def to_json(self):
        def default_handle(x):
            if hasattr(x, '__dict__'):
                return x.__dict__
            elif isinstance(x, bytes):
                return base64.b64encode(x)
            else:
                raise TypeError('Can\'t encode {0}'.format(type(x)))
        return json.dumps(self.__dict__, default=default_handle)