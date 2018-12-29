import abc
from .notes import Note
from .errors import *
from .groups import (ExtensionGroup, LineExtensionGroup, PairExtensionGroup,
                     ListExtensionGroup, NumberListExtensionGroup, BulletListExtensionGroup)


# TODO: Replace fmt with a function
class Extension(abc.ABC):
    def __init__(self, content: str, cindex: int, note: Note, ext_group: ExtensionGroup):
        self._rcontent = content
        self.content = content
        self.cindex = cindex
        self.note = note
        self.name = ext_group.name
        self.lbound = ext_group.lbound
        self.rbound = ext_group.rbound
        self.placeholder = ext_group.placeholder
        self.fmt = ext_group.fmt

    @abc.abstractmethod
    def __repr__(self):
        pass

    def __str__(self):
        return self.fmt(self)


class LineExtension(Extension):
    def __init__(self, content: str, cindex: int, note: Note, ext_group: LineExtensionGroup):
        super().__init__(content, cindex, note, ext_group)

    def __repr__(self):
        return f"{self.lbound}{self.content}{self.rbound}"


class PairExtension(Extension):
    def __init__(self, content: str, cindex: int, note: Note, ext_group: PairExtensionGroup):
        super().__init__(content, cindex, note, ext_group)
        self.separator = ext_group.separator

        tokens = tuple(content.split(self.separator))
        if len(tokens) != 2:
            raise SeparatorError(content)

        self.term, self.definition = tokens[0].strip(), tokens[1].strip()

    def __repr__(self):
        return f"{self.lbound}{self.term} {self.separator} {self.definition}{self.rbound}"


class ListExtension(Extension):
    def __init__(self, content: str, cindex: int, note: Note, ext_group: ListExtensionGroup):
        super().__init__(content, cindex, note, ext_group)
        self.separators = ext_group.separators
        self.elements = []

    def __repr__(self):
        rstring = ""
        rstring += self.lbound

        elements = self.separators[0].join(list(map(lambda x: x.content, self.elements)))
        for i in range(len(elements)):
            for j in range(1, self.elements[i].tabs + 1):
                elements[i] = self.separators[j] + elements[i]

        rstring += self.rbound
        return rstring


class ListElement:
    def __init__(self, content: str, tabs: int, list_ext: ListExtension):
        self.content = content
        self.tabs = tabs
        self.list_ext = list_ext
        # I might implement this
        # self.parents = []
        # self.children = []

    def __str__(self):
        return ("\t" * self.tabs) + self.content


class BulletListExtension(ListExtension):
    def __init__(self, content: str, cindex: int, note: Note, ext_group: BulletListExtensionGroup):
        super().__init__(content, cindex, note, ext_group)

    def __repr__(self):
        rstring = ""
        rstring += self.lbound

        elements = self.separators[0].join(list(map(lambda x: x.content, self.elements)))
        for i in range(len(elements)):
            for j in range(1, self.elements[i].tabs + 1):
                elements[i] = self.separators[j] + elements[i]

        rstring += self.rbound
        return rstring


class NumberListExtension(ListExtension):
    def __init__(self, content: str, cindex: int, note: Note, ext_group: NumberListExtensionGroup):
        super().__init__(content, cindex, note, ext_group)

    def __repr__(self):
        rstring = ""
        rstring += self.lbound

        elements = self.separators[0].join(list(map(lambda x: x.content, self.elements)))
        for i in range(len(elements)):
            for j in range(1, self.elements[i].tabs + 1):
                elements[i] = self.separators[j] + elements[i]

        rstring += self.rbound
        return rstring

