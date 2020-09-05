from ..array import Array
from .char import Char


def String(size):
    class String(Array(Char, size)):
        @property
        def end(self):
            return self.values.index(b'\x00')

        def __bytes__(self):
            return b''.join(self.values[:self.end])

        def __str__(self):
            return str(bytes(self), 'ascii')

        def __repr__(self):
            return "'{0}'".format(str(self))

    return String
