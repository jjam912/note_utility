import abc
from .notes import Note
from .errors import *


# Just like Notes, the plan is that we will create everything needed to pass into the Extension's constructor
# in the NoteUtil method and then just make the Extension, which will be added to the Note.
class Extension(abc.ABC):
    # Order of constructor args: content, hidden content, outside content, outside hidden content.
    def __init__(self, content, name, eindex, rcontent, cindex, note, placeholder, before, lbound, rbound, fmt):
        """
        Parameters
        ----------
        content : str
            The content of the `Extension` excluding bounds.
        name : str
            The name assigned to this `Extension`, used as a key in `NoteUtil.extension_dict`.
        eindex : int
            The `Extension` index that corresponds to the position in the list
            found with `NoteUtil.extension_dict[Extension.name]`
        rcontent : str
            Raw content of this `Extension`.
        cindex : int
            The `content` index that corresponds to the position of this `Extension` in its `note`.
        note : Note
            The `Note` that this `Extension` was found in.
        placeholder : str
            The string that replaces the `rcontent` of the `Extension` in its `Note`.
        before : bool
            Whether this `Extension` comes before (T) or after (F) the `separator` in a `Note`.
            If there is no `separator` (`Note` is a `Line`), then this is `None`.
        lbound : str
            The string that determines when this `Extension` begins. The "left bound."
        rbound : str
            The string that determines when this `Extension` ends. The "right bound."
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
    content: str
        The content of the `Extension` excluding bounds.
    name: str
        The name assigned to this `Extension`, used as a key in `NoteUtil.extension_dict`.
    eindex: int
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    note: `Note`
        The `Note` that this `Extension` was found in.
    """

    def __init__(self, content, name, eindex, rcontent, cindex, note, placeholder, before, lbound, rbound, fmt):
        super().__init__(content, name, eindex, rcontent, cindex, note, placeholder, before, lbound, rbound, fmt)

    def __repr__(self):
        return f"{self._lbound}{self.content}{self._rbound}"


class PairExtension(Extension):
    """
    Attributes
    ----------
    content: str
        The content of the `Extension` excluding bounds.
    name: str
        The name assigned to this `Extension`, used as a key in `NoteUtil.extension_dict`.
    eindex: int
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    separator: str
        The string that separates the key and value (term and definition) of this `Extension's` content.
    term: str
        The first part that came before the `separator`.
    definition: str
        The second part that came after the `separator`.
    note: `Note`
        The `Note` that this `Extension` was found in.
    """

    def __init__(self, content, name, eindex, separator, rcontent, cindex,
                 note, placeholder, before, lbound, rbound, fmt):
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
    content: str
        The content of the `Extension` excluding bounds.
    name: str
        The name assigned to this `Extension`, used as a key in `NoteUtil.extension_dict`.
    eindex: int
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    separators: list of str
        # TODO: This should be in Groups
        The first string separates each `ListElement`.
        Any later strings indicate the prefix needed to nest the `ListElement` a certain number of tabs.
        There must be at least one `separator` in `separators`.
    elements : list of `ListElement`
        All elements created from the tokens between the `separators`.
    note: `Note`
        The `Note` that this `Extension` was found in.
    """

    def __init__(self, content, name, eindex, separators, rcontent, cindex,
                 note, placeholder, before, lbound, rbound, fmt):
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
    rcontent: str
        Raw content, what the content was before any additional formatting.
    content: str
        The content of the `ListElement`, including any prefixes or other modifications.
    list_ext: `ListExtension`
        The `ListExtension` that this `ListElement` belongs to.
    """
    def __init__(self, rcontent, content, list_ext, tabs: int):
        self.rcontent = rcontent
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
    content: str
        The content of the `Extension` excluding bounds.
    name: str
        The name assigned to this `Extension`, used as a key in `NoteUtil.extension_dict`.
    eindex: int
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    separators: list of str
        The first string separates each `ListElement`.
        Any later strings indicate the prefix needed to nest the `ListElement` a certain number of tabs.
        There must be at least one `separator` in `separators`.

    bullets: list of str
        The bullets that will be used to prefix each `ListElement`.
        The first string will be the bullet of the `ListElement` with no tabs, second with one tab, etc.
        If there are fewer `bullets` than `separators`, the `bullets` will repeat starting from the beginning.
        There must be at least one `bullet` in `bullets`.

    spaces: int
        The number of spaces between the `bullet` and the `content` of the `ListElement`.
    elements : list of `ListElement`
        All elements created from the tokens between the `separators`.
    note: `Note`
        The `Note` that this `Extension` was found in.
    """

    def __init__(self, content, name, eindex, separators, bullets, spaces,
                 rcontent, cindex, note, placeholder, before, lbound, rbound, fmt):
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
    content: str
        The content of the `Extension` excluding bounds.
    name: str
        The name assigned to this `Extension`, used as a key in `NoteUtil.extension_dict`.
    eindex: int
        The `Extension` index that corresponds to the position in the list
        found with `NoteUtil.extension_dict[Extension.name]`
    separators: list of str
        The first string separates each `ListElement`.
        Any later strings indicate the prefix needed to nest the `ListElement` a certain number of tabs.
        There must be at least one `separator` in `separators`.

    continuous: bool
        Whether to continue the number sequence if the next `ListElement` has a different number of tabs.
    elements : list of `ListElement`
        All `ListElements` created from the tokens between the `separators`.
    note: `Note`
        The `Note` that this `Extension` was found in.
    """

    def __init__(self, content, name, eindex, separators, continuous,
                 rcontent, cindex, note, placeholder, before, lbound, rbound, fmt):
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

