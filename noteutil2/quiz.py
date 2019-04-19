from .comparisons import CompareOptions
from .errors import *
from .notes import Note
import random
import os.path
import copy
from typing import Union, Generator
import json


class Quiz:
    """Quiz takes terms and definitions of `Note`s and forms questions and answers from them.
    It keeps track of which terms were marked correct and which terms were marked incorrect.

    Parameters
    ----------
    noteutil : `NoteUtil`
        The `NoteUtil` that has the terms and definitions to be used with this Quiz.

    Attributes
    ----------
    noteutil : `NoteUtil`
    last_nindex : int
        The `nindex` of the last `Note` generated.
    correct : Set[`Note`]
        All `Note`s marked as correct.
    incorrect : Set[`Note`]
        All `Note`s marked as incorrect.
    randomize : bool
        Whether to generate `Note`s randomly (T) or chronologically (F).
    pairs : List[`Note`]
        List of all `Note`s that are pairs that the `Quiz` is generating from.
        This can either be all pairs in `NoteUtil`, or only pairs inside a specific heading.
    """

    QUESTION_FORMAT = ""
    ANSWER_FORMAT = ""

    def __init__(self, noteutil):
        self.noteutil = noteutil
        self.last_nindex = 0
        self.correct = set()
        self.incorrect = set()

        # Options
        self.randomize = True
        self.pairs = self.noteutil.pairs
        self.heading = None

        # Saving
        self.qz_file = self.noteutil.note_file.split(".")[0] + ".qz"

    def generate(self) -> Generator[str, None, None]:
        """A generator that yields `Note`s, either chronologically or randomly.
        Once a generator is created, it is "frozen in time," and isn't affected by any changes to `Quiz`.
        However, `Quiz` keeps track of the last index used, which changes every time this generator is activated.

        Yields
        ------
        `Note`
            A pair that is either random or in chronological order.
        """

        pairs = copy.deepcopy(self.pairs)       # This could be changed to use indices
        if self.randomize:
            random.shuffle(pairs)
            while pairs:
                note = pairs.pop()
                self.last_nindex = note.nindex
                yield note
        else:
            index = 0
            while index != len(pairs):
                note = pairs[index]
                self.last_nindex = note.nindex
                yield note
                index += 1

    def append(self, pair, correct: bool) -> None:
        """Adds a pair to one of the correct or incorrect sets.
        It will also remove it from the other set if it's in that one.

        Parameters
        ----------
        pair : `Note`
            The pair to add to either the correct set or the incorrect set.
        correct : bool
            Whether to add to the correct set (T) or the incorrect set (F).

        Returns
        -------
        None
        """

        if correct:
            self.correct.add(pair)
            self.incorrect.discard(pair)
        else:
            self.incorrect.add(pair)
            self.correct.discard(pair)

    def remove(self, pair, correct: bool) -> None:
        """Removes a pair from one of the correct or incorrect sets.

        Parameters
        ----------
        pair : `Note`
            The pair to remove from either the correct set or the incorrect set.
        correct : bool
            Whether to remove from the correct set (T) or the incorrect set (F).

        Returns
        -------
        None
        """

        if correct:
            self.correct.discard(pair)
        else:
            self.incorrect.discard(pair)

    def clear(self) -> None:
        """Empties the correct and incorrect sets.

        Returns
        -------
        None
        """

        self.correct.clear()
        self.incorrect.clear()

    def select_heading(self, heading: Union[None, str, Note]) -> None:
        """Changes the current heading and pairs to match the pairs in the given heading.

        Parameters
        ----------
        heading : None or `Note` or str
            The `Note` or heading name whose pairs should be used.
            If left as None, all pairs in `NoteUtil` will be used.

        Returns
        -------
        None

        Raises
        ------
        HeadingExpected
            If the `Note` provided is not None and isn't a heading.
        HeadingNotFound
            If the str provided is not None and it isn't a recognized heading name.
        """

        if heading is None:
            self.heading = None
            self.pairs = self.noteutil.pairs
            return

        if isinstance(heading, Note):
            if not heading.is_heading():
                raise HeadingExpected(heading)
            self.heading = heading
        elif heading in self.noteutil.heading_names:
            self.heading = self.noteutil.get(heading_name=heading)
        else:
            raise HeadingNotFound(heading)

        self.pairs = list(filter(lambda n: n.is_pair(),
                                 self.noteutil.notes[self.heading.begin_nindex: self.heading.end_nindex]))

    def save(self) -> None:
        """Writes correct and incorrect terms to a .qz file.

        Returns
        -------
        None
        """

        kwargs = dict()
        kwargs["correct"] = list(map(lambda p: p.rcontent, self.correct))
        kwargs["incorrect"] = list(map(lambda p: p.rcontent, self.incorrect))
        with open(self.qz_file, mode="w") as f:
            f.write(json.dumps(kwargs))

    def load(self) -> None:
        """Loads correct and incorrect terms to a .qz file.

        Returns
        -------
        None
        """

        kwargs = dict()
        with open(self.qz_file, mode="r") as f:
            try:
                kwargs = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                pass

        for rcontent in kwargs.get("correct", []):
            for note in self.noteutil.notes:
                if rcontent == note.rcontent:
                    self.append(note, True)

        for rcontent in kwargs.get("incorrect", []):
            for note in self.noteutil.notes:
                if rcontent == note.rcontent:
                    self.append(note, False)
                    
    def reset(self) -> None:
        """Resets the state of the `Quiz` to as if it had just been initialized except for `randomize`.
        
        Returns
        -------
        None
        """
        
        self.last_nindex = 0
        self.clear()
        self.pairs = self.noteutil.pairs
        self.heading = None

    # This function seemingly has no purpose because when I edit notes with `NoteUtil`, they get edited in `Quiz` too.
    def refresh(self, noteutil) -> None:
        """Resets the state of the `Quiz` to match a new `NoteUtil`.
        This is the same as saving the NoteUtil and then loading it with a different `NoteUtil`.
        As such, only identical `Note`s from both `NoteUtil`s are kept.

        Returns
        -------
        None
        """

        self.noteutil = noteutil

        for old_note in self.correct.copy():
            self.remove(old_note, True)
            for new_note in self.noteutil.notes:
                if old_note.rcontent == new_note.rcontent:
                    self.append(new_note, True)

        for old_note in self.incorrect.copy():
            self.remove(old_note, False)
            for new_note in self.noteutil.notes:
                if old_note.rcontent == new_note.rcontent:
                    self.append(new_note, False)

        self.last_nindex = 0
        self.pairs = self.noteutil.pairs
        self.heading = None
        self.qz_file = self.noteutil.note_file.split(".")[0] + ".qz"



