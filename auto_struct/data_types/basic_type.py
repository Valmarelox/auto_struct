from struct import Struct


class BaseType:
    FORMAT = None

    def __init__(self):
        self._basic_type_struct = None

    @classmethod
    def _generate_struct(self):
        return Struct(self.FORMAT)

    @property
    def struct(self) -> Struct:
        if not self._basic_type_struct:
            self._basic_type_struct: Struct = self._generate_struct()
        return self._basic_type_struct

    @classmethod
    def format(self):
        return self._generate_struct().format

    @property
    def __len__(self):
        return self.struct.size

    @classmethod
    def element_count(cls) -> int:
        return 1

    @classmethod
    def _build_tuple_tree(cls, values):
        assert len(values) == 1, values
        return values