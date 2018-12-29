import abc
from .errors import *
from .groups import *


# TODO: __repr__ should be the function that is used to convert the Note back into something that can be read in .nu
# TODO: Revisit __repr__ for extensions and categories
class Note(abc.ABC):
    """Base class for all text Notes, which are created when parsing the note file.

    Attributes
    ----------
    content: :class:`str`
        The actual content of the notes; all of the text that was found in between separators.
    nindex: :class:`int`
        The note index that corresponds to position in the :attr:`NoteUtil.notes_list`.
    """

    def __init__(self, content: str, nindex: int, tabs: int, ngroup: NoteGroup,
                 *, extensions: dict = None, categories: list = None):
        super().__init__()
        self._rcontent = content
        self.content = content
        self.nindex = nindex
        self.tabs = tabs
        self.extensions = {} if extensions is None else extensions
        self.categories = [] if categories is None else categories

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
        return self.format()

    @abc.abstractmethod
    def __repr__(self):
        pass

    @abc.abstractmethod
    def format(self):
        pass


class Line(Note):

    def __init__(self, content: str, nindex: int, lindex: int, tabs: int, lgroup: LineGroup,
                 *, extensions: list = None, categories: list = None):
        super().__init__(content, nindex, tabs, lgroup, extensions=extensions, categories=categories)
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

    def format(self):
        return self.content


class Pair(Note):
    def __init__(self, content: str, nindex: int, pindex: int, separator: str, tabs: int, pgroup: PairGroup,
                 *, extensions: list = None, categories: list = None):
        super().__init__(content, nindex, tabs, pgroup, extensions=extensions, categories=categories)
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

    def format(self):
        return f"{self.term} {self.separator} {self.definition}"


from .categories import GlobalCategory
