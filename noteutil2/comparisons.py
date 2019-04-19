"""This module is for comparisons used when comparing `Note`s in `NoteUtil`."""
import enum


def is_equal(note, **kwargs) -> bool:
    """Is True when all of the `kwargs` values are exactly equal to the `Note`'s attributes.

    Returns
    -------
    bool
    """

    return all(val == getattr(note, attr) for attr, val in kwargs.items())


def is_similar(note, **kwargs) -> bool:
    """Is True when all of the `kwargs` values are equal ignoring case to the `Note`'s attributes.

    Returns
    -------
    bool
    """

    return all(getattr(note, attr) is not None and val.lower() == getattr(note, attr).lower() for attr, val in kwargs.items())


def is_in(note, **kwargs) -> bool:
    """Is True when all of the `kwargs` values are "in" the `Note`'s attributes.

    Returns
    -------
    bool
    """

    return all(getattr(note, attr) is not None and val in getattr(note, attr) for attr, val in kwargs.items())


def is_similar_in(note, **kwargs) -> bool:
    """Is True when all of the `kwargs` values are "in" ignoring case to the `Note`'s attributes.

    Returns
    -------
    bool
    """

    return all(getattr(note, attr) is not None and val.lower() in getattr(note, attr).lower() for attr, val in kwargs.items())


class CompareOptions(enum.Enum):
    """Enum for selecting compare options for NoteUtil.get methods.

    Constants
    ---------
    EQUALS : function
        Tests for equality. Use with ints, or when you want exact matching.
    SIMILAR : function
        Tests for equals ignore case. Use with strings when you want to match, but ignore case.
    IN : function
        Tests for "in". Use with strings when you want to know if the exact value is in the attribute.
    SIN : function
        Tests for "in" and also ignores case. Use with strings when you want to know if the value is in the attribute.
        Stands for "Similar In".

    """

    EQUALS = is_equal
    SIMILAR = is_similar
    IN = is_in
    SIN = is_similar_in


