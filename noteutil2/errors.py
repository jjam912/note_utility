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
