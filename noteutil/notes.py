import abc
from .errors import *


# The plan is that we will create everything needed to pass into the Note's constructor
# in the NoteUtil method and then just make the Note.
class Note(abc.ABC):
    """Base class for all notes, which are created when parsing the note file."""

    # Order of constructor args: content, hidden content, outside content, outside hidden content.
    def __init__(self, content: str, nindex: int, rcontent: str, prefix: str,
                 extensions: dict, categories: list, tabs: int, fmt):
        """
        Parameters
        ----------
        content : :class:`str`
            The content of the note excluding prefixes and extensions.
        nindex : :class:`int`
            The `Note` index that corresponds to the position in the :attr:`NoteUtil.notes_list`.
        rcontent : :class:`str`
            Raw content of the `Note`.
        prefix : :class:`str`
            Any prefixes this `Note` had to determine type of `Note` or `Category`.
        extensions: Dict[:class:`str` : :class:`Extension`]
            A dict of the extensions that this `Note` has with key: :attr:`Extension.name` and value :class:`Extension`.
        categories: List[:class:`Category`]
            An unsorted list of all of the categories this `Note` belongs to.
        tabs: :class:`int`
            The number of tabs that indicates how nested this `Note` is (one per category).
        fmt: function
            The function applied to a `Note` to give it its `str` value.
            Must take a `Note` as a parameter.
        """
        super().__init__()
        self.content = content
        self.nindex = nindex
        self._rcontent = rcontent
        self._prefix = prefix
        self.extensions = extensions
        self.categories = categories
        self._tabs = tabs
        self._format = fmt

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
        return self._format(self)

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
    extensions: Dict[:class:`str` : :class:`Extension`]
        A dict of the extensions that this `Line` has with key: :attr:`Extension.name` and value :class:`Extension`.
    categories: List[:class:`Category`]
        An unsorted list of all of the categories this `Line` belongs to.
    """

    def __init__(self, content: str, nindex: int, lindex: int, rcontent: str, prefix: str,
                 extensions: dict, categories: list, tabs, fmt):
        super().__init__(content, nindex, rcontent, prefix, extensions, categories, tabs, fmt)
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


# A Note token will automatically become a Pair if its separator is in the rcontent
# unless it has the prefix of a LineGroup.
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
        The first part that came before the separator.
    definition: :class:`str`
        The second part that came after the separator.
    extensions: Dict[:class:`str` : :class:`Extension`]
        A dict of the extensions that this `Pair` has with key: :attr:`Extension.name` and value :class:`Extension`.
    categories: List[:class:`Category`]
        An unsorted list of all of the categories this `Note` belongs to.
    """

    def __init__(self, content: str, nindex: int, pindex: int, separator: str, rcontent: str, prefix: str,
                 extensions: dict, categories: list, tabs, fmt):
        super().__init__(content, nindex, rcontent, prefix, extensions, categories, tabs, fmt)
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
