from .errors import *
from .notes import Note, Line, Pair


def one(func):
    def wrapper(*args, **kwargs):
        if len(locals()["kwargs"]) != 1:
            raise NeedOneArg(func)

        return func(*args, **kwargs)
    return wrapper


def some(func):
    def wrapper(*args, **kwargs):
        if len(locals()["kwargs"]) == 0:
            raise NoArgs(func)

        return func(*args, **kwargs)
    return wrapper


class NoteUtil:
    """This class reads the note file and compiles it into separated tokens.
    Then it reads the tokens and makes a list of `Note`s, which can then be retrieved using various methods.
    
    .. note::
        
        All comparisons using ``content`` will be case insensitive. When looking for a single `Note` with ``content``,
        it will look for an exact match, and when looking for multiple `Note`s with ``content``, it will look to see
        if the passed ``content`` arg is ``in`` any `Note`'s ``content``.
    
    Parameters
    ----------
    file_name : :class:`str`
        The name of the file that has the raw notes. This file will be read and formatted into a .nu file
        that can be edited by the program.

        .. warning::
        
            The file must be in the current working directory to be detected. 
            
    separator : Optional[:class:`str`]
        The delimiter that distinguishes between each token.
    comment : Optional[:class:`str`]
        A prefix of a token in the file that will cause it to be ignored and not included in the .nu file.
        
    Attributes
    ----------
    notes: List[:class:`Note`]
        All `Note`s created from the .nu file.
    file_name: :class:`str`
        Name of the file without the any file extensions.
    separator: :class:`str`
        Delimiter that splits `Note` tokens.
    comment: :class:`str`
        Prefix of `Note` tokens that have been ignored.
    """

    def __init__(self, file_name: str, category_groups: list, note_groups: list, extension_groups: list,
                 *, separator: str="\n", comment: str=None):
        self.notes = []
        self.lines = []
        self.pairs = []
        self.positionals = []
        self.extensions = {}
        self.categories = {}

        self.file_name = file_name
        self.separator = separator
        self.comment = comment

        if self.file_name.endswith(".nu"):
            self._read_file()
        else:
            self._compile_file()
            self._read_file()

    def __repr__(self):
        pass

    def _compile_file(self):
        """Strips the file of white space, empty lines and comments. Writes the stripped contents into a .nu file."""

        with open(self.file_name, mode="r", encoding="UTF-8") as f:
            for line in f.read().split(self.separator):
                if self.comment is not None:
                    if line.startswith(self.comment):
                        continue

                line = line.strip()

                if self.comment is not None:
                    if line.startswith(self.comment):
                        continue

                if line == "":
                    continue

                if line not in self.notes:
                    self.notes.append(line)

        self.file_name = self.file_name.split(".")[0] + ".nu"
        with open(self.file_name, mode="w", encoding="UTF-8") as f:
            f.write(self.separator.join(self.notes))

    def _read_file(self):
        """Splits the .nu file by the ``separator`` and appends all of the tokens to the ``notes``."""

        # with open(self.note_file, mode="r", encoding="UTF-8") as f:
            # for i, line in enumerate(f.read().split(self.separator)):


        # for eg in self._egroups:
        #     if eg.name not in self.extensions:
        #         self.extensions[eg.name] = []
        #
        #     while True:
        #         try:
        #             i = self.content.index(eg.lbound)
        #         except IndexError:
        #             break
        #
        #         try:
        #             j = self.content.index(eg.rbound)
        #         except IndexError:
        #             raise NoRightBound
        #
        #         self.extensions[eg.name].append(Extension(eg, self.content[i + len(eg.lbound): j].strip(), self))
        #         eg.notes.append(self)
        #         self.content = self.content[:i].strip() + eg.placeholder + self.content[j + len(eg.rbound):].strip()

    def format(self):
        """Returns a formatted version of the notes.
        
        This is just the ``separator`` joined with the ``notes``.
        """

        return self.separator.join(self.notes)

    @one
    def nindex(self, *, content: str=None):
        """Finds the note index of a `Note` that has a certain attribute.
        
        Parameters
        ----------
        content : :class:`str`
            The text that the `Note` equals.
        """
        
        if content is not None:
            for note in self.notes:
                if content.lower() == note.content.lower():
                    return note.nindex
            raise NoteNotFound("No note was found to equal the content: {0}".format(content))

    @one
    def nindexes(self, *, content: str=None):
        """Finds all note indexes of `Note`s that have certain attributes.
        
        Parameters
        ----------
        content : :class:`str`
            The text that the `Note` contains.
        """
        
        nindexes = []
        if content is not None:
            for note in self.notes:
                if content.lower() in note.content.lower():
                    nindexes.append(note.nindex)
        if not nindexes:
            raise NoteNotFound("No note was found containing the content: {0}".format(content))
        return sorted(set(nindexes))

    @one
    def note(self, *, content: str=None, nindex: int=None):
        """Finds the `Note` that has a certain attribute.
        
        Parameters
        ----------
        content : :class:`str`
            The text that the `Note` content equals.
        nindex : :class:`int`
            The note index of the `Note`.
        """
        
        if nindex is not None:
            try:
                return self.notes[nindex]
            except IndexError:
                raise NoteIndexError("The note index: {0} was out of bounds of the notes.".format(nindex))
        if content is not None:
            for note in self.notes:
                if content.lower() == note.content.lower():
                    return note
            raise NoteNotFound("No note was found to equal content: {0}".format(content))

    @one
    def notes(self, *, content: str=None, nindexes: list=None):
        """Finds all `Note`s that have certain attributes.
        
        Parameters
        ----------
        content : :class:`str`
            The text that the `Note` contains.
        nindexes : List[:class:`int`]
            The note indexes of any amount of `Note`s.
        """
        
        notes = []
        if nindexes is not None:
            for nindex in nindexes:
                try:
                    notes.append(self.notes[nindex])
                except IndexError:
                    raise NoteIndexError("The note index: {0} was out of bounds of the notes.".format(nindex))
        if content is not None:
            for note in self.notes:
                if content.lower() in note.content.lower():
                    notes.append(note)

            if not notes:
                raise NoteNotFound("No note was found containing the content: {0}".format(content))
        return sorted(set(notes))

    @one
    def lindex(self, *, content: str=None, nindex: int=None):
        if nindex is not None:
            try:
                return self.notes[nindex].lindex
            except IndexError:
                raise NoteIndexError("The note index: {0} was out of bounds of the notes.".format(nindex))
            except AttributeError:
                raise LineExpected("The note at the note index: {0} was not a Line.".format(nindex))

        if content is not None:
            for line in self.lines:
                if content.lower() == line.content.lower():
                    return line.lindex
            raise LineNotFound("No line was found to equal the content: {0}".format(content))

    @one
    def lindexes(self, *, content: str=None, nindexes: list=None):

        lindexes = []
        if content is not None:
            for line in self.lines:
                if content.lower() in line.content.lower():
                    lindexes.append(line.lindex)

        if nindexes is not None:
            for nindex in nindexes:
                try:
                    lindexes.append(self.notes[nindex].lindex)
                except IndexError:
                    raise NoteIndexError(
                        "The note index: {0} was out of bounds of the notes.".format(nindex))
                except AttributeError:
                    raise LineExpected("The note at note index: {0} was not a Line.".format(nindex))

        if not lindexes:
            raise LineNotFound("No line was found with the content: {0} or "
                                      "have any of the nindexes: [1}".format(content, nindexes))
        return sorted(set(lindexes))

    @one
    def line(self, *, content: str=None, nindex: int=None, lindex: int=None):
        if nindex is not None:
            try:
                if isinstance(self.notes[nindex], Line):
                    return self.notes[nindex]
                else:
                    raise LineExpected("The note at note index: {0} was not a Line".format(nindex))
            except IndexError:
                raise NoteIndexError("The note index: {0} was out of bounds of the notes.".format(nindex))
        if lindex is not None:
            try:
                return self.lines[lindex]
            except IndexError:
                raise LineIndexError("The line index: {0} was out of bounds of the lines.".format(lindex))
        if content is not None:
            for line in self.lines:
                if line.content.lower() == content.lower():
                    return line
            raise LineNotFound("No line was found to equal content: {0}".format(content))

    @one
    def lines(self, *, content: str=None, nindexes: list=None, lindexes: list=None):
        lines = []

        if content is not None:
            for line in self.lines:
                if content.lower() in line.content.lower():
                    lines.append(line)
        if nindexes is not None:
            for nindex in nindexes:
                try:
                    if isinstance(self.notes[nindex], Line):
                        lines.append(self.notes[nindex])
                    else:
                        raise LineExpected("The note at note index: {0} was not a Line.".format(nindex))
                except IndexError:
                    raise NoteIndexError(
                        "The note index: {0} was out of bounds of the notes".format(nindex))
        if lindexes is not None:
            for lindex in lindexes:
                try:
                    lines.append(self.lines[lindex])
                except IndexError:
                    raise LineIndexError(
                        "The line index: {0} was out of bounds of the lines".format(lindex))

        if not lines:
            raise LineNotFound(
                "No line was found to contain content: {0} or have any indexes in: {1}".format(content, nindexes))
        return sorted(set(lines))

