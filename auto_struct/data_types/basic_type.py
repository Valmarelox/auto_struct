from struct import Struct


class BaseType:
    FORMAT = None

    def __init__(self):
        self._struct = None

    @classmethod
    def _generate_struct(self):
        return Struct(self.FORMAT)

    @property
    def struct(self) -> Struct:
        if not self._struct:
            self._struct: Struct = self._generate_struct()
        return self._struct

    @classmethod
    def format(self):
        return self._generate_struct().format

    @property
    def __len__(self):
        return self.struct.size

    @classmethod
    def element_count(cls) -> int:
        return 1