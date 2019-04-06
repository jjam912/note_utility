from .notes import Note
from .comparisons import CompareOptions
from .errors import *
import os.path


def readlines(f):
    """Splits a file into lines without the "\n" suffixes.

    Parameters
    ----------
    f : File

    Yields
    ------
    str
    """

    lines = f.read().split("\n")
    for line in lines:
        yield line.strip()


class NoteUtil:
    """NoteUtil is used for retrieving and manipulating `Notes`.
    It must be configured with a config file.

    Parameters
    ----------
    config_file : str
        The name of the config file that is used to set up this `NoteUtil`.

    Attributes
    ----------
    note_file: str
        The name of the file with notes, likely a text file.
    nu_file: str
        The same name of the file with notes, but with a .nu extension indicating `NoteUtil` modified.
    comments: str
        The prefix of lines that should be ignored in the note file.
    separator: str
        A delimiter used to split `Note` lines into terms and definitions.
    notes : List[`Note`]
        All `Note`s created from the .nu file.
    pairs : List[`Note`]
        All `Note`s that have terms and definitions.
    heading_char : str
        If a `Note` is a heading, its content will start with this character.
    levels : int
        The number of headings.
    level_names : List[str]
        The general name of each group of headings.
    heading_level : dict {str: List[`Note`]}
        Mapped general names of headings to a list of notes that are headings that belong to that name.
    heading_order : List[`Note`]
        Chronological list of notes that are headings.
    warnings : List[str]
        List of all of the warnings that occurred during the `Note` creation process.
    """

    def __init__(self, config_file: str):
        self.notes = []
        self.config_file = config_file
        self.warnings = []
        self._parse_config()
        self._read_config()
        if not os.path.exists(self.nu_file):
            self._parse_notes()
        self._read_notes()
        print("Warnings\n"
              "--------\n"
              "\t{0}\n"
              "--------".format("\n\t".join(self.warnings)))

    @property
    def pairs(self):
        return list(filter(lambda n: n.is_pair(), self.notes))

    @property
    def heading_level(self):
        heading_level = {}
        for level_name in self.level_names:
            heading_level[level_name] = []

        for note in self.heading_order:
            level_name = self.level_names[note.level - 1]
            heading_level[level_name].append(note)
        return heading_level

    @property
    def heading_order(self):
        return list(filter(lambda n: n.is_heading(), self.notes))

    def _parse_config(self):
        with open(self.config_file, mode="r") as f:
            raw_config = ""
            lines = f.readlines()
            for index, line in enumerate(lines):
                # If this line and the last line are blank, that means there are two blank lines.
                if line.startswith("\n") and index != 0 and lines[index - 1].startswith("\n"):
                    raise ExtraLine(index)
                # If this line is a blank line and the previous one was not a comment, there's an unexpected line.
                if line.startswith("\n") and index != 0 and lines[index - 1].strip().startswith(">>>") is False:
                    raise UnexpectedLine(index)

                line = line.strip()

                # Remove any comments and leave only intended lines
                if line.startswith(">>>"):
                    continue

                else:
                    raw_config += line + "\n"

        with open("temp.cfg", mode="w") as f:
            f.write(raw_config)

    def _read_config(self):
        with open("temp.cfg", mode="r") as f:
            lines = readlines(f)

            # Read line by line to get each variable
            self.note_file = next(lines)
            self.nu_file = self.note_file.split(".")[0] + ".nu"
            self.comments = next(lines) or None
            self.separator = next(lines) or None
            self.heading_char = next(lines) or None
            if self.heading_char is not None:
                self.levels = int(next(lines))
                self.level_names = []
                for _ in range(self.levels):
                    self.level_names.append(next(lines))

    def _parse_notes(self):
        with open(self.note_file, mode="r") as f:
            raw_notes = ""
            for line in f.readlines():
                line = line.strip()

                if line.startswith('<span style="text-decoration:underline;">'):
                    line = "__" + line[41:-7] + "__"

                # Check for comments or empty line
                if self.comments is not None:
                    if line.startswith(self.comments):
                        continue
                if line == "":
                    continue

                # Passed, add it to the raw notes
                raw_notes += line + "\n"

        with open(self.nu_file, mode="w") as f:
            f.write(raw_notes)

    def _read_notes(self):
        with open(self.nu_file, mode="r") as f:

            if self.heading_char is not None:
                current_level = 0

            for nindex, line in enumerate(f.readlines()):
                kwargs = {}
                line = line.strip()

                # Heading Detection
                if self.heading_char is not None:
                    if line.startswith(self.heading_char):
                        kwargs["heading_char"] = self.heading_char

                        previous_level = current_level
                        kwargs["level"] = current_level = line.count(self.heading_char, 0, self.levels)
                        if current_level - previous_level > 1:
                            raise HeadingJump(line, previous_level, current_level)
                        kwargs["heading"] = kwargs["heading_char"] * kwargs["level"]
                        line = line[len(kwargs["heading"]):].strip()    # !! Remove heading from line - Affects content
                        kwargs["heading_name"] = line

                        kwargs["begin_nindex"] = nindex
                # End Heading Detection

                # Pair Detection
                if self.separator is not None:
                    if self.separator in line:      # Line is a pair, add additional parameters
                        if len(line.split(self.separator)) > 2:
                            self.warnings.append("Extra Separator - Line content: {0}".format(line))
                            # raise ExtraSeparator(line)

                        kwargs["term"] = line.split(self.separator)[0].strip()
                        if kwargs["term"] in map(lambda n: n.term, self.pairs):
                            self.warnings.append("Duplicate Term - Line content: {0}".format(kwargs["term"]))
                            # raise DuplicateTerm(kwargs["term"])

                        kwargs["definition"] = line.split(self.separator)[1].strip()
                        if kwargs["definition"] == "":
                            self.warnings.append("No Definition - Line content: {0}".format(line))
                            # raise NoDefinition(line)

                        kwargs["separator"] = self.separator
                # End Pair Detection

                note = Note(line, nindex, **kwargs)

                # Add the note to NoteUtil's data structures.
                self.notes.append(note)
                if note.is_heading():
                    self.heading_level[list(self.heading_level.keys())[kwargs["level"] - 1]].append(note)
                    self.heading_order.append(note)

            # Headings are still missing their end_nindex and nindexes:
            # Complete Headings
            headings_list = list(self.heading_level.values())
            for headings in headings_list:
                for i in range(len(headings)):
                    heading = headings[i]
                    level_index = i + 1     # The next heading index at the same level
                    order_index = self.heading_order.index(heading) + 1     # The next heading index in heading order

                    while order_index != len(self.heading_order) and \
                            self.heading_order[order_index].level > heading.level:
                        order_index += 1

                    if level_index == len(headings):
                        level_begin_nindex = len(self.notes)
                    else:
                        level_begin_nindex = headings[level_index].begin_nindex
                    if order_index == len(self.heading_order):
                        order_begin_nindex = len(self.notes)
                    else:
                        order_begin_nindex = self.heading_order[order_index].begin_nindex

                    if level_begin_nindex < order_begin_nindex:
                        end_nindex = level_begin_nindex
                    else:
                        end_nindex = order_begin_nindex

                    heading.end_nindex = end_nindex
                    heading.nindexes = [i for i in range(heading.begin_nindex, heading.end_nindex)]
            # End Complete Headings

    def get(self, **kwargs):
        """Retrieves a `Note` with attributes equal to passed keyword args.

        Parameters
        ----------
        kwargs
            Keys are attribute names and Values are values you are looking for in those attributes.

        Other Parameters
        ----------------
        compare
            If one of the keys of kwargs is `compare`, comparisons will be used with the value of this key.
            The custom compare must accept the parameters: `Note`, **kwargs

        Returns
        -------
        `Note` or None
            If a `Note` is found to have the passed attributes.
            If no `Note` is found.
        """

        if not kwargs:
            return None

        compare = kwargs.pop("compare") if kwargs.get("compare", False) else CompareOptions.EQUALS

        for note in self.notes:
            if compare(note, **kwargs):
                return note
        return None

    def get_list(self, **kwargs):
        """Retrieves all `Note`s with attributes equal to passed keyword args and stores them in a List.

        Parameters
        ----------
        kwargs
            Keys are attribute names and Values are values you are looking for in those attributes.

        Other Parameters
        ----------------
        compare
            If one of the keys of kwargs is `compare`, comparisons will be used with the value of this key.
            The custom compare must accept the parameters: `Note`, **kwargs

        Returns
        -------
        List[`Note`] or None
            If a `Note`s are found to have the passed attributes.
            If no `Note`s are found.
        """

        if not kwargs:
            return None

        notes = []
        compare = kwargs.pop("compare") if kwargs.get("compare", False) else CompareOptions.EQUALS

        for note in self.notes:
            if compare(note, **kwargs):
                notes.append(note)
        return notes if notes else None

    def edit(self, note, content: str):
        """Given a `Note`, edit its content.
        This can have many side effects:
            1. Changes to heading_name.
            2. Changes to whether the `Note` is a pair.
            3. Changes to term, definition, and separator

        Parameters
        ----------
        note : `Note`
            A `Note` that you want to modify.
        content : str
            The new content that the `Note` should have.

        Returns
        -------
        None
        """

        note.content = content
        note.heading_name = content

        if self.separator is not None:
            if self.separator in content:
                if len(content.split(self.separator)) > 2:
                    raise ExtraSeparator(content)

                term = content.split(self.separator)[0].strip()
                if term in map(lambda n: n.term, self.pairs):
                    raise DuplicateTerm(term)

                definition = content.split(self.separator)[1].strip()
                if definition == "":
                    raise NoDefinition(content)
            else:
                note.term = None
                note.definition = None
                note.separator = None

        self.notes[note.nindex] = note

    def reformat(self):
        """Writes all of the `Note`s back into what they were when they were being parsed into a .nu file.

        If any changes to the `Note`s were made, they will be written here as well.

        Returns
        -------
        None
        """

        raw_notes = "\n".join(list(map(lambda n: repr(n), self.notes)))
        with open(self.nu_file, mode="w") as f:
            f.write(raw_notes)


















