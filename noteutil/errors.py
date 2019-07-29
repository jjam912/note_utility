class NoteUtilError(Exception):
    """Superclass for all NoteUtil exceptions."""

    pass


class ConfigError(NoteUtilError):
    """Superclass for exceptions raised during the Config parsing process."""

    pass


class UnexpectedLine(ConfigError):
    def __init__(self, index):
        super().__init__("There was an unexpected line after an option at Line {0}".format(index + 1))


class ExtraLine(ConfigError):
    def __init__(self, index):
        super().__init__("There are two or more blank lines at Line {0}".format(index + 1))


class NoteError(NoteUtilError):
    """Superclass for exceptions raised during the Note creating process."""

    pass


class IncorrectConfig(NoteError):
    def __init__(self, lines):
        super().__init__("There was an "
                         "incorrect number of lines in the config file: {0} (should be at least 13).".format(lines))


class NoteFileNotFound(NoteError):
    def __init__(self, file_name):
        super().__init__("The file: {0} was not found".format(file_name))


class ExtraSeparator(NoteError):
    def __init__(self, content):
        super().__init__("There was more than one separator in the line content: {0}".format(content))


class DuplicateTerm(NoteError):
    def __init__(self, term):
        super().__init__("There was already a term of the name: {0}".format(term))


class NoDefinition(NoteError):
    def __init__(self, content):
        super().__init__("There was no text after the separator in the line content: {0}".format(content))


class HeadingJump(NoteError):
    def __init__(self, content, previous_level, current_level):
        super().__init__("The heading level jumped down 2 or more levels: From level {0} to {1} in content: {2}".
                         format(previous_level, current_level, content))


class MissingBound(NoteError):
    def __init__(self, content, lbound, rbound):
        super().__init__("The left bound: {0} was found, but there was no right bound: {1} in content: {2}".format(
            lbound, rbound, content))


class NindexError(NoteUtilError, IndexError):
    def __init__(self, nindex):
        super().__init__("The nindex was out of bounds: {0}".format(nindex))


class QuizError(Exception):
    """Superclass for all Quiz exceptions."""

    pass


class HeadingExpected(QuizError):
    def __init__(self, note):
        super().__init__("The note was expected to be a heading, but wasn't: {0}".format(note.rcontent))


class DivisionNotFound(QuizError):
    def __init__(self, heading_name):
        super().__init__("The division name wasn't found: {0}".format(heading_name))


class LeitnerError(Exception):
    """Superclass for all Leitner exceptions."""

    pass


class TimeTooShort(LeitnerError):
    def __init__(self, time):
        super().__init__("The time period for the box must be longer than the last box: (> {0})".format(time))


class TimeTooLong(LeitnerError):
    def __init__(self, time):
        super().__init__("The time period for the box must be shorter than the box after it: (< {0})".format(time))


class BoxNumberError(LeitnerError, KeyError):
    def __init__(self, box):
        super().__init__("The box number was out of bounds: {0}".format(box))


class LastBox(LeitnerError):
    def __init__(self):
        super().__init__("The number of boxes are not allowed to be less than 1.")

