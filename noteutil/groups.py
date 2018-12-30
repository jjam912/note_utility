from .errors import *
from .notes import Line, Pair
from .extensions import LineExtension, PairExtension, ListExtension, BulletListExtension, NumberListExtension
import itertools


# TODO: Implement actual functions
# Groups are meant to help NoteUtil initialize its Categories, Notes, and Extensions.
# They should not be used after NoteUtil has been fully initialized.
class Group:
    def __new__(cls, *args, **kwargs):
        if cls is Group:
            raise AbstractGroupError(cls)

    def __init__(self, name: str, *, fmt=lambda n: None):
        self._name = name
        self.fmt = fmt

    @property
    def name(self):
        return self._name


#######################
class NoteGroup(Group):
    def __new__(cls, *args, **kwargs):
        if cls is NoteGroup:
            raise AbstractGroupError(cls)

    def __init__(self, name: str, prefix: str, *, fmt=lambda n: None):
        super().__init__(name, fmt=fmt)
        self._prefix = prefix

    @property
    def prefix(self):
        return self._prefix


def line_fmt(line: Line):
    return line.content


class LineGroup(NoteGroup):
    def __init__(self, name: str, prefix: str, *, fmt=line_fmt):
        super().__init__(name, prefix, fmt=fmt)


def pair_fmt(pair: Pair):
    return "{0} {1} {2}".format(pair.term, pair.separator, pair.definition)


class PairGroup(NoteGroup):
    def __init__(self, name: str, prefix: str, separator: str, *, fmt=pair_fmt):
        super().__init__(name, prefix, fmt=fmt)
        self.separator = separator


###############################
class CategoryGroup(NoteGroup):
    def __new__(cls, *args, **kwargs):
        if cls is CategoryGroup:
            raise AbstractGroupError(cls)

    def __init__(self, name: str, prefix: str):
        super().__init__(name, prefix)


class GlobalCategoryGroup(CategoryGroup):
    def __init__(self, name: str, prefix: str):
        super().__init__(name, prefix)


class PositionalCategoryGroup(CategoryGroup):
    def __init__(self, name: str, prefix: str):
        super().__init__(name, prefix)


############################
class ExtensionGroup(Group):
    def __new__(cls, *args, **kwargs):
        if cls is ExtensionGroup:
            raise AbstractGroupError(cls)

    def __init__(self, name: str, lbound: str, rbound: str, *, fmt=lambda e: None, placeholder: str = ""):
        super().__init__(name, fmt=fmt)
        self._lbound = lbound
        self._rbound = rbound
        self._placeholder = placeholder

    @property
    def lbound(self):
        return self._lbound

    @property
    def rbound(self):
        return self._rbound

    @property
    def placeholder(self):
        return self._placeholder


def line_ext_fmt(line_ext):
    return line_ext.content


class LineExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, lbound: str, rbound: str, *, fmt=line_ext_fmt, placeholder: str = ""):
        super().__init__(name, lbound, rbound, fmt=fmt, placeholder=placeholder)


def pair_ext_fmt(pair_ext):
    return "{0} {1} {2}".format(pair_ext.term, pair_ext.separator, pair_ext.definition)


class PairExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, separator: str, lbound: str, rbound: str, *, fmt=pair_ext_fmt, placeholder: str = ""):
        super().__init__(name, lbound, rbound, fmt=fmt, placeholder=placeholder)
        self._separator = separator

    @property
    def separator(self):
        return self._separator


def list_ext_fmt(list_ext):
    fmt = ""


class ListExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, separators: list, lbound: str, rbound: str,
                 *, fmt=list_ext_fmt, placeholder: str = ""):
        super().__init__(name, lbound, rbound, fmt=fmt, placeholder=placeholder)
        self._separators = separators

    @property
    def separators(self):
        return self._separators


def bullet_list_ext_fmt(bullet_list_ext):
    fmt = ""


class BulletListExtensionGroup(ListExtensionGroup):
    def __init__(self, name: str, separators: list, bullets: list, lbound: str, rbound: str,
                 *, fmt=bullet_list_ext_fmt, placeholder: str = ""):
        super().__init__(name, separators, lbound, rbound, fmt=fmt, placeholder=placeholder)
        self._bullets = bullets

    @property
    def bullets(self):
        return self._bullets


def number_list_ext_fmt(number_list_ext):
    fmt = ""


class NumberListExtensionGroup(ListExtensionGroup):
    def __init__(self, name: str, separators: list, lbound: str, rbound: str,
                 *, fmt=number_list_ext_fmt, placeholder: str = ""):
        super().__init__(name, separators, lbound, rbound, fmt=fmt, placeholder=placeholder)

