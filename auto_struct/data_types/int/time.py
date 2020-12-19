from time import localtime, asctime

from .unsigned_integer import uint32_t, uint64_t

class TimeMixin:
    """
        Mixin extending an integer type to represent time in seconds since an epoch
    """
    def __repr__(self):
        return f"'{str(self)}'"

    def as_localtime(self):
        return localtime(self)

    def __str__(self):
        return asctime(self.as_localtime())


class time_t(uint32_t, TimeMixin):
    """
        32-bit unsigned integer representing seconds since epoch
    """

class time64_t(uint64_t, TimeMixin):
    """
        64-bit unsigned integer representing seconds since epoch
    """
