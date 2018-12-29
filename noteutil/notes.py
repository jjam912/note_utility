import abc
from .errors import *


# The plan is that we will create everything needed to pass into the Note's constructor
# in the NoteUtil method and then just make the Note.
class Note(abc.ABC):
    """Base class for all notes, which are created when parsing the note file."""

    def __init__(self, rcontent: str, content: str, nindex: int, tabs: int, fmt, extensions: dict, categories: list):
        super().__init__()
        self._rcontent = rcontent
        self.content = content
        self.nindex = nindex
        self.tabs = tabs
        self._format = fmt
        self.extensions = extensions
        self.categories = categories

    def __eq__(self, other):
        return self.nindex == other.nindex

    def __ne__(self, other):
        return self.nindex != other.nindex

    def __lt__(self, other):
        return self.nindex < other.nindex

    def __gt__(self, other):
        return self.nindex > other.nindex

    def __hash__(self):
        return hash(self._rcontent.lower())

    def __str__(self):
        return self._format()

    @abc.abstractmethod
    def __repr__(self):
        pass


# A single token of notes refers to the string that is in between the NoteUtil's separators in the .nu file.
class Line(Note):
    """A single token of notes.

    Attributes
    ----------
    content: :class:`str`
        The actual content of the Line; all of the text that was found in between separators.
    nindex: :class:`int`
        The `Note` index that corresponds to the position in the :attr:`NoteUtil.notes_list`.
    lindex: :class:`int`
        The `Line` index that corresponds to the position in the :attr:`NoteUtil.lines_list`.
    tabs: :class:`int`
        The number of tabs that indicates how nested this `Line` is (one per category).
    extensions: List[:class:`Extension`]
        An unsorted list of the extensions that this `Line` has.
    categories: List[:class:`Category`]
        An unsorted list of all of the categories this `Line` belongs to.
    """

    def __init__(self, rcontent: str, content: str, nindex: int, lindex: int,
                 tabs: int, fmt, extensions: dict, categories: list):
        super().__init__(rcontent, content, nindex, tabs, fmt, extensions, categories)
        self.lindex = lindex

    def __repr__(self):
        rstring = ""
        rstring += self.content
        for ext in self.extensions:
            rstring += repr(ext)
        for cat in reversed(self.categories):
            if isinstance(cat, GlobalCategory):
                rstring = cat.prefix + rstring
        return rstring


# A Note token will automatically become a Pair if its separator is in the rcontent.
class Pair(Note):
    """A single token of notes with a separator that splits a term and a definition.

    Attributes
    ----------
    content: :class:`str`
        The actual content of the notes; all of the text that was found in between separators.
    nindex: :class:`int`
        The note index that corresponds to the position in the :attr:`NoteUtil.notes_list`.
    pindex: :class:`int`
        The pair index that corresponds to the position in the :attr:`NoteUtil.pairs_list`.
    separator: :class:`str`
        The string that separates the key and value (term and definition) of the notes token.
    term: :class:`str`
        The first part that came before the `Pair`'s separator.
    definition :class:`str`
        The second part that came after the `Pair`'s separator.
    tabs: :class:`int`
        The number of tabs that indicates how nested this note is (one per category).
    extensions: List[:class:`Extension`]
        An unsorted list of the extensions that this `Note` has.
    categories: List[:class:`Category`]
        An unsorted list of all of the categories this `Note` belongs to.
    """

    def __init__(self, rcontent: str, content: str, nindex: int, pindex: int, separator: str,
                 tabs: int, fmt, extensions: dict, categories: list):
        super().__init__(rcontent, content, nindex, tabs, fmt, extensions, categories)
        self.pindex = pindex
        self.separator = separator

        tokens = tuple(content.split(separator))
        if len(tokens) != 2:
            raise SeparatorError(content)

        self.term, self.definition = tokens[0].strip(), tokens[1].strip()

    def __repr__(self):
        rstring = ""
        rstring += f"{self.term} {self.separator} {self.definition}"
        for ext in self.extensions:
            rstring += repr(ext)
        for cat in reversed(self.categories):
            if isinstance(cat, GlobalCategory):
                rstring = cat.prefix + rstring
        return rstring


from .categories import GlobalCategory
