import abc
from .notes import Note


# The plan is to create GlobalCategories before creating notes, and then creating Positional Categories along the way
class Category(abc.ABC):
    """A `Category` is a tag that belongs to a `Note`.

    An example of a `Category` could be Chapters, such as Chapter 1, 2, 3, etc.

    Parameters
    ----------
    name : str
        The name assigned to this `Category`, used as a key in `NoteUtil.categories`.
    prefix : str
        The prefix used to determine that a `Note` would be of this `Category`.
    fmt : function
        The function applied to a `Category` to give it its `str` value.
    """

    # Order of constructor args: content, hidden content, outside content, outside hidden content.
    def __init__(self, name, prefix, fmt):
        self.notes = []
        self.lines = []
        self.pairs = []

        self.name = name
        self._prefix = prefix
        self._format = fmt

    def __contains__(self, note: Note):
        return note in self.notes


class GlobalCategory(Category):
    """A `GlobalCategory` is a `Category` that is not affected by the position of a `Note`.

    An example of a `GlobalCategory` would be People, such as different important people throughout history.
    There could be important people several time periods, so it's illogical to separate them and group them together.

    Attributes
    ----------
    name : str
        The name assigned to this `Category`, used as a key in `NoteUtil.categories`.
    removed : bool
        Whether `Notes` of this `Category` were removed from the `NoteUtil.notes`.
    notes : list of `Note`
        A sorted list of all of the `Notes` that belong to this `Category`.
    lines : list of `Line`
        A sorted list of all of the `Lines` that belong to this `Category`.
    pairs : list of `Pair`
        A sorted list of all of the `Pairs` that belong to this `Category`.
    """

    def __init__(self, name, removed, prefix, fmt):
        super().__init__(name, prefix, fmt)
        self.removed = removed


class PositionalCategory(Note, Category):
    def __init__(self, content, nindex, pindex, name, rcontent, prefix, extensions, categories, tabs, fmt):
        """A `PositionalCategory` is a `Category` whose position is important to the classification of its `Notes`.

        An example would be if your notes are in chronological order and
            all notes that follow a `Category` belong to that `Category`.
        This class acts similar to a `Line`.

        Attributes
        ----------
        content : str
            The content of the `Category` excluding `prefixes` and `Extensions`.
        nindex : int
            The `Note` index that corresponds to the position in the `NoteUtil.notes`.
        pindex : int
            The `Positional` index that corresponds to the position in the `NoteUtil.positionals`.
        name : str
            The name assigned to this `Category`, used as a key in `NoteUtil.categories`.
        removed : bool
            Whether `Notes` of this `Category` were removed from the `NoteUtil.notes`.
        notes : list of `Note`
            A sorted list of all of the `Notes` that belong to this `Category`.
        lines : list of `Line`
            A sorted list of all of the `Lines` that belong to this `Category`.
        pairs : list of `Pair`
            A sorted list of all of the `Pairs` that belong to this `Category`.
        extensions : dict of {str : `Extension`}
            A dict of the `Extensions` that this `Line` has with key: `Extension.name` and value `Extension`.
        categories : list of `Category`
            A sorted list of all of the `Categories` this `Line` belongs to.
        """

        super().__init__(content, nindex, rcontent, prefix, extensions, categories, tabs, fmt)
        super().__init__(name, prefix, fmt)     # The format of the `Note` will be overridden by the `Category` one.
        self.pindex = pindex

    def __repr__(self):
        rstring = ""
        rstring += self._prefix
        rstring += self.content
        for extension in self.extensions:
            rstring += repr(extension)
        for category in self.categories[::-1]:
            rstring = category._prefix + rstring
        return rstring
