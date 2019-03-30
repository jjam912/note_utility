"""This module is **Temporarily** for custom comparisons used when comparing `Note`s in `NoteUtil`."""


def is_equal(note, **kwargs):
    """Is True when all of the `kwargs` values are exactly equal to the `Note`'s attributes.

    Returns
    -------
    bool
    """

    return all(getattr(note, attr) is not None and val == getattr(note, attr) for attr, val in kwargs.items())


def is_in(note, **kwargs):
    """Is True when all of the `kwargs` values are "in" the `Note`'s attributes.

    Returns
    -------
    bool
    """

    return all(getattr(note, attr) is not None and val in getattr(note, attr) for attr, val in kwargs.items())


def is_similar(note, **kwargs):
    """Is True when all of the `kwargs` values are equal ignoring case to the `Note`'s attributes.

    Returns
    -------
    bool
    """

    return all(getattr(note, attr) is not None and val.lower() == getattr(note, attr).lower() for attr, val in kwargs.items())


def is_in_similar(note, **kwargs):
    """Is True when all of the `kwargs` values are "in" ignoring case to the `Note`'s attributes.

    Returns
    -------
    bool
    """

    return all(getattr(note, attr) is not None and val.lower() in getattr(note, attr).lower() for attr, val in kwargs.items())
