class Note:
    """A `Note` is the text found in the notes file. It contains the actual notes from each line of text.

    Parameters
    ----------
    content : str
        The content of the `Note` excluding `prefixes` and `Extensions`.
    nindex : int
        The `Note` index that corresponds to the position in the `NoteUtil.notes`.
    **kwargs
        Any other parameters that extend the `Note`.

    Other Parameters
    ----------------
    If the `Note` is a `Heading`:
        heading_char : str
            The character used as to indicate this `Note` is a heading.
        level : int
            The depth of heading hierarchy of this `Note`.
        heading : str
            The prefix of the content that was removed and the actual heading string.
        heading_name : str
            The content of the `Note` without the `heading`.
        begin_nindex : int
            The beginning note index for this heading.
        end_nindex : int
            The ending note index for this heading.
        nindexes : List[int]
            List of indexes starting from the `begin_nindex` to the `end_nindex` like a range.
    If the `Note` is a `Pair`:
        term : str
            The first part of text that came before the `separator`.
        definition : str
            The second part of text that came after the `separator`.
        separator : str
            The string that separates the `term` and `definition` of this `Note`.
    """

    def __init__(self, content, nindex, **kwargs):
        # Basics of all notes
        self.content = content
        self.nindex = nindex

        # Heading parameters
        self.heading_char = kwargs.get("heading_char", None)
        self.level = kwargs.get("level", None)
        self.heading = kwargs.get("heading", None)
        self.heading_name = kwargs.get("heading_name", None)

        self.begin_nindex = kwargs.get("begin_nindex", None)
        self.end_nindex = None      # Later assigned
        self.nindexes = None

        # Pair parameters
        self.term = kwargs.get("term", None)
        self.definition = kwargs.get("definition", None)
        self.separator = kwargs.get("separator", None)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __ne__(self, other):
        return repr(self) != repr(other)

    def __lt__(self, other):
        return self.nindex < other.nindex

    def __gt__(self, other):
        return self.nindex > other.nindex

    def __repr__(self):
        """What a `Note` looked like before parsing it."""

        rcontent = ""
        if self.is_heading():
            rcontent += self.heading
        rcontent += self.content
        return rcontent

    def is_pair(self):
        """Returns whether the `Note` should have the parameters of a pair.

        Returns
        -------
        bool
        """

        return self.separator is not None

    def is_heading(self):
        """Returns whether the `Note` should have the parameters of a heading.

        Returns
        -------
        bool
        """

        return self.heading_char is not None
