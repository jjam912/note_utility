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
            raise SeparatorError(f"There was either zero or more than one separator in the content: {content}")

        self.term, self.definition = tokens[0].strip(), tokens[1].strip()

    def __repr__(self):
        return f"{self.lbound}{self.term} {self.separator} {self.definition}{self.rbound}"


class ListExtension(Extension, abc.ABC):
    def __init__(self, content: str, cindex: int, note: Note, ext_group: ListExtensionGroup):
        super().__init__(content, cindex, note, ext_group)
        self.separators = ext_group.separators
        self.elements = []


class ListElement:
    def __init__(self, content: str, list_ext: ListExtension, *, parents: list = None, children: list = None):
        self.content = content
        self.list_ext = list_ext
        self.parents = parents
        self.children = children


class BulletListExtension(ListExtension):
    def __init__(self, content: str, cindex: int, note: Note, ext_group: BulletListExtensionGroup):
        super().__init__(content, cindex, note, ext_group)

    def __repr__(self):
        pass


class NumberListExtension(ListExtension):
    def __init__(self, content: str, cindex: int, note: Note, ext_group: NumberListExtensionGroup):
        super().__init__(content, cindex, note, ext_group)

    def __repr__(self):
        pass

