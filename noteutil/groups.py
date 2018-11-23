import abc


class Group(abc.ABC):
    def __init__(self, name: str):
        self.name = name


class LineGroup(Group):
    def __init__(self, name: str, prefix: str = None):
        super().__init__(name)
        self.prefix = prefix
        self.lines = []


class PairGroup(Group):
    def __init__(self, name: str, separator, prefix: str = None):
        super().__init__(name)
        self.prefix = prefix
        self.separator = separator
        self.pairs = []


class CategoryGroup(Group):
    def __init__(self, name: str, prefix: str):
        super().__init__(name)
        self.prefix = prefix


class GlobalCategoryGroup(CategoryGroup):
    def __init__(self, name: str, prefix: str):
        super().__init__(name, prefix)
        self.category = None


class PositionalCategoryGroup(CategoryGroup):
    def __init__(self, name: str, prefix: str):
        super().__init__(name, prefix)
        self.categories = []


class ExtensionGroup(Group):
    def __init__(self, name: str, lbound: str, rbound: str, placeholder: str = " "):
        super().__init__(name)
        self.lbound = lbound
        self.rbound = rbound
        self.placeholder = placeholder
        self.notes = []
        self.lines = []
        self.pairs = []


class LineExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, lbound: str, rbound: str, placeholder: str = " "):
        super().__init__(name, lbound, rbound, placeholder)


class PairExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, separator: str, lbound: str, rbound: str, placeholder: str = " "):
        super().__init__(name, lbound, rbound, placeholder)
        self.separator = separator


class ListExtensionGroup(ExtensionGroup):
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

