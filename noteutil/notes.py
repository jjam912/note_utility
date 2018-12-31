import abc
from .errors import *


# The plan is that we will create everything needed to pass into the Note's constructor
# in the NoteUtil method and then just make the Note.
class Note(abc.ABC):
    """A `Note` is the text found in the notes file. It contains the actual notes.

    Parameters
    ----------
    content : str
        The content of the `Note` excluding `prefixes` and `Extensions`.
    nindex : int
        The `Note` index that corresponds to the position in the `NoteUtil.notes`.
    rcontent : str
        Raw content of the `Note`.
    prefix : str
        Any prefixes this `Note` had that were used to determine the type of `Category`.
    extensions: dict of {str : `Extension`}
        A dict of the `Extensions` this `Note` has with key: `Extension.name` and value: `Extension`.
    categories: list of `Category`
        A sorted list of all of the `Categories` this `Note` belongs to.
    tabs: int
        The number of tabs that indicates how nested this `Note` is (one per `Category`).
    fmt: function
        The function applied to a `Note` to give it its `str` value.
    """

    # Order of constructor args: content, hidden content, outside content, outside hidden content.
    def __init__(self, content, nindex, rcontent, prefix, extensions, categories, tabs, fmt):
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
    content : str
        The content of the `Line` excluding `prefixes` and `Extensions`.
    nindex : int
        The `Note` index that corresponds to the position in the `NoteUtil.notes`.
    lindex : int
        The `Line` index that corresponds to the position in the `NoteUtil.lines`.
    extensions : dict of {str : `Extension`}
        A dict of the `Extensions` that this `Line` has with key: `Extension.name` and value `Extension`.
    categories : list of `Category`
        A sorted list of all of the `Categories` this `Line` belongs to.
    """

    def __init__(self, content, nindex, lindex, rcontent, prefix, extensions, categories, tabs, fmt):
        super().__init__(content, nindex, rcontent, prefix, extensions, categories, tabs, fmt)
        self.lindex = lindex

    def __repr__(self):
        rstring = ""
        rstring += self._prefix
        rstring += self.content
        for extension in self.extensions:
            rstring += repr(extension)
        for category in self.categories[::-1]:
            rstring = category._prefix + rstring
        return rstring


class Pair(Note):
    """A single token of notes with a separator that splits a term and a definition.

    Attributes
    ----------
    content : str
        The content of the `Pair` excluding `prefixes` and `Extensions`.
    nindex : int
        The `Note` index that corresponds to the position in the `NoteUtil.notes`.
    pindex : int
        The `Pair` index that corresponds to the position in the `NoteUtil.pairs`.
    separator : str
        The string that separates the key and value (term and definition) of the `Note` token.
    term : str
        The first part of text that came before the `separator`.
    definition : str
        The second part of text that came after the `separator`.
    extensions : dict of {str : `Extension`}
        A dict of the `Extensions` that this `Pair` has with key: `Extension.name` and value `Extension`.
    categories : list of `Category`
        A sorted list of all of the `Categories` this `Pair` belongs to.
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
        rstring += self._prefix
        rstring += self.term
        for extension in self.extensions:
            if extension._before is True:
                rstring += repr(extension)
        rstring += self.separator + self.definition
        for extension in self.extensions:
            if not extension._before:
                rstring += repr(extension)

        for category in self.categories[::-1]:
            rstring = category._prefix + rstring
        return rstring
