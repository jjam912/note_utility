import abc
from .errors import *


# The plan is that we will create everything needed to pass into the Note's constructor
# in the NoteUtil method and then just make the Note.
class Note(abc.ABC):

    # Order of constructor args: content, hidden content, outside content, outside hidden content.
    def __init__(self, content, nindex, rcontent, prefix, extensions, categories, tabs, fmt):
        """
        Base class for all notes, which are created when parsing the note file.

        Parameters
        ----------
        content : str
            The content of the `Note` excluding `prefixes` and `Extensions`.
        nindex : int
            The `Note` index that corresponds to the position in the `NoteUtil.notes_list`.
        rcontent : str
            Raw content of the `Note`.
        prefix : str
            Any prefixes this `Note` had that were used to determine the type of `Note` or `Category`.
        extensions: dict of {str : `Extension`}
            A dict of the `Extensions` this `Note` has with key: `Extension.name` and value: `Extension`.
        categories: list of `Category`
            An unsorted list of all of the `Categories` this `Note` belongs to.
        tabs: int
            The number of tabs that indicates how nested this `Note` is (one per `Category`).
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


class Line(Note):
    """A single token of text.

    This is all of the text that is found in between two of a `NoteUtil's` `separators` in the .nu file.

    Attributes
    ----------
    content: str
        The actual content of the `Line`; all of the text that was found in between the `separators`.
    nindex: int
        The `Note` index that corresponds to the position in the `NoteUtil.notes_list`.
    lindex: int
        The `Line` index that corresponds to the position in the `NoteUtil.lines_list`.
    extensions: dict of {str : `Extension`}
        A dict of the `Extensions` that this `Line` has with key: `Extension.name` and value `Extension`.
    categories: list of `Category`
        An unsorted list of all of the `Categories` this `Line` belongs to.
    """

    def __init__(self, content, nindex, lindex, rcontent, prefix, extensions, categories, tabs, fmt):
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


class Pair(Note):
    """A single token of notes with a separator that splits a term and a definition.

    A `Note` will automatically become a `Pair` if its `separator` is in the `rcontent` of the `Note`.
    This holds true unless the `rcontent` contains the `prefix` of a `LineGroup`.

    Attributes
    ----------
    content: str
        The actual content of the `Notes`; all of the text that was found in between `separators`.
    nindex: int
        The `Note` index that corresponds to the position in the `NoteUtil.notes_list`.
    pindex: int
        The `Pair` index that corresponds to the position in the `NoteUtil.pairs_list`.
    separator: str
        The string that separates the key and value (term and definition) of the `Note` token.
    term: str
        The first part of text that came before the `separator`.
    definition: str
        The second part of text that came after the `separator`.
    extensions: dict of {str : `Extension`}
        A dict of the `Extensions` that this `Pair` has with key: `Extension.name` and value `Extension`.
    categories: list of `Category`
        An unsorted list of all of the `Categories` this `Pair` belongs to.
    """

    def __init__(self, content, nindex, pindex, separator, rcontent, prefix, extensions, categories, tabs, fmt):
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
