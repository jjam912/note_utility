from .errors import *
from .notes import Note
from .noteutil import NoteUtil
import random
import copy
from typing import Generator
import os
import json


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
            open(self.lt_file, mode="w", encoding="utf8").close()

    def generate(self, *, randomize: bool) -> Generator[Note, None, None]:
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

        if randomize:
            random.shuffle(pairs)
        for pair in pairs:
            self.last_nindex = pair.nindex
            yield pair
        self.session += 1

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

    def append_box(self, time: int) -> None:
        """Adds an additional box to store pairs in.

        Parameters
        ----------
        time : int
            The time period for the box to be added.
            Must be greater than the time period of the last box before this one.

        Returns
        -------
        None

        Raises
        ------
        TimeTooShort
            If the time given is shorter than the current longest time period.
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

        Raises
        ------
        LastBox
            If the number of boxes is equal to 1.
        """

        if len(self.boxes) == 1:
            raise LastBox

        pairs = self.boxes.pop(len(self.boxes))
        for pair in pairs:
            pair.box -= 1
        self.times.pop(len(self.times))
        self.boxes[len(self.boxes)].extend(pairs)

    def edit_box(self, box: int, time: int) -> None:
        """Modifies the box and changes its time.

        Returns
        -------
        None

        Raises
        ------
        TimeTooShort
        TimeTooLong
        """

        if box not in self.times:
            raise BoxNumberError(box)

        prev_time = 1
        next_time = float("inf")
        if box - 1 in self.times:
            prev_time = self.times[box - 1]
        if box + 1 in self.times:
            next_time = self.times[box + 1]

        if time < prev_time:
            raise TimeTooShort(time)
        elif time > next_time:
            raise TimeTooLong(time)
        else:
            self.times[box] = time

    def save(self) -> None:
        """Writes Leitner state to a .lt file.

        Returns
        -------
        None
        """

        kwargs = dict()
        boxes = {}
        for box_number, pairs in self.boxes.items():
            boxes[box_number] = list(map(lambda p: p.rcontent, pairs))

        kwargs["boxes"] = boxes
        kwargs["times"] = self.times
        kwargs["session"] = self.session

        with open(self.lt_file, mode="w", encoding="utf8") as f:
            f.write(json.dumps(kwargs))

    def load(self) -> None:
        """Loads a Leitner state from a .lt file.

        Returns
        -------
        None
        """

        self.reset()
        kwargs = dict()
        with open(self.lt_file, mode="r", encoding="utf8") as f:
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
                        break

        for box_number, time_period in kwargs.get("times", self.times).items():
            self.times[int(box_number)] = int(time_period)
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
        for box_number, pairs in zip(self.boxes.keys(), list(self.boxes.values()).copy()):
            for _ in range(len(pairs)):
                old_note = pairs.pop(0)
                for new_note in new_pairs:
                    if old_note.rcontent == new_note.rcontent:
                        new_pairs.remove(new_note)
                        self.boxes[box_number].append(new_note)
                        new_note.box = box_number
                        break

        for pair in new_pairs:
            pair.box = 1
            self.boxes[1].append(pair)

        for pairs in self.boxes.values():
            pairs.sort(key=lambda n: n.nindex)

        self.last_nindex = 0
        self.session = 1
        self.lt_file = self.noteutil.note_file.split(".")[0] + ".lt"

