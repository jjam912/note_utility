class Note:
    """A `Note` is the text found in the notes_list file. It contains the actual notes from each line of text.

        Parameters
        ----------
        content : str
            The content of the `Note` excluding `prefixes` and `Extensions`.
        nindex : int
            The `Note` index that corresponds to the position in the `NoteUtil.notes_list`.
        kwargs
            Any other parameters that extend the `Note`.

        Other Parameters
        ----------------
        If the `Note` is a `Pair`:
            term : str
                The first part of text that came before the `separator`.
            definition : str
                The second part of text that came after the `separator`.
            separator : str
                The string that separates the `term` and `definition` of this `Note`.

    """

    def __init__(self, content, nindex, **kwargs):
        # Basics of all notes_list
        self._rcontent = content
        self.content = content
        self.nindex = nindex

        # Pair parameters
        self.term = kwargs.get("term", None)
        self.definition = kwargs.get("definition", None)
        self.separator = kwargs.get("separator", None)

    def is_pair(self):
        """Returns whether the `Note` has the parameters of a pair (`term`, `definition`, and `separator`).

        Returns
        -------
        bool
        """

        return self.term is not None and self.definition is not None and self.separator is not None
