class NoteUtilError(Exception):
    """Base exception for all ``noteutil`` modules."""
    
    pass


class NoteNotFound(NoteUtilError):
    """This exception is thrown when no `Note`_ is found in the ``notes_list`` with the given arguments."""
    
    pass


class NoteIndexError(NoteUtilError):
    """This exception is thrown when a ``nindex`` is passed that is out of range of the ``notes_list``."""
    
    pass


class NoArgsPassed(NoteUtilError):
    """This exception is thrown when no arguments are passed into a function of any `NoteUtil`_ that needs at least one.
    
    If all of the arguments of a function are ``None``, this exception will be thrown.
    """
    
    pass


class LineExpected(NoteUtilError):
    """This exception is thrown when a `Line`_ or subclass of `Line`_ was expected from the ``notes_list``.
    
    This should theoretically never happen because all `Note`_\ s automatically convert to `Line`_\ s.
    """
    
    pass


class LineNotFound(NoteNotFound):
    """This exception is thrown when no `Line`_ is found in the ``lines_list`` with the given arguments."""

    pass


class LineIndexError(NoteIndexError):
    """This exception is thrown when a ``lindex`` is passed that is out of range of the ``lines_list``."""

    pass
