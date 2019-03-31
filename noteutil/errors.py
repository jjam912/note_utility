class NoteUtilError(Exception):
    """Base exception for all ``NoteUtil`` errors."""

    pass


# Note Exceptions
class NoteError(Exception):
    pass


class LineError(NoteError):
    pass


class PairError(NoteError):
    pass


class SeparatorError(PairError):
    def __init__(self, content: str):
        super().__init__("There was either zero or more than one separator in the content: {0}".format(content))


# Extension Exceptions
class ExtensionError(Exception):
    pass


class NoRightBound(ExtensionError):
    pass


class NoSeparators(ExtensionError):
    def __init__(self):
        super().__init__("There must be at least one `separator` in `separators`.")


class NoBullets(ExtensionError):
    def __init__(self):
        super().__init__("There must be at least one `bullet` in `bullets`.")


# Category Exceptions
class CategoryError(Exception):
    pass


# Group Exceptions
class GroupError(Exception):
    pass


class AbstractGroupError(GroupError):
    def __init__(self, cls):
        super().__init__(cls.__name__ + " is an abstract Group that cannot be implemented")


# More general Note Exceptions
class NoteNotFound(NoteUtilError):
    """This exception is thrown when no `Note`_ is found in the ``notes`` with the given arguments."""

    pass


class NoteIndexError(NoteUtilError):
    """This exception is thrown when a ``nindex`` is passed that is out of range of the ``notes``."""
    
    pass


class LineExpected(NoteUtilError):
    """This exception is thrown when a `Line`_ or subclass of `Line`_ was expected from the ``notes``.
    
    This should theoretically never happen because all `Note`_\ s automatically convert to `Line`_\ s.
    """
    
    pass


class LineNotFound(NoteNotFound):
    """This exception is thrown when no `Line`_ is found in the ``lines`` with the given arguments."""

    pass


class LineIndexError(NoteIndexError):
    """This exception is thrown when a ``lindex`` is passed that is out of range of the ``lines``."""

    pass


class PairExpected(NoteUtilError):
    pass


class PairNotFound(NoteNotFound):
    pass


class PairIndexError(NoteIndexError):
    pass


class NoArgs(NoteUtilError):
    """This exception is thrown when no arguments are passed into a function of any `NoteUtil`_ that needs at least one.

    If all of the arguments of a function are ``None``, this exception will be thrown.
    """

    def __init__(self, func):
        super().__init__("At least one argument must be passed to " + func.__name__)


class NeedOneArg(NoteUtilError):
    def __init__(self, func):
        super().__init__("Only one argument may be passed to " + func.__name__)


