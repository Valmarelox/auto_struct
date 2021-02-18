from .base_type import BaseType


class BaseSingleValueType(BaseType):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __bytes__(self):
        return self.struct.pack(self.value)
