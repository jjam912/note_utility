class NoteUtilError(Exception):
    """Superclass for all `NoteUtil` exceptions."""

    pass


class ConfigError(NoteUtilError):
    """Superclass for exceptions raised during the `Config` parsing process."""

    pass


class UnexpectedLine(ConfigError):
    def __init__(self, index):
        super().__init__("There was an unexpected line after an option at Line {0}".format(index + 1))


class ExtraLine(ConfigError):
    def __init__(self, index):
        super().__init__("There are two or more blank lines at Line {0}".format(index + 1))


class NoteError(NoteUtilError):
    """Superclass for exceptions raised during the `Note` creating process."""

    pass


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


class QuizError(Exception):
    """Superclass for all `Quiz` exceptions."""

    pass


class HeadingExpected(QuizError):
    def __init__(self, note):
        super().__init__("The note was expected to be a heading, but wasn't: {0}".format(note.raw()))


class HeadingNotFound(QuizError):
    def __init__(self, heading_name):
        super().__init__("The heading name wasn't found: {0}".format(heading_name))



