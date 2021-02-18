from struct import Struct
from types import FunctionType
from typing import Optional, Sequence, Any, Dict

from auto_struct.data_types.base.base_type import BaseTypeMeta, BaseType
from auto_struct.exceptions.enum import NoSuchEnumElement


class BaseEnumMeta(BaseTypeMeta):

    def __new__(mcs, cls: str, bases: Sequence[type], classdict: Dict[str, Any]):
        element_type = classdict.get('__ELEMENT_TYPE__', None)
        if not element_type:
            for base in bases:
                if hasattr(base, '__ELEMENT_TYPE__'):
                    element_type = base.__ELEMENT_TYPE__
                    break
            else:
                raise TypeError(f'__ELEMENT_TYPE__ Not defined for class {cls}')

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
        # TODO: IS this this?
        self.value = self.__ELEMENT_TYPE__(value)
        self.verify()

    def verify(self) -> bool:
        if self.value not in self.__VALUES__.values():
            raise NoSuchEnumElement(f'Value {self.value} not in enum {type(self).__name__}')

    def __repr__(self):
        for (key, value) in self.__VALUES__.items():
            if self.value == value:
                return f'{type(self).__name__}.{key}'

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return str(self.value)

    def __bytes__(self):
        return bytes(self.value)

    def __bool__(self):
        return bool(self.value)

    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value

    def to_json(self):
        return self.value

    def __hash__(self):
        return hash(self.value)
