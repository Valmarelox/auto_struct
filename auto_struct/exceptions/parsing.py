from .base import AutoStructValueException, AutoStructTypeException


class StructSubParseException(AutoStructValueException):
    pass


class StructDefinitionException(AutoStructTypeException):
    pass

