import abc
from .notes import Note
from .groups import CategoryGroup, GlobalCategoryGroup, PositionalCategoryGroup


class Category(abc.ABC):
    def __init__(self, cat_group: CategoryGroup):
        self.notes = []
        self.lines = []
        self.pairs = []

        self.name = cat_group.name
        self.prefix = cat_group.prefix

    def __contains__(self, note: Note):
        return note in self.notes


class GlobalCategory(Category):
    def __init__(self, cat_group: GlobalCategoryGroup):
        super().__init__(cat_group)


class PositionalCategory(Note, Category):
    def __init__(self, content: str, nindex: int, cat_group: PositionalCategoryGroup,
                 *, extensions: list = None, categories: list = None):
        super().__init__(content, nindex, extensions=extensions, categories=categories)
        super().__init__(cat_group)

    def __repr__(self):
        rstring = ""
        rstring += self.content

        for ext in self.extensions:
            rstring += repr(ext)
        rstring = self.prefix + rstring
        for cat in reversed(self.categories):
            if isinstance(cat, GlobalCategory):
                rstring = cat.prefix + rstring
        return rstring

    def format(self):
        return self.content

    # def append(self, note):
    #     i, j, k, n = 0, len(self.notes) // 2, len(self.notes), note.nindex
    #     while k - i > 1:
    #         mid = self.notes[j].nindex
    #         if n > mid:
    #             i = j
    #         else:
    #             k = j
    #         j = (i + k) // 2
    #     if n > self.notes[j].nindex:
    #         self.notes.insert(j, note)
    #     else:
    #         self.notes.insert(i, note)
    #
    # def insert(self, category):
    #     # if pack.nindex < self.nindex:
    #     #     raise Something
    #
    #     i, j, k, n = 0, len(self.categories) // 2, len(self.categories), category.nindex
    #     while k - i > 1:
    #         mid = self.categories[j].nindex
    #         if n > mid:
    #             i = j
    #         else:
    #             k = j
    #         j = (i + k) // 2
    #     if n > self.notes[j].nindex:
    #         self.categories.insert(j, category)
    #     else:
    #         self.categories.insert(i, category)

