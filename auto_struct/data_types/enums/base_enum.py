from struct import Struct
from types import FunctionType
from typing import Optional, Sequence, Any, Dict

from auto_struct.data_types.basic_type import BaseTypeMeta, BaseType


class BaseEnumMeta(BaseTypeMeta):

    def __new__(metacls, cls: str, bases: Sequence[type], classdict: Dict[str, Any]):

        ELEMENT_TYPE = '__ELEMENT_TYPE__'
        if ELEMENT_TYPE in classdict:
            element_type = classdict[ELEMENT_TYPE]
        else:
            for base in bases:
                if hasattr(base, ELEMENT_TYPE):
                    element_type = base.__ELEMENT_TYPE__
            else:
                raise TypeError()

        values = {}
        for key in classdict.copy():
            if not key.startswith('_') and not isinstance(classdict[key], FunctionType):
                values[key] = element_type(classdict[key])
        classdict['__VALUES__'] = values

        cls = super().__new__(metacls, cls, bases, classdict)

        for item in values:
            setattr(cls, item, cls(cls.__dict__[item]))
        return cls

    @property
    def struct(cls) -> Optional[Struct]:
        return cls.__ELEMENT_TYPE__.struct


class BaseEnum(BaseType, metaclass=BaseEnumMeta):
    __ELEMENT_TYPE__ = type(None)

    def __init__(self, value):
        assert value in self.__VALUES__.values(), value
        self._value = self.__ELEMENT_TYPE__(value)

    def __repr__(self):
        for (key, value) in self.__VALUES__.items():
            if self._value == value:
                return '{0}.{1}'.format(type(self).__name__, key)

    def __int__(self):
        return int(self._value)

    def __str__(self):
        return str(self._value)

    def __bytes__(self):
        return bytes(self._value)

    def __bool__(self):
        return bool(self._value)

    def to_json(self):
        return self._value
