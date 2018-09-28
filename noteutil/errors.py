class NotesError(Exception):
    """Base exception for all ``noteutil`` modules."""
    
    pass


class NotesNotFound(NotesError):
    """This exception is thrown when no `Note`_ is found in the ``notes_list`` with the given arguments."""
    
    pass


class NotesIndexError(NotesError):
    """This exception is thrown when a ``nindex`` is passed that is out of range of the ``notes_list``."""
    
    pass


class NoArgsPassed(NotesError):
    """This exception is thrown when no arguments are passed into a function of any `NoteUtil`_ that needs at least one.
    
    If all of the arguments of a function are ``None``, this exception will be thrown.
    """
    
    pass


class NotALine(NotesError):
    """This exception is thrown when a `Line`_ or subclass of `Line`_ was expected from the ``notes_list``.
    
    This should theoretically never happen because all `Note`_\ s automatically convert to `Line`_\ s.
    """
    
    pass

