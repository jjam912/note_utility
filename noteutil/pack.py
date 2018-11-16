from abc import ABC
from .note import *


class Pack(Note, ABC):
    def __init__(self, content, nindex, *, extensions: list=None, packs: list=None, notes: list=None):
        super().__init__(content, nindex, extensions=extensions, packs=packs)
        self.notes = [] if notes is None else notes

        self.tabs = "\t" * len(self.packs)
        self.lines = []
        self.pairs = []

        for note in notes:
            if isinstance(note, Line):
                self.lines.append(note)
            elif isinstance(note, Pair):
                self.pairs.append(note)

    def __eq__(self, other):
        return self.nindex == other.nindex

    def __ne__(self, other):
        return self.nindex != other.nindex

    def __contains__(self, item: Note):
        for note in self.notes:
            if item == note:
                return True
        return False

    def __lt__(self, other):
        return self.nindex < other.nindex

    def __gt__(self, other):
        return self.nindex > other.nindex

    def __hash__(self):
        return hash(self._rcontent.lower())

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, item):
        return self.notes[item]

    def __missing__(self, key):
        raise errors.NoteIndexError(key + " not in notes.")

    def __delitem__(self, key):
        del self.notes[self.notes.index(key)]

    def __iter__(self):
        return iter(self.notes)

    def __reversed__(self):
        return reversed(self.notes)

    def __str__(self):
        return self._rcontent

    def append(self, note):
        i, j, k, n = 0, len(self.notes) // 2, len(self.notes), note.nindex
        while k - i > 1:
            mid = self.notes[j].nindex
            if n > mid:
                i = j
            else:
                k = j
            j = (i + k) // 2
        if n > self.notes[j].nindex:
            self.notes.insert(j, note)
        else:
            self.notes.insert(i, note)

    def insert(self, pack):
        # if pack.nindex < self.nindex:
        #     raise Something

        i, j, k, n = 0, len(self.packs) // 2, len(self.packs), pack.nindex
        while k - i > 1:
            mid = self.packs[j].nindex
            if n > mid:
                i = j
            else:
                k = j
            j = (i + k) // 2
        if n > self.notes[j].nindex:
            self.packs.insert(j, pack)
        else:
            self.packs.insert(i, pack)

