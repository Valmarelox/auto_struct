from ..int import uint8_t
from ..array import Array


def Padding(size):
    class Padding(Array(uint8_t, size)):
        FORMAT = f'{size}B'

        def __bytes__(self):
            return b''.join(self)
    return Padding
