import abc
from .notes import Note
from .errors import *


# Just like Notes, the plan is that we will create everything needed to pass into the Extension's constructor
# in the NoteUtil method and then just make the Extension, which will be added to the Note.
class Extension(abc.ABC):
    # Order of constructor args: content, hidden content, outside content, outside hidden content.
    def __init__(self, content: str, name: str, eindex: int, rcontent: str, cindex: int,
                 note: Note, placeholder: str, before: bool, lbound: str, rbound: str, fmt):
        """
        Parameters
        ----------
        content : :class:`str`
            The content of the extension excluding bounds.
        name : :class:`str`
            The name assigned to this extension, used as a key in :attr:`NoteUtil.extension_dict`.
        eindex : :class:`int`
            The `Extension` index that corresponds to the position in the list
            found with `NoteUtil.extension_dict[Extension.name]`
        rcontent : :class:`str`
            Raw content of the `Extension`.
        cindex : :class:`int`
            The `content` index that corresponds to the position of this extension in its `Note`.
        note : :class:`Note`
            The `Note` that this extension was found in.
        placeholder : :class:`str`
            The string that replaces the raw content of the extension in its `Note`.
        before : :class:`bool`
            Whether this extension comes before (T) or after (F) the separator in a `Note`.
            If there is no separator (`Note` is a `Line`), then this is `None`.
        lbound : :class:`str`
            The string that determines when this extension begins. The "left bound."
        rbound : :class:`str`
            The string that determines when this extension ends. The "right bound."
        fmt : function
            The function applied to an `Extension` to give it its `str` value.
            Must take an `Extension` as a parameter.
        """

        self.content = content
        self.name = name
        self.eindex = eindex
        self._rcontent = rcontent
        self._cindex = cindex
        self.note = note
        self._placeholder = placeholder
        self._before = before
        self._lbound = lbound
        self._rbound = rbound
        self._format = fmt

    @abc.abstractmethod
    def __repr__(self):
        pass

    def __str__(self):
        return self._format(self)


class LineExtension(Extension):
    """
    Attributes
    ----------
    content: :class:`str`
        The content of the extension excluding bounds.
    name: :class:`str`
        The name assigned to this extension, used as a key in :attr:`NoteUtil.extension_dict`.
    eindex: :class:`int`
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    note: :class:`Note`
        The `Note` that this extension was found in.
    """
    def __init__(self, content: str, name: str, eindex: int, rcontent: str, cindex: int,
                 note: Note, placeholder: str, before: bool, lbound: str, rbound: str, fmt):
        super().__init__(content, name, eindex, rcontent, cindex, note, placeholder, before, lbound, rbound, fmt)

    def __repr__(self):
        return f"{self._lbound}{self.content}{self._rbound}"


class PairExtension(Extension):
    """
    Attributes
    ----------
    content: :class:`str`
        The content of the extension excluding bounds.
    name: :class:`str`
        The name assigned to this extension, used as a key in :attr:`NoteUtil.extension_dict`.
    eindex: :class:`int`
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    separator: :class:`str`
        The string that separates the key and value (term and definition) of this extension's content.
    term: :class:`str`
        The first part that came before the separator.
    definition: :class:`str`
        The second part that came after the separator.
    note: :class:`Note`
        The `Note` that this extension was found in.
    """

    def __init__(self, content: str, name: str, eindex: int, separator: str, rcontent: str, cindex: int,
                 note: Note, placeholder: str, before: bool, lbound: str, rbound: str, fmt):
        super().__init__(content, name, eindex, rcontent, cindex, note, placeholder, before, lbound, rbound, fmt)
        self.separator = separator
        self._separate()

    def _separate(self):
        tokens = tuple(self.content.split(self.separator))
        if len(tokens) != 2:
            raise SeparatorError(self.content)

        self.term, self.definition = tokens[0].strip(), tokens[1].strip()

    def __repr__(self):
        return f"{self._lbound}{self.term} {self.separator} {self.definition}{self._rbound}"


class ListExtension(Extension):
    """
    Attributes
    ----------
    content: :class:`str`
        The content of the extension excluding bounds.
    name: :class:`str`
        The name assigned to this extension, used as a key in :attr:`NoteUtil.extension_dict`.
    eindex: :class:`int`
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    separators: List[:class:`str`]
        The first string separates each `ListElement`.
        Any later strings indicate the prefix needed to nest the element a certain number of tabs.

        .. warning::

            There must be at least one separator in `separators`.

    elements : List[:class:`ListElement`]
        All elements created from the tokens between the separators.
    note: :class:`Note`
        The `Note` that this extension was found in.
    """

    def __init__(self, content: str, name: str, eindex: int, separators: list, rcontent: str, cindex: int,
                 note: Note, placeholder: str, before: bool, lbound: str, rbound: str, fmt):
        super().__init__(content, name, eindex, rcontent, cindex, note, placeholder, before, lbound, rbound, fmt)
        assert len(separators) >= 1, "There must be at least one separator in separators."
        self.separators = separators
        self._separate()

    def _separate(self):
        self.elements = []

    def __repr__(self):
        rstring = ""
        rstring += self._lbound

        elements = self.separators[0].join(list(map(lambda x: x.content, self.elements)))
        for i in range(len(elements)):
            for j in range(1, self.elements[i].tabs + 1):
                elements[i] = self.separators[j] + elements[i]

        rstring += self._rbound
        return rstring


class ListElement:
    """
    Attributes
    ----------
    content: :class:`str`
        The content of the element, including any prefixes.
    ucontent: :class:`str`
        Unmodified content, what was the content before any additional formatting.
    list_ext: :class:`ListExtension`
        The `ListExtension` that this element belongs to.
    """
    def __init__(self, ucontent: str, content: str, list_ext: ListExtension, tabs: int):
        self.ucontent = ucontent
        self.content = content
        self.list_ext = list_ext
        self._tabs = tabs
        # I might implement this
        # self.parents = []
        # self.siblings = []
        # self.children = []

    def __str__(self):
        return ("\t" * self._tabs) + self.content


class BulletListExtension(ListExtension):
    """
    Attributes
    ----------
    content: :class:`str`
        The content of the extension excluding bounds.
    name: :class:`str`
        The name assigned to this extension, used as a key in :attr:`NoteUtil.extension_dict`.
    eindex: :class:`int`
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    separators: List[:class:`str`]
        The first string separates each `ListElement`.
        Any later strings indicate the prefix needed to nest the element a certain number of tabs.

        .. warning::

            There must be at least one separator in `separators`.

    bullets: List[:class:`str`]
        The bullets that will be used to prefix each element.
        The first string will be the bullet of the ListElement with no tabs, second with one tab, etc.

        .. note::

            If there are fewer bullets than separators, the bullets will repeat starting from the beginning.

        .. warning::
            There must be at least one bullet in `bullets`.

    spaces: :class:`int`
        The number of spaces between the bullet and the content of the `ListElement`.
    elements : List[:class:`ListElement`]
        All elements created from the tokens between the separators.
    note: :class:`Note`
        The `Note` that this extension was found in.
    """

    def __init__(self, content: str, name: str, eindex: int, separators: list, bullets: list, spaces: int,
                 rcontent: str, cindex: int, note: Note, placeholder: str, before: bool, lbound: str, rbound: str, fmt):
        super().__init__(content, name, eindex, separators, rcontent, cindex,
                         note, placeholder, before, lbound, rbound, fmt)
        assert len(bullets) >= 1, "There must be at least one bullet in bullets."
        self.bullets = bullets
        self.spaces = spaces
        self._separate()

    def _separate(self):
        self.elements = []

    def __repr__(self):
        rstring = ""
        rstring += self._lbound

        elements = self.separators[0].join(list(map(lambda x: x.content, self.elements)))
        for i in range(len(elements)):
            for j in range(1, self.elements[i].tabs + 1):
                elements[i] = self.separators[j] + elements[i]

        rstring += self._rbound
        return rstring


class NumberListExtension(ListExtension):
    """
    Attributes
    ----------
    content: :class:`str`
        The content of the extension excluding bounds.
    name: :class:`str`
        The name assigned to this extension, used as a key in :attr:`NoteUtil.extension_dict`.
    eindex: :class:`int`
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    separators: List[:class:`str`]
        The first string separates each `ListElement`.
        Any later strings indicate the prefix needed to nest the element a certain number of tabs.

        .. warning::

            There must be at least one separator in `separators`.

    continuous: :class:`bool`
        Whether to continue the number sequence if the next ListElement has a different number of tabs.
    elements : List[:class:`ListElement`]
        All elements created from the tokens between the separators.
    note: :class:`Note`
        The `Note` that this extension was found in.
    """

    def __init__(self, content: str, name: str, eindex: int, separators: list, continuous: bool,
                 rcontent: str, cindex: int, note: Note, placeholder: str, before: bool, lbound: str, rbound: str, fmt):
        super().__init__(content, name, eindex, separators, rcontent, cindex,
                         note, placeholder, before, lbound, rbound, fmt)
        self.continuous = continuous
        self._separate()

    def _separate(self):
        self.elements = []

    def __repr__(self):
        rstring = ""
        rstring += self._lbound

        elements = self.separators[0].join(list(map(lambda x: x.content, self.elements)))
        for i in range(len(elements)):
            for j in range(1, self.elements[i].tabs + 1):
                elements[i] = self.separators[j] + elements[i]

        rstring += self._rbound
        return rstring

