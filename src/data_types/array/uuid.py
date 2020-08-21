import uuid

from src.data_types.array.array import Array
from src.data_types.int.unsigned_integer import uint8_t


class UUID(Array(uint8_t, 16)):
    def __str__(self):
        return str(uuid.UUID(bytes=bytes(self)))

    def __repr__(self):
        return "'{0}'".format(str(self))