from .errors import *


# TODO: Replace fmt with a lambda function
class Group:
    def __new__(cls, *args, **kwargs):
        if cls is Group:
            raise AbstractGroupError("Group is an abstract class that cannot be implemented.")

    def __init__(self, name: str, *, fmt: function = lambda n: None):
        self._name = name
        self.fmt = fmt

    @property
    def name(self):
        return self._name


class NoteGroup(Group):
    def __new__(cls, *args, **kwargs):
        if cls is NoteGroup:
            raise AbstractGroupError("NoteGroup is an abstract class that cannot be implemented.")

    def __init__(self, name: str, prefix: str, *, fmt: function = lambda n: None):
        super().__init__(name, fmt=fmt)
        self._prefix = prefix

    @property
    def prefix(self):
        return self._prefix


class LineGroup(NoteGroup):
    def __init__(self, name: str, prefix: str, *, fmt: function = lambda n: n.content):
        super().__init__(name, prefix, fmt=fmt)
        self.lines = []


class PairGroup(NoteGroup):
    def __init__(self, name: str, prefix: str, separator: str, *,
                 fmt: function = lambda n: f"{n.term} {n.separator} {n.definition}"):
        super().__init__(name, prefix, fmt=fmt)
        self.separator = separator
        self.pairs = []


class CategoryGroup(NoteGroup):
    def __new__(cls, *args, **kwargs):
        if cls is CategoryGroup:
            raise AbstractGroupError("CategoryGroup is an abstract class that cannot be implemented.")

    def __init__(self, name: str, prefix: str):
        super().__init__(name, prefix)


class GlobalCategoryGroup(CategoryGroup):
    def __init__(self, name: str, prefix: str):
        super().__init__(name, prefix)
        self.category = None


class PositionalCategoryGroup(CategoryGroup):
    def __init__(self, name: str, prefix: str):
        super().__init__(name, prefix)
        self.categories = []


class ExtensionGroup(Group):
    def __new__(cls, *args, **kwargs):
        if cls is ExtensionGroup:
            raise AbstractGroupError("ExtensionGroup is an abstract class that cannot be implemented.")

    def __init__(self, name: str, lbound: str, rbound: str, *, fmt: function = lambda e: None, placeholder: str = ""):
        super().__init__(name, fmt=fmt)
        self._lbound = lbound
        self._rbound = rbound
        self._placeholder = placeholder
        self.notes = []
        self.lines = []
        self.pairs = []

    @property
    def lbound(self):
        return self._lbound

    @property
    def rbound(self):
        return self._rbound

    @property
    def placeholder(self):
        return self._placeholder


class LineExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, lbound: str, rbound: str, *,
                 fmt: function = lambda e: e.content, placeholder: str = ""):
        super().__init__(name, lbound, rbound, fmt=fmt, placeholder=placeholder)


class PairExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, separator: str, lbound: str, rbound: str, *,
                 fmt: function = lambda e: f"{e.term} {e.separator} {e.definition}", placeholder: str = ""):
        super().__init__(name, lbound, rbound, fmt=fmt, placeholder=placeholder)
        self._separator = separator

    @property
    def separator(self):
        return self._separator


class ListExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, separators: list, lbound: str, rbound: str,
                 *, fmt: function = lambda e: "\n".join(e.elements), placeholder: str = ""):
        super().__init__(name, lbound, rbound, fmt=fmt, placeholder=placeholder)
        self._separators = separators

    @property
    def separators(self):
        return self._separators


class BulletListExtensionGroup(ListExtensionGroup):
    def __init__(self, name: str, separators: list, bullets: list, lbound: str, rbound: str, placeholder: str = ""):
        super().__init__(name, separators, lbound, rbound, placeholder)
        self._bullets = bullets

    @property
    def bullets(self):
        return self._bullets


class NumberListExtensionGroup(ListExtensionGroup):
    def __init__(self, name: str, separators: list, lbound: str, rbound: str, placeholder: str = ""):
        super().__init__(name, separators, lbound, rbound, placeholder)

