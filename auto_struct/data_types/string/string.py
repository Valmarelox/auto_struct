from ..array import Array
from .char import Char


def String(size):
    class String(Array(Char, size)):
        f"""
            String of size {size}
        """
        @property
        def end(self):
            return self._values.index(b'\x00')

        def __bytes__(self):
            return b''.join(self._values[:self.end])

        def __str__(self):
            return str(bytes(self), 'ascii')

        def __repr__(self):
            return f"'{str(self)}'"

    return String
