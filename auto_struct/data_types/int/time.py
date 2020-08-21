from time import localtime, asctime

from .unsigned_integer import uint32_t


class time_t(uint32_t):
    def __repr__(self):
        return "'{0}'".format(str(self))

    def as_localtime(self):
        return localtime(self)

    def __str__(self):
        return asctime(self.as_localtime())