class Note:
    """A Note is the text found in the notes file. It contains the actual notes from each line of text.
    They can be Headings, which means a group of notes that come after this Note belong to this Note.
        Only notes that come directly after this heading and before the next heading will belong to this Note.
        It is impossible to go back to this heading after we have passed the next heading.
    They can have Extensions, which are additional information added on separately from the content of this Note.
    They can be Pairs, which means it has a separator, term, and definition that can be used for quizzing.

    Parameters
    ----------
    noteutil : NoteUtil
        A reference to the NoteUtil that is creating this Note.
    content : str
        The content of the Note excluding prefixes and Extensions.
    nindex : int
        The Note index that corresponds to the position in the NoteUtil.notes.
    **kwargs
        Any other parameters that extend the Note.

    Attributes
    ----------
    content : str
        The content of the Note excluding prefixes and Extensions.
    rcontent : str
        The raw content of the Note before parsing, including prefixes and Extensions.
    nindex : int
        The index at which this Note resides in NoteUtil.notes.

    If the NoteUtil uses headings:
        previous_heading : Note
            The first heading that comes before this Note.
        next_heading : Note
            The first heading that comes after this Note.

    If the Note is a Heading:
        heading_char : str
            The character used as to indicate this Note is a heading.
        level : int
            The depth of heading hierarchy of this Note.
        heading : str
            The prefix of the content that was removed and the actual heading string.
        heading_name : str
            The content of the Note without the heading.
        begin_nindex : int
            The beginning note index for this heading.
        end_nindex : int
            The ending note index for this heading.

        See NoteUtil:
        pairs
        heading_order
        heading_names
        heading_level
        categories
        with_extensions
    If the Note is part of a Category:
        category_names : List[str]
            List of Category names that this Note belongs to.
        category_prefixes : List[str]
            List of Category prefixes that each Category name corresponds to.
    If the Note has Extensions:
        extension_names : List[str]
            A set of the generic names of the Extensions that this Note has.
        extensions : List[Extension]
            All of the Extensions that this Note has.
    If the Note is a Pair:
        term : str
            The first part of text that came before the separator.
        definition : str
            The second part of text that came after the separator.
        separator : str
            The string that separates the term and definition of this Note.
    """

    def __init__(self, noteutil, content, nindex, **kwargs):
        # Basics of all notes
        self._noteutil = noteutil
        self.content = content
        self.nindex = nindex

        # Heading parameters
        self.heading_char = kwargs.get("heading_char", None)
        self.level = kwargs.get("level", None)
        self.heading = kwargs.get("heading", None)
        self.heading_name = kwargs.get("heading_name", None)

        self.begin_nindex = kwargs.get("begin_nindex", None)
        self.end_nindex = None      # Later assigned

        # Category parameters
        self.category_names = kwargs.get("category_names", [])
        self.category_prefixes = kwargs.get("category_prefixes", [])

        # Pair parameters
        self.term = kwargs.get("term", None)
        self.definition = kwargs.get("definition", None)
        self.separator = kwargs.get("separator", None)

        # Extension parameters
        self.extension_names = kwargs.get("extension_names", [])
        self.extensions = kwargs.get("extensions", [])

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.rcontent == other.rcontent
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Note):
            return self.rcontent != other.rcontent
        else:
            return False

    def __lt__(self, other):
        return self.nindex < other.nindex

    def __gt__(self, other):
        return self.nindex > other.nindex

    def __repr__(self):
        rstring = "Note("
        rstring += "content='{0}', nindex={1}".format(self.content, self.nindex)
        if self.is_heading():
            rstring += (", heading_char='{0}', level={1}, heading='{2}', heading_name='{3}', begin_nindex={4}, "
                        "end_nindex={5}".format(self.heading_char, self.level, self.heading,
                                                self.heading_name, self.begin_nindex, self.end_nindex))
        if self.has_extensions():
            rstring += ", extension_names={0}".format(repr(self.extension_names))
            rstring += ", extensions=["
            for ext in self.extensions:
                rstring += repr(ext)
            rstring += "]"
        if self.is_pair():
            rstring += (", term='{0}', definition='{1}', separator='{2}'".format(self.term, self.definition,
                                                                                 self.separator))
        rstring += ")"
        return rstring

    @property
    def rcontent(self) -> str:
        """What a Note looked like before parsing it."""
        rcontent = ""
        if self.is_heading():
            rcontent += self.heading
        if self.has_categories():
            for prefix in self.category_prefixes:
                rcontent += prefix
        rcontent += self.content
        if self.has_extensions():
            for ext in self.extensions:
                rcontent += ext.rcontent
        return rcontent

    @property
    def previous_heading(self):
        if self._noteutil.heading_char is not None:
            for heading in self._noteutil.heading_order[::-1]:
                if self.nindex > heading.nindex:
                    return heading
        return None

    @property
    def next_heading(self):
        if self._noteutil.heading_char is not None:
            for heading in self._noteutil.heading_order:
                if self.nindex < heading.nindex:
                    return heading
        return None

    @property
    def pairs(self):
        if self.is_heading():
            return list(filter(lambda n: n.is_pair(), [self._noteutil.get(nindex=i)
                                                       for i in range(self.begin_nindex, self.end_nindex)]))
        return []

    @property
    def heading_order(self):
        if self.is_heading():
            return list(filter(lambda n: n.is_heading(), [self._noteutil.get(nindex=i)
                                                          for i in range(self.begin_nindex, self.end_nindex)]))
        return []

    @property
    def heading_names(self):
        if self.is_heading():
            return list(map(lambda n: n.heading_name, self.heading_order))
        return []

    @property
    def level_order(self):
        if self.is_heading():
            level_order = {name: [] for name in self._noteutil.level_names}
            for note in self.heading_order:
                level_name = self._noteutil.level_names[note.level - 1]
                level_order[level_name].append(note)
            return level_order
        return {}

    @property
    def categories(self):
        if self.is_heading():
            categories = {name: [] for name in self._noteutil.category_names}
            for note in [self._noteutil.get(nindex=i) for i in range(self.begin_nindex, self.end_nindex)]:
                for category_name in note.category_names:
                    categories[category_name].append(note)
            return categories
        else:
            return {}

    @property
    def with_extensions(self):
        if self.is_heading():
            return list(filter(lambda n: n.has_extensions(), [self._noteutil.get(nindex=i)
                                                              for i in range(self.begin_nindex, self.end_nindex)]))
        return []

    def is_pair(self) -> bool:
        """Returns whether the Note should have the parameters of a pair.

        Returns
        -------
        bool
        """

        return self.separator is not None

    def is_heading(self) -> bool:
        """Returns whether the Note should have the parameters of a heading.

        Returns
        -------
        bool
        """

        return self.heading_char is not None

    def has_categories(self) -> bool:
        """Returns whether the Note belongs to any Categories.

        Returns
        -------
        bool
        """

        return not not self.category_names

    def has_extensions(self) -> bool:
        """Returns whether the Note has any extensions.

        Returns
        -------
        bool
        """

        return not not self.extensions


class Extension:
    """An Extension is additional text added on to a Note.
    All Extensions have a corresponding name and bounded characters to distinguish it from the content of a Note.
    The Extension is taken out of the content of a Note and lives in a Note's extensions List.

    Parameters
    ----------
    content : str
        The actual notes of the Extension without any bounds.
    name : str
        The general name associated with the Extension/What it falls under.
    lbound : str
        The string that bounds the left side of the Extension.
    rbound : str
        The string that bounds the right side of the Extension.

    Attributes
    ----------
    content : str
    name : str
    lbound : str
    rbound : str
    """

    def __init__(self, content: str, name: str, lbound: str, rbound: str):
        self.content = content
        self.name = name
        self.lbound = lbound
        self.rbound = rbound

    @property
    def rcontent(self) -> str:
        return self.lbound + self.content + self.rbound

    def __eq__(self, other):
        if isinstance(other, Extension):
            return self.rcontent == other.rcontent
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Extension):
            return self.rcontent != other.rcontent
        else:
            return False

    def __repr__(self):
        rstring = "Extension("
        rstring += "content='{0}', name={1}, lbound={2}, rbound={3}".format(
            self.content, self.name, self.lbound, self.rbound)
        rstring += ")"
        return rstring



