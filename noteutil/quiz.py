from .errors import *
from .notes import Note
from .noteutil import NoteUtil
import random
from itertools import filterfalse
from typing import Union, Generator
import os
import json


class Quiz:
    """Quiz takes terms and definitions of Notes and generates them in useful sequences.
    It keeps track of which terms were marked correct and which terms were marked incorrect.

    Parameters
    ----------
    noteutil : NoteUtil
        The NoteUtil that has the terms and definitions to be used with this Quiz.

    Attributes
    ----------
    noteutil : NoteUtil
    last_nindex : int
        The nindex of the last Note generated.
    correct : List[Note]
        All Notes marked as correct.
    incorrect : List[Note]
        All Notes marked as incorrect.
    unmarked : List[Note]
        All Notes neither marked correct nor incorrect.
    pairs : List[Note]
        List of all Notes that are pairs that the Quiz is generating from.
        This can either be all pairs in NoteUtil, or only pairs inside a specific heading/category.
    division : str or Note
        The heading/category whose pairs are being used.
    qz_file : str
        File name for the .qz file to save the Quiz's correct and incorrect lists.
    """

    def __init__(self, noteutil: NoteUtil):
        self.noteutil = noteutil
        self.last_nindex = 0
        self.correct = list()
        self.incorrect = list()

        # Options
        self.pairs = self.noteutil.pairs
        self.division = "none"

        # Saving
        self.qz_file = self.noteutil.note_file.split(".")[0] + ".qz"
        if not os.path.exists(self.qz_file):
            open(self.qz_file, mode="w", encoding="utf8").close()

    @property
    def unmarked(self):
        return list(filterfalse(lambda p: p in self.incorrect or p in self.correct, self.noteutil.pairs))

    def generate(self, *, randomize: bool) -> Generator[Note, None, None]:
        """A generator that yields Notes, either chronologically or randomly.
        Quiz keeps track of the last index used, which changes every time this generator is iterated.

        Parameters
        ----------
        randomize : bool
            Whether to generate a random term from the list of pairs.

        Yields
        ------
        Note
            A pair that is either in random or chronological order.
        """

        notes = [n for n in self.pairs]
        if randomize:
            random.shuffle(notes)
            while notes:
                index = random.randint(0, len(notes) - 1)
                note = notes.pop(index)
                self.last_nindex = note.nindex
                yield note
        else:
            index = 0
            while index < len(notes):
                note = notes[index]
                self.last_nindex = note.nindex
                yield note
                index += 1

    def append(self, pair: Note, *, correct: bool) -> None:
        """Adds a pair to one of the correct or incorrect lists.
        It will also remove it from the other list if it's in that one.

        Parameters
        ----------
        pair : Note
            The pair to add to either the correct list or the incorrect list.
        correct : bool
            Whether to add to the correct list (T) or the incorrect list (F).

        Returns
        -------
        None
        """

        if correct:
            if pair not in self.correct:
                self.correct.append(pair)
            self.remove(pair, correct=False)
        else:
            if pair not in self.incorrect:
                self.incorrect.append(pair)
            self.remove(pair, correct=True)

    def remove(self, pair: Note, *, correct: bool) -> None:
        """Removes a pair from one of the correct or incorrect lists.

        Parameters
        ----------
        pair : Note
            The pair to remove from either the correct list or the incorrect list.
        correct : bool
            Whether to remove from the correct list (T) or the incorrect list (F).

        Returns
        -------
        None
        """

        if correct:
            try:
                self.correct.remove(pair)
            except ValueError:
                pass
        else:
            try:
                self.incorrect.remove(pair)
            except ValueError:
                pass

    def clear(self) -> None:
        """Empties the correct and incorrect lists.

        Returns
        -------
        None
        """

        self.correct.clear()
        self.incorrect.clear()

    def select_pairs(self, division: Union[None, str, Note]) -> None:
        """Changes the current division and pairs to match the pairs in the given Heading/Category.

        Parameters
        ----------
        division : Note or str
            The Note or heading name or category name whose pairs should be used.
            If the division name is "correct" or "incorrect", the pairs in the corresponding list will be used.
            If the division name is "unmarked", the pairs that are not in the correct or incorrect list will be used.
            If left as None or "none", all pairs in NoteUtil will be used.

        Returns
        -------
        None

        Raises
        ------
        HeadingExpected
            If the Note provided is not None and isn't a heading.
        DivisionNotFound
            If the str provided is not None and it isn't a recognized heading or category name.
        """

        if division is None:
            self.division = "None"
            self.pairs = self.noteutil.pairs
            return

        if isinstance(division, str):
            if division.lower() == "none":
                self.division = "None"
                self.pairs = self.noteutil.pairs
                return
            elif division.lower() == "correct":
                self.division = "Correct"
                self.pairs = self.correct
                return
            elif division.lower() == "incorrect":
                self.division = "Incorrect"
                self.pairs = self.incorrect
                return
            elif division.lower() == "unmarked":
                self.division = "Unmarked"
                self.pairs = self.unmarked
                return
            elif division in self.noteutil.category_names:
                self.division = division
                self.pairs = list(filter(lambda n: n.is_pair(), self.noteutil.categories[division]))
                return
            elif division in self.noteutil.heading_names:
                division = self.noteutil.get(heading_name=division)
        if isinstance(division, Note):
            if not division.is_heading():
                raise HeadingExpected(division)
            self.division = division
            self.pairs = list(filter(lambda n: n.is_pair(),
                                     self.noteutil.notes[self.division.begin_nindex: self.division.end_nindex]))
        else:
            raise DivisionNotFound(division)

    def save(self) -> None:
        """Writes correct and incorrect terms to a .qz file.

        Returns
        -------
        None
        """

        kwargs = dict()
        kwargs["correct"] = list(map(lambda p: p.rcontent, self.correct))
        kwargs["incorrect"] = list(map(lambda p: p.rcontent, self.incorrect))
        with open(self.qz_file, mode="w", encoding="utf8") as f:
            f.write(json.dumps(kwargs))

    def load(self) -> None:
        """Loads correct and incorrect terms to a .qz file.

        Returns
        -------
        None
        """

        self.reset()
        kwargs = dict()
        with open(self.qz_file, mode="r", encoding="utf8") as f:
            try:
                kwargs = json.loads(f.read())
            except json.JSONDecodeError:
                pass

        for rcontent in kwargs.get("correct", []):
            for note in self.noteutil.notes:
                if rcontent == note.rcontent:
                    self.append(note, correct=True)

        for rcontent in kwargs.get("incorrect", []):
            for note in self.noteutil.notes:
                if rcontent == note.rcontent:
                    self.append(note, correct=False)
                    
    def reset(self) -> None:
        """Resets the state of the Quiz to as if it had just been initialized.
        
        Returns
        -------
        None
        """
        
        self.__init__(self.noteutil)

    def refresh(self, noteutil: NoteUtil) -> None:
        """Resets the state of the Quiz to match a new NoteUtil.
        This is the same as saving the NoteUtil and then loading it with a different NoteUtil.
        As such, only identical Notes from both NoteUtils are kept.

        Returns
        -------
        None
        """

        self.noteutil = noteutil

        for old_note in self.correct.copy():
            self.remove(old_note, correct=True)
            for new_note in self.noteutil.pairs:
                if old_note.rcontent == new_note.rcontent:
                    self.append(new_note, correct=True)
                    break

        for old_note in self.incorrect.copy():
            self.remove(old_note, correct=False)
            for new_note in self.noteutil.pairs:
                if old_note.rcontent == new_note.rcontent:
                    self.append(new_note, correct=False)
                    break

        self.last_nindex = 0
        self.pairs = self.noteutil.pairs
        self.division = None
        self.qz_file = self.noteutil.note_file.split(".")[0] + ".qz"
