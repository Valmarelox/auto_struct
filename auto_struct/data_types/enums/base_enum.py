from struct import Struct
from types import FunctionType
from typing import Optional, Sequence, Any, Dict

from auto_struct.data_types.basic_type import BaseTypeMeta, BaseType


class BaseEnumMeta(BaseTypeMeta):

    def __new__(mcs, cls: str, bases: Sequence[type], classdict: Dict[str, Any]):
        element_type_name = '__ELEMENT_TYPE__'
        if element_type_name in classdict:
            element_type = classdict[element_type_name]
        else:
            for base in bases:
                if hasattr(base, element_type_name):
                    element_type = base.__ELEMENT_TYPE__
                    break
            else:
                raise TypeError('__ELEMENT_TYPE__ Not defined for class {0}'.format(cls))

        values = {}
        for key in classdict.copy():
            if not key.startswith('_') and not isinstance(classdict[key], FunctionType):
                values[key] = element_type(classdict[key])
        classdict['__VALUES__'] = values

        cls = super().__new__(mcs, cls, bases, classdict)

        for item in values:
            setattr(cls, item, cls(cls.__dict__[item]))
        return cls

    @property
    def struct(cls) -> Optional[Struct]:
        return cls.__ELEMENT_TYPE__.struct


class BaseEnum(BaseType, metaclass=BaseEnumMeta):
    __ELEMENT_TYPE__ = type(None)

    def __init__(self, value):
        self.value = self.__ELEMENT_TYPE__(value)
        self.verify()

    def verify(self):
        assert self.value in self.__VALUES__.values(), '{} {}'.format(self.value, self.__VALUES__)

    def __repr__(self):
        for (key, value) in self.__VALUES__.items():
            if self.value == value:
                return '{0}.{1}'.format(type(self).__name__, key)

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return str(self.value)

    def __bytes__(self):
        return bytes(self.value)

    def __bool__(self):
        return bool(self.value)

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def to_json(self):
        return self.value

