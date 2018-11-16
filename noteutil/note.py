from abc import ABC


# TODO: __repr__ should be the function that is used to convert the Note back into something that can be read in .nu
class Note(ABC):
    """Base class for all text Notes, which are created when parsing the note file.

    Attributes
    ----------
    content: :class:`str`
        The actual content of the notes; all of the text that was found in between separators.
    nindex: :class:`int`
        The note index that corresponds to position in the :attr:`NoteUtil.notes_list`.
    """

    def __init__(self, content: str, nindex: int, *, extensions: list = None, packs: list = None):
        super().__init__()
        self._rcontent = content
        self.content = content
        self.nindex = nindex
        self.extensions = {} if extensions is None else extensions
        self.packs = [] if packs is None else packs

        # for eg in self._egroups:
        #     if eg.name not in self.extensions:
        #         self.extensions[eg.name] = []
        #
        #     while True:
        #         try:
        #             i = self.content.index(eg.lbound)
        #         except IndexError:
        #             break
        #
        #         try:
        #             j = self.content.index(eg.rbound)
        #         except IndexError:
        #             raise errors.NoRightBound
        #
        #         self.extensions[eg.name].append(Extension(eg, self.content[i + len(eg.lbound): j].strip(), self))
        #         eg.notes.append(self)
        #         self.content = self.content[:i].strip() + eg.placeholder + self.content[j + len(eg.rbound):].strip()

    def __eq__(self, other):
        return self.nindex == other.nindex

    def __ne__(self, other):
        return self.nindex != other.nindex

    def __lt__(self, other):
        return self.nindex < other.nindex

    def __gt__(self, other):
        return self.nindex > other.nindex

    def __hash__(self):
        return hash(self._rcontent.lower())


class Line(Note):

    def __init__(self, content: str, nindex: int, lindex: int, *, extensions=None, packs=None):
        super().__init__(content, nindex, extensions=extensions, packs=packs)
        self.lindex = lindex

    def __repr__(self):
        return f"Line(\"{self.content}\", {self.nindex}, {self.lindex}, {repr(self.extensions)}, {repr(self.packs)})"


class Pair(Note):
    def __init__(self, content: str, nindex: int, pindex: int, separator: str, *, extensions=None, packs=None):
        super().__init__(content, nindex, extensions=extensions, packs=packs)
        self.pindex = pindex
        self.separator = separator

        tokens = tuple(content.split(separator))
        if len(tokens) != 2:
            raise errors.SeparatorError(f"There was either zero or more than one separator in the content: {content}")

        self.term, self.definition = tokens[0].strip(), tokens[1].strip()

    def __repr__(self):
        return (f"Pair(\"{self.content}\", {self.nindex}, {self.pindex}, \"{self.separator}\", "
                f"{repr(self.extensions)}, {repr(self.packs)})")
