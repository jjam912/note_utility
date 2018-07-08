class DelimeterError(Exception):
    pass


class MissingDelimeterError(DelimeterError):
    pass


class ExtraDelimeterError(DelimeterError):
    pass


class NoDefinitionError(Exception):
    pass


class TermAlreadyExistsError(Exception):
    pass


class MissingBoundError(Exception):
    pass
