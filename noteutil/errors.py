class NotesError(Exception):
    pass


class NotesNotFound(NotesError):
    pass


class NotesIndexError(NotesError):
    pass


class NoArgsPassed(NotesError):
    pass


