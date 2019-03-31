class NoteUtilError(Exception):
    """Superclass for all `NoteUtil` exceptions."""

    pass


class NoteError(NoteUtilError):
    """Superclass for exceptions raised during the `Note` creating process."""

    pass


class ExtraSeparator(NoteError):
    def __init__(self, content):
        super().__init__("There was more than one separator in the line content: {0}".format(content))


class NoDefinition(NoteError):
    def __init__(self, content):
        super().__init__("There was no text after the separator in the line content: {0}".format(content))


class HeadingJump(NoteError):
    def __init__(self, previous_level, current_level):
        super().__init__("The heading level jumped down 2 or more levels: From level {0} to {1}".
                         format(previous_level, current_level))



