class NotesError(Exception):
    pass


class NotesNotFoundError(NotesError):
    pass


class NotesIndexError(NotesNotFoundError):
    pass


class ForbiddenEdit(NotesError):
    pass


class DuplicateError(NotesError):
    pass


class MultipleFoundError(NotesError):
    pass


class DelimeterError(NotesError):
    pass


class MissingDelimeterError(DelimeterError):
    pass


class ExtraDelimeterError(DelimeterError):
    pass


class NoDefinitionError(NotesNotFoundError):
    pass


class DuplicateTermError(DuplicateError):
    pass


class MissingBoundError(NotesError):
    pass


class NoCategoryError(NotesNotFoundError):
    pass


class NoExtensionError(NotesNotFoundError):
    pass


