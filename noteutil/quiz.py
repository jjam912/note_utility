from .errors import *
from .notes import Note
from .noteutil import NoteUtil
import random
from itertools import filterfalse
import copy
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
    pairs : List[Note]
        List of all Notes that are pairs that the Quiz is generating from.
        This can either be all pairs in NoteUtil, or only pairs inside a specific heading.
    heading : None or Note
        The heading whose pairs are being used.
        It is None if pairs are being used from all of NoteUtil's pairs, or the correct/incorrect list.
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
        self.heading = None

        # Saving
        self.qz_file = self.noteutil.note_file.split(".")[0] + ".qz"
        if not os.path.exists(self.qz_file):
            open(self.qz_file, mode="w").close()

    def generate(self, *, randomize: bool) -> Generator[Note, None, None]:
        """A generator that yields Notes, either chronologically or randomly.
        Once a generator is created, it is "frozen in time," and isn't affected by any changes to Quiz.
        However, Quiz keeps track of the last index used, which changes every time this generator is activated.

        Parameters
        ----------
        randomize : bool
            Whether to generate a random term from the list of pairs.

        Yields
        ------
        Note
            A pair that is either in random or chronological order.
        """

        pairs = copy.deepcopy(self.pairs)       # This could be changed to use indices

        if randomize:
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
            try:
                self.incorrect.remove(pair)
            except ValueError:
                pass
        else:
            if pair not in self.incorrect:
                self.incorrect.append(pair)
            try:
                self.correct.remove(pair)
            except ValueError:
                pass

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

    def select_heading(self, heading: Union[None, str, Note]) -> None:
        """Changes the current heading and pairs to match the pairs in the given heading.

        Parameters
        ----------
        heading : None or Note or str
            The Note or heading name whose pairs should be used.
            If the heading name is "correct" or "incorrect", the pairs in the corresponding list will be used.
            If the heading name is "unmarked", the pairs that are not in the correct or incorrect list will be used.
            If left as None, all pairs in NoteUtil will be used.

        Returns
        -------
        None

        Raises
        ------
        HeadingExpected
            If the Note provided is not None and isn't a heading.
        HeadingNotFound
            If the str provided is not None and it isn't a recognized heading name.
        """

        if heading is None or heading == "none":
            self.heading = None
            self.pairs = self.noteutil.pairs
            return

        if heading == "correct":
            self.heading = "correct"
            self.pairs = self.correct
            return
        elif heading == "incorrect":
            self.heading = "incorrect"
            self.pairs = self.incorrect
            return
        elif heading == "unmarked":
            self.heading = "unmarked"
            self.pairs = list(filterfalse(lambda p: p in self.incorrect or p in self.correct, self.noteutil.pairs))
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

        self.reset()
        kwargs = dict()
        with open(self.qz_file, mode="r") as f:
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
        self.heading = None
        self.qz_file = self.noteutil.note_file.split(".")[0] + ".qz"


# 1, 2, 3, 5, 11, 19, 29
class Leitner:
    """The Leitner system is a method of spaced repetition where cards are reviewed at increasing intervals.

    If we model a pair as a flashcard (term and definition), then we can also use the Leitner system.
    We use seven "boxes" numbered 1-7, and every time our session is divisible by the box period, we review that box.
    Any terms that we mark as correct will advance to the next box number (+1), and incorrect ones will reset to box 1.

    Parameters
    ----------
    noteutil : NoteUtil
        The NoteUtil that has terms an definitions to be used in this Leitner.

    Attributes
    ----------
    noteutil : NoteUtil
    last_nindex : int
        The note index of the last Note generated.
    boxes : Dict[int, List[Note]]
        A dictionary where each box number (key) maps to the list of Notes inside of it (value).
    times : Dict[int, int]
        A dictionary where each box number (key) maps to the time period before review (# of sessions) (value).
    session : int
        The session number that determines which boxes will be reviewed.
    lt_file : str
        The name of the .lt file that will save Leitner's boxes.
    """

    def __init__(self, noteutil: NoteUtil):
        self.noteutil = noteutil
        self.last_nindex = 0
        self.boxes = dict(zip([x + 1 for x in range(7)], [[] for _ in range(7)]))
        for pair in self.noteutil.pairs:
            pair.box = 1
            self.boxes[1].append(pair)

        self.times = {1: 1, 2: 2, 3: 3, 4: 5, 5: 11, 6: 19, 7: 29}
        self.session = 1

        # Saving
        self.lt_file = self.noteutil.note_file.split(".")[0] + ".lt"
        if not os.path.exists(self.lt_file):
            open(self.lt_file, mode="w").close()

    def generate(self) -> Generator[Note, None, None]:
        """A generator that yields Notes according to the session number.
        If the session number is divisible by the time on a box, then we review that box.

        Yields
        ------
        Note
            A randomly selected pair from all of the pairs we are reviewing in this session.
        """

        pairs = []
        for number, box in self.boxes.items():
            if self.session % self.times[number] == 0:
                pairs.extend(self.boxes[number])

        self.session += 1       # Not sure if this is the right place for it to go
        random.shuffle(pairs)
        for pair in pairs:
            self.last_nindex = pair.nindex
            yield pair

    def correct(self, pair: Note) -> None:
        """Handles the pair if it was answered correctly.
        Removes it from its current box and then moves it to the next box.

        Parameters
        ----------
        pair : Note
            The pair that was answered correctly.

        Returns
        -------
        None
        """

        if pair.box != len(self.boxes):
            self.boxes[pair.box].remove(pair)
            self.boxes[pair.box + 1].append(pair)
            pair.box += 1

    def incorrect(self, pair: Note) -> None:
        """Handles the pair if it was answered correctly.
        Removes it from its current box and then moves it to the next box.

        Parameters
        ----------
        pair : Note
            The pair that was answered incorrectly.

        Returns
        -------
        None
        """

        if pair.box != 0:
            self.boxes[pair.box].remove(pair)
            self.boxes[1].append(pair)
            pair.box = 1

    def add_box(self, time: int) -> None:
        """Adds an additional box to store pairs in.

        Parameters
        ----------
        time : int
            The time period for the box to be added.
            Must be greater than the time period of the last box before this one.

        Returns
        -------
        None
        """

        if time <= self.times[len(self.times)]:
            raise TimeTooShort(self.times[len(self.boxes)])

        self.boxes[len(self.boxes) + 1] = []
        self.times[len(self.times) + 1] = time

    def pop_box(self):
        """Pops the last box and moves the lost pairs to the box before the one just popped.

        Returns
        -------
        None
        """

        if len(self.boxes) == 1:
            raise LastBox

        pairs = self.boxes.pop(len(self.boxes))
        self.times.pop(len(self.times))
        self.boxes[len(self.boxes)].extend(pairs)

    def save(self) -> None:
        """Writes Leitner state to a .lt file.

        Returns
        -------
        None
        """

        kwargs = dict()
        boxes = self.boxes
        for box_number, pairs in boxes.items():
            boxes[box_number] = list(map(lambda p: p.rcontent, pairs))

        kwargs["boxes"] = boxes
        kwargs["times"] = self.times
        kwargs["session"] = self.session

        with open(self.lt_file, mode="w") as f:
            f.write(json.dumps(kwargs))

    def load(self) -> None:
        """Loads a Leitner state from a .lt file.

        Returns
        -------
        None
        """

        self.reset()
        kwargs = dict()
        with open(self.lt_file, mode="r") as f:
            try:
                kwargs = json.loads(f.read())
            except json.JSONDecodeError:
                pass

        boxes = kwargs.get("boxes", {})
        for box_number, rcontents in boxes.items():
            box_number = int(box_number)
            for rcontent in rcontents:
                for pair in self.boxes[1].copy():
                    if rcontent == pair.rcontent:
                        self.boxes[1].remove(pair)
                        pair.box = box_number
                        self.boxes[box_number].append(pair)

        for box_number, time_period in kwargs.get("times", self.times).items():
            self.times[int(box_number)] = time_period
        self.session = kwargs.get("session", self.session)

    def reset(self) -> None:
        """Resets the state of the Leitner to as if it had just been initialized.

        Returns
        -------
        None
        """

        self.__init__(self.noteutil)

    def refresh(self, noteutil: NoteUtil) -> None:
        """Resets the state of the Leitner to match a new NoteUtil.
        This is the same as saving the NoteUtil and then loading it with a different NoteUtil.
        As such, only identical Notes from both NoteUtils are kept.

        Returns
        -------
        None
        """

        self.noteutil = noteutil

        new_pairs = copy.deepcopy(self.noteutil.pairs)
        for box_number, pairs in self.boxes.items():
            for old_note in pairs.copy():
                pairs.remove(old_note)
                for new_note in new_pairs:
                    if old_note.rcontent == new_note.rcontent:
                        new_pairs.remove(new_note)
                        self.boxes[box_number].append(new_note)
                        new_note.box = box_number
                        break
        for pair in new_pairs:
            pair.box = 1
            self.boxes[1].append(pair)

        self.last_nindex = 0
        self.session = 1
        self.lt_file = self.noteutil.note_file.split(".")[0] + ".lt"

