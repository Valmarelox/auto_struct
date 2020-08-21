from .string import String


def Padding(size):
    class Padding(String):
        FORMAT = '{0}B'.format(size)
        pass
    return Padding
