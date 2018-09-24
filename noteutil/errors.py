class NotesError(Exception):
    pass


class NotesNotFound(NotesError):
    pass


class NotesIndexError(NotesNotFound):
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


class NoDefinitionError(NotesNotFound):
    pass


class DuplicateTermError(DuplicateError):
    pass


class MissingBoundError(NotesError):
    pass


class NoCategoryError(NotesNotFound):
    pass


class NoExtensionError(NotesNotFound):
    pass


