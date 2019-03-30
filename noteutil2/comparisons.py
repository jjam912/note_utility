"""This module is **Temporarily** for custom comparisons used when comparing `Note`s in `NoteUtil`."""


def is_equal(note, **kwargs):
    return all(getattr(note, attr) is not None and val == getattr(note, attr) for attr, val in kwargs.items())


def is_in(note, **kwargs):
    return all(getattr(note, attr) is not None and val in getattr(note, attr) for attr, val in kwargs.items())


def is_similar(note, **kwargs):
    return all(getattr(note, attr) is not None and val.lower() == getattr(note, attr).lower() for attr, val in kwargs.items())


def is_in_similar(note, **kwargs):
    return all(getattr(note, attr) is not None and val.lower() in getattr(note, attr).lower() for attr, val in kwargs.items())
