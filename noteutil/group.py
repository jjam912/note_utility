import abc


class Group(abc.ABC):
    def __init__(self, name):
        self.name = name


class LineGroup(Group):
    def __init__(self, name, prefix):
        super().__init__(name)
        self.prefix = prefix
        self.lines = []


class PairGroup(Group):
    def __init__(self, name, prefix, separator):
        super().__init__(name)
        self.prefix = prefix
        self.separator = separator
        self.pairs = []


class CategoryGroup(Group):
    def __init__(self, name, prefix, *, categories: list = None):
        super().__init__(name)
        self.prefix = prefix
        self.categories = [] if categories is None else categories
        self.notes = []


class ExtensionGroup(abc.ABC, Group):
    def __init__(self, name, lbound: str, rbound: str, placeholder: str = " "):
        super().__init__(name)
        self.lbound = lbound
        self.rbound = rbound
        self.placeholder = placeholder
        self.notes = []


class LineExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, lbound: str, rbound: str, placeholder: str = " "):
        super().__init__(name, lbound, rbound, placeholder)


class PairExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, separator: str, lbound: str, rbound: str, placeholder: str = " "):
        super().__init__(name, lbound, rbound, placeholder)
        self.separator = separator


class ListExtensionGroup(abc.ABC, ExtensionGroup):
    def __init__(self, name: str, separators: list, lbound: str, rbound: str, placeholder: str = " "):
        super().__init__(name, lbound, rbound, placeholder)
        self.separators = separators


class BulletListExtensionGroup(ListExtensionGroup):
    def __init__(self, name: str, separators: list, bullets: list, lbound: str, rbound: str, placeholder: str = " "):
        super().__init__(name, separators, lbound, rbound, placeholder)
        self.bullets = bullets


class NumberListExtensionGroup(ListExtensionGroup):
    def __init__(self, name: str, separators: list, lbound: str, rbound: str, placeholder: str = " "):
        super().__init__(name, separators, lbound, rbound, placeholder)

