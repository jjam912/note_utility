from .errors import *
from .notes import Line, Pair
from .categories import PositionalCategory, GlobalCategory


class Group:
    """Groups are meant to help `NoteUtil` initialize its Categories, Notes, and Extensions.

    They should not be used after `NoteUtil` has been initialized.
    Think of these as the configuration classes for `NoteUtil`.

    Parameters
    ----------
    fmt : function
        The function applied to a `Note`, `Category`, or `Extension` to give it its `str` value.
        Must take the appropriate ``class`` as the **only** parameter.
    """

    def __new__(cls, *args, **kwargs):
        if cls is Group:
            raise AbstractGroupError(cls)

    def __init__(self, fmt):
        self.format = fmt


#######################
class NoteGroup(Group):
    """Base class for `Groups` relating to the `notes` module.

    Notes represent the text found in the notes file, and are basically your notes.
    They can have `Extensions`, which are additional information, and `Categories`, which are tags that it belongs to.

    Parameters
    ----------
    fmt: function
        The function applied to a `Note` to give it its `str` value.
        Must take a `Note` as the **only** parameter.
    """

    def __new__(cls, *args, **kwargs):
        if cls is NoteGroup:
            raise AbstractGroupError(cls)

    def __init__(self, fmt):
        super().__init__(fmt)


def line_fmt(line: Line):
    return line.content


class LineGroup(NoteGroup):
    """A `Group` for `Lines`.

    Lines are the most basic form of notes, simply a line of text.
    There should only be one of these because all `Lines` are all the same.

    Parameters
    ----------
    fmt: function
        The function applied to a `Line` to give it its `str` value.
        Must take a `Line` as the **only** parameter.

    Examples
    --------
    There should only be one `LineGroup`, but you can edit the `format`::

        # Default format
        def line_fmt(line: Line):
            return line.content
        line_group = LineGroup()

        # New format
        def my_fmt(line: Line):
            return "{0} : {1}".format(line.nindex, line.content)
        line_group = LineGroup(my_fmt)

    """

    def __init__(self, fmt=line_fmt):
        super().__init__(fmt)


def pair_fmt(pair: Pair):
    return "{0} {1} {2}".format(pair.term, pair.separator, pair.definition)


class PairGroup(NoteGroup):
    """A `Group` for `Pairs`.

    Pairs are notes with a `term` and a `definition`, separated by a `separator`.
    A `Note` will automatically become a `Pair` if its `separator` is in the `rcontent` of the `Note`.
    Thus, the creation of a `Pair` has higher priority than a `Line`.
    There can be multiple `PairGroups` as long as the separators are different.
    The priority of `PairGroups` depends on the order it is passed to `NoteUtil` as parameters.

    Parameters
    ----------
    separator : str
        The string that separates the term and definition of the `Pair`.
    fmt: function
        The function applied to a `Pair` to give it its `str` value.
        Must take a `Pair` as the **only** parameter.

    Examples
    --------
    There can be many `PairGroups`, each with its own `format`::

        # Default format
        def pair_fmt(pair: Pair):
            return "{0} {1} {2}".format(pair.term, pair.separator, pair.definition)
        pair_group1 = PairGroup(":")

        # New format
        def my_fmt(pair: Pair):
            return "The definition of {0} is {1}".format(pair.term, pair.definition)

        pair_group2 = PairGroup("-", my_fmt)

    In this case, if the list of `PairGroups` were in the order: [`pair_group1`, `pair_group2`],
        If a `Note` has a `rcontent` of for example: "John Cabot - In 1497 : This person was an Italian sea captain."
            The order in which the `separators` appear is insignificant; `pair_group1` was passed as the first arg,
            so the `Pair`'s `term` will be "John Cabot - In 1497" and
            its `definition` will be "This person was an Italian sea captain."

    """

    def __init__(self, separator, fmt=pair_fmt):
        super().__init__(fmt)
        self.separator = separator


############################
class ExtensionGroup(Group):
    """Base class for `Groups` relating to the `extensions` module.

    An extension is additional information given to a `Note` that may related, but not necessary.
    They are surrounded by bounds, which separate the `Extension` from the `Note`.
    They may have their own `separators` inside of their bounds, but they must be different from the `Note separators`.

    Parameters
    ----------
    name : str
        The name assigned to this `Extension`, used as a key in `NoteUtil.extensions`.
    lbound : str
        The string that determines when this `Extension` begins. The "left bound."
    rbound : str
        The string that determines when this `Extension` ends. The "right bound."
    fmt : function
        The function applied to an `Extension` to give it its `str` value.
    placeholder : str
        The string that replaces the `rcontent` of the `Extension` in its `Note`.
    """

    def __new__(cls, *args, **kwargs):
        if cls is ExtensionGroup:
            raise AbstractGroupError(cls)

    def __init__(self, name: str, lbound: str, rbound: str, *, fmt, placeholder: str = ""):
        super().__init__(fmt)
        self.name = name
        self._lbound = lbound
        self._rbound = rbound
        self._placeholder = placeholder


def line_ext_fmt(line_ext):
    return line_ext.content


class LineExtensionGroup(ExtensionGroup):
    """A `Group` for `LineExtensions`

    These, like `Lines` are just a line of text.

    Parameters
    ----------
    name : str
        The name assigned to this `Extension`, used as a key in `NoteUtil.extensions`.
    lbound : str
        The string that determines when this `Extension` begins. The "left bound."
    rbound : str
        The string that determines when this `Extension` ends. The "right bound."
    fmt : function
        The function applied to an `Extension` to give it its `str` value.
    placeholder : str
        The string that replaces the `rcontent` of the `Extension` in its `Note`.

    Examples
    --------
    If you want to make an `Extension` that is bounded by curly brackets {}::
        ext1 = LineExtensionGroup("Additional Info", "{", "}", placeholder="{}")
    If you want to add an `Extension` to your `Note`, make sure the `Extension` is bounded correctly::
        "Hi, I am example 1."   # Without anything
        "Hi, I am example 1. {But with an extension}"   # Content of Note before processing Extensions
        "Hi, I am example 1. {}"    # Content of Note after processing Extension
    """

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
    for e in list_ext.elements:
        fmt += e.content + "\n"
    return fmt


class ListExtensionGroup(ExtensionGroup):
    def __init__(self, name: str, separators: list, lbound: str, rbound: str,
                 *, fmt=list_ext_fmt, placeholder: str = ""):
        super().__init__(name, lbound, rbound, fmt=fmt, placeholder=placeholder)
        self.separators = separators


def bullet_list_ext_fmt(bullet_list_ext):
    fmt = ""
    for e in bullet_list_ext.elements:
        fmt += e.mcontent + "\n"
    return fmt


class BulletListExtensionGroup(ListExtensionGroup):
    def __init__(self, name: str, separators: list, bullets: list, lbound: str, rbound: str,
                 *, fmt=bullet_list_ext_fmt, placeholder: str = ""):
        super().__init__(name, separators, lbound, rbound, fmt=fmt, placeholder=placeholder)
        self.bullets = bullets


def number_list_ext_fmt(number_list_ext):
    fmt = ""
    for e in number_list_ext:
        fmt += e.mcontent + "\n"
    return fmt


class NumberListExtensionGroup(ListExtensionGroup):
    def __init__(self, name: str, separators: list, lbound: str, rbound: str,
                 *, fmt=number_list_ext_fmt, placeholder: str = ""):
        super().__init__(name, separators, lbound, rbound, fmt=fmt, placeholder=placeholder)


###############################
class CategoryGroup(NoteGroup):
    """Base class for `Groups` relating to the `categories` module.

     All `Categories` must have a `prefix` that will be used to identify if a `Note` belongs to that `Category`.
     The last prefix in `prefixes` will be used as the `prefix` of the `Category`.

     If you want to nest `Categories` (Category 2 in Category 1), Category 2 must start with Category 1`s prefix.
     There can be multiple `CategoryGroups` as long as the prefixes are different.
     The priority of `Categories` depends on the order it is passed to `NoteUtil` as parameters.

     Parameters
     ----------
     name : str
         The name that will be assigned to the `Category`, used as a key in `NoteUtil.categories`.
     prefixes : list of str
        The prefixes used to determine that a `Note` will belong to what `Categories`.
     fmt: function
         The function applied to a `Category` to give it its `str` value.
         Must take a `Category` as the **only** parameter.
     """

    def __new__(cls, *args, **kwargs):
        if cls is CategoryGroup:
            raise AbstractGroupError(cls)

    def __init__(self, name, prefixes, fmt):
        super().__init__(fmt)
        self.name = name
        self.prefixes = prefixes


def pos_cat_fmt(category: PositionalCategory):
    fmt = "{0} || {1}\n".format(category.name, category.content)
    for note in category.notes:
        tabs = (category.tabs().count("\t") - note.tabs().count("\t")) * "\t"
        fmt += tabs + note.content
    return fmt


class PositionalCategoryGroup(CategoryGroup):
    """A `Group` for `PositionalCategories`

    `PositionalCategories` are `Categories` that are also `Notes`.
    Their position matters in that any `Note` that comes after it is considered to be part of this `PositionalCategory`.
    An example would be if your notes are in chronological order and
    all notes that follow a "Chapter 1" `PositionalCategory` belong to "Chapter 1".

    Parameters
    ----------
    name : str
        The name that will be assigned to the `Category`, used as a key in `NoteUtil.categories`.
    prefixes : list of str
        The prefixes used to determine that a `Note` will belong to what `Categories`.
    fmt: function
        The function applied to a `Category` to give it its `str` value.
        Must take a `Category` as the **only** parameter.

    Examples
    --------
     If you want Category 2 in Category 1, an example prefixing would look like::
         cat1 = PositionalCategoryGroup("Category 1", ["!"])
         cat2 = PositionalCategoryGroup("Category 2", ["!", "@"])
     Notice that Category 2 includes Category 1's prefix and then adds on its own prefix.
     If this were the case, then a `Note` would have to look like the following::
         # In Category 1:
         "! Category 1"
             "Hi I am example 1."
             "Example 2 here."
         # In Category 2 and Category 1:
         "!@ Category 2"
             "Example 3's got this."
             "Example 4, I am."

    .. note::
        There is no way of placing a `Note` only in Category 1 after Category 2 has been declared.
        That is, it is impossible to tag a note with only Category 1 if it comes after Category 2.
        This is only the case if Category 2 is in Category 1.

    """

    def __init__(self, name, prefixes, fmt=pos_cat_fmt):
        super().__init__(name, prefixes, fmt)


def glo_cat_fmt(category: GlobalCategory):
    fmt = category.name + "\n"
    for note in category.notes:
        fmt += "\t" + note.content
    return fmt


class GlobalCategoryGroup(CategoryGroup):
    """A `Group` for `GlobalCategories`.

    `GlobalCategories` are `Categories` whose `Note's` position is irrelevant.
    An example of a `GlobalCategory` would be People, such as different important people throughout history.
    There could be important people in several time periods, so it's illogical to separate them and group them together.

    Parameters
    ----------
    name : str
        The name that will be assigned to the `GlobalCategory`, used as a key in `NoteUtil.categories`.
    prefixes : list of str
        The prefix used to determine that a `Note` will belong to the `GlobalCategory`.
    fmt: function
        The function applied to the `GlobalCategory` to give it its `str` value.
        Must take a `GlobalCategory` as the **only** parameter.

    Examples
    --------
    If you want Category 2 in Category 1, an example prefixing would look like::
         cat1 = GlobalCategoryGroup("Category 1", ["!"], False)
         cat2 = GlobalCategoryGroup("Category 2", ["!", "@"], False)
     Notice that Category 2 includes Category 1's prefix and then adds on its own prefix.
     If this were the case, then a `Note` would have to look like the following::
         # In Category 1:
             "!Hi I am example 1."
             "!Example 2 here."
         # In Category 2 and Category 1:
             "!@Example 3's got this."
             "!@Example 4, I am."
    """
    def __init__(self, name, prefixes, fmt=glo_cat_fmt):
        super().__init__(name, prefixes, fmt)
