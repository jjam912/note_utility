from .notes import Note, Extension
from .comparisons import CompareOptions
from .errors import *
import os.path
from typing import List, Dict, Generator, Union, Tuple


def readlines(f) -> Generator[str, None, None]:
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
    """NoteUtil is used for retrieving and manipulating Notes.
    It must be configured with a config file.

    Parameters
    ----------
    config_file : str
        The name of the config file that is used to set up this NoteUtil.

    Attributes
    ----------
    note_file: str
        The name of the file with notes, likely a text file.
    nu_file: str
        The same name of the file with notes, but with a .nu extension indicating NoteUtil modified.
    comments: str
        The prefix of lines that should be ignored in the note file.
    separator: str
        A delimiter used to split Note lines into pairs (terms and definitions).
    notes : List[Note]
        All Notes created from the .nu file.
    heading_char : str
        If a Note is a heading, its content will start with this character.
    levels : int
        The number of headings.
    level_names : List[str]
        The general name of each group of headings.
    heading_names : List[str]
        The list of all heading names in chronological order.
    heading_level : Dict[str, List[Note]]
        Mapped general names of headings to a list of notes that are headings that belong to that name.
    heading_order : List[Note]
        Chronological list of notes that are headings.
    category_names : List[str]
        The list of all category names in chronological order.
    category_prefixes : List[str]
        The list of all category prefixes in chronological order.
        zip(category_names, category_prefixes) gives correctly corresponding names and prefixes.
    categories : Dict[str, List[int]]
        Mapped category names to list of Notes.
    extension_names : List[str]
        List of all generic names of the extensions.
    extension_bounds : List[Tuple[str, str]]
        List of all (left bound, right bound) tuples that correspond to the extension names.
        zip(extension_names, extension_bounds) gives correctly corresponding names and bounds.
    extensions : List[Note]
        All Notes that have extensions.
    pairs : List[Note]
        All Notes that have terms and definitions.
    warnings : List[str]
        List of all of the warnings that occurred during the Note creation process.
    errors : List[str]
        List of all of the errors that occurred during the Note creation process.

    Raises
    ------
    NoteError
        If there were any severe problems during the Note creation process.
    """

    def __init__(self, config_file: str, refresh: bool = False):
        self.notes = []
        self.config_file = config_file
        self.warnings = []
        self.errors = []
        self._parse_config()
        self._read_config()
        if not os.path.exists(self.nu_file) or refresh:
            self._parse_notes()
        self._read_notes()

        if self.warnings:
            print("Warnings for {0}\n"
                  "--------\n"
                  "\t{1}\n"
                  "--------".format(self.note_file, "\n\t".join(self.warnings)))
        if self.errors:
            raise NoteError("Errors\n"
                            "------\n"
                            "\t{0}\n"
                            "------".format("\n\t".join(self.errors)))

    @property
    def pairs(self) -> List[Note]:
        return list(filter(lambda n: n.is_pair(), self.notes))

    @property
    def heading_names(self) -> List[str]:
        return list(map(lambda n: n.heading_name, self.heading_order))

    @property
    def heading_level(self) -> Dict[str, List[Note]]:
        heading_level = {}
        for level_name in self.level_names:
            heading_level[level_name] = []

        for note in self.heading_order:
            level_name = self.level_names[note.level - 1]
            heading_level[level_name].append(note)
        return heading_level

    @property
    def heading_order(self) -> List[Note]:
        return list(filter(lambda n: n.is_heading(), self.notes))

    @property
    def categories(self) -> Dict[str, List[Note]]:
        categories = {name: [] for name in self.category_names}
        for note in self.notes:
            for category_name in note.category_names:
                categories[category_name].append(note)
        return categories

    @property
    def extensions(self) -> List[Note]:
        return list(filter(lambda n: n.has_extensions(), self.notes))

    def _parse_config(self) -> None:
        """Strips the file of white space, empty lines, and comments.
        Detects unusual spacing and writes contents into a temporary config file.
        """

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

    def _read_config(self) -> None:
        """Parses the config file into NoteUtil attributes."""

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
            else:
                next(lines)
                next(lines)

            category_number = next(lines) or None
            if category_number:
                self.category_names = list()
                self.category_prefixes = list()
                for _ in range(int(category_number)):
                    self.category_names.append(next(lines))
                for _ in range(int(category_number)):
                    self.category_prefixes.append(next(lines))
            else:
                self.category_names = []
                self.category_prefixes = []
                next(lines)
                next(lines)

            extension_number = next(lines) or None
            if extension_number:
                self.extension_names = list()
                self.extension_bounds = list()
                for _ in range(int(extension_number)):
                    self.extension_names.append(next(lines))
                for _ in range(int(extension_number)):
                    self.extension_bounds.append(tuple(next(lines).split()))
            else:
                self.extension_names = []
                self.extension_bounds = []
                next(lines)
                next(lines)

    def _parse_notes(self) -> None:
        """Strips the note file of whitespace, empty lines, and comments.
        Removes the underline heading generated from Docs to Markdown and writes content to the .nu file.
        """

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

    def _read_notes(self) -> None:
        """Parses the newly written .nu file and creates Notes in the order of Heading, Extensions, Pairs, and Notes.
        Adds all of the notes to self.notes.
        """

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
                            self.errors.append("Heading Jump - Line content: {0}".format(line))
                            # raise HeadingJump(line, previous_level, current_level)
                        kwargs["heading"] = kwargs["heading_char"] * kwargs["level"]
                        line = line[len(kwargs["heading"]):].strip()    # !! Remove heading from line - Affects content
                        kwargs["heading_name"] = line

                        kwargs["begin_nindex"] = nindex
                # End Heading Detection

                # Category Detection
                if self.category_names is not None and self.category_prefixes is not None:
                    kwargs["category_names"] = []
                    kwargs["category_prefixes"] = []
                    for name, prefix in zip(self.category_names, self.category_prefixes):
                        if line.startswith(prefix):
                            kwargs["category_names"].append(name)
                            kwargs["category_prefixes"].append(prefix)
                            line = line[len(prefix):].strip()       # !! Remove prefix from line - Affects content
                    # Since content may have been modified, fix up heading_name
                    if kwargs.get("heading_name", False):
                        kwargs["heading_name"] = line
                # End Category Detection

                # Extension Detection
                if self.extension_names is not None and self.extension_bounds is not None:
                    kwargs["extensions"] = []
                    kwargs["extension_names"] = []
                    for name, bounds in zip(self.extension_names, self.extension_bounds):
                        lbound, rbound = bounds
                        while lbound in line:
                            if rbound in line:
                                lindex = line.index(lbound) + len(lbound)
                                rindex = line.index(rbound, lindex)
                                kwargs["extensions"].append(
                                    Extension(line[lindex:rindex].strip(), name, lbound, rbound))
                                if name not in kwargs["extension_names"]:
                                    kwargs["extension_names"].append(name)

                                line = line[:lindex - len(lbound)].strip() + " " + line[rindex + len(rbound):].strip()
                                line = line.strip()
                            else:
                                self.warnings.append("Missing Bound - Line content: {0}".format(line))
                                break
                                # raise MissingBound(line, lbound, rbound)

                # End Extension Detection

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

            # Headings are still missing their end_nindex:
            # Complete Headings
            if self.heading_char is not None:
                headings_list = list(self.heading_level.values())
                for headings in headings_list:
                    for i in range(len(headings)):
                        heading = headings[i]
                        level_index = i + 1     # The next heading index at the same level
                        order_index = self.heading_order.index(heading) + 1    # The next heading index in heading order

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
            # End Complete Headings

    def get(self, **kwargs) -> Union[None, Note]:
        """Retrieves a Note with attributes equal to passed keyword args.

        Parameters
        ----------
        kwargs
            Keys are attribute names and Values are values you are looking for in those attributes.

        Other Parameters
        ----------------
        compare
            If one of the keys of kwargs is compare, comparisons will be used with the value of this key.
            The custom compare must accept the parameters: Note, **kwargs

        Returns
        -------
        Note or None
            If a Note is found to have the passed attributes.
            If no Note is found.
        """

        if not kwargs:
            return None

        compare = kwargs.pop("compare") if kwargs.get("compare", False) else CompareOptions.EQUALS

        for note in self.notes:
            if compare(note, **kwargs):
                return note
        return None

    def get_list(self, **kwargs) -> Union[None, List[Note]]:
        """Retrieves all Notes with attributes equal to passed keyword args and stores them in a List.

        Parameters
        ----------
        kwargs
            Keys are attribute names and Values are values you are looking for in those attributes.

        Other Parameters
        ----------------
        compare
            If one of the keys of kwargs is compare, comparisons will be used with the value of this key.
            The custom compare must accept the parameters: Note, **kwargs

        Returns
        -------
        List[Note] or None
            If a Notes are found to have the passed attributes.
            If no Notes are found.
        """

        if not kwargs:
            return None

        notes = []
        compare = kwargs.pop("compare") if kwargs.get("compare", False) else CompareOptions.EQUALS

        for note in self.notes:
            if compare(note, **kwargs):
                notes.append(note)
        return notes if notes else None

    def edit(self, note: Note, content: str, override: bool = False) -> None:
        """Given a Note, edit its content.
        This can have many side effects:
            1. Changes to heading_name.
            2. Changes to categories.
            2. Changes to extensions.
            3. Changes to whether the Note is a pair.
            4. Changes to term, definition, and separator

        Parameters
        ----------
        note : Note
            A Note that you want to modify.
        content : str
            The new content that the Note should have.
        override : bool
            Whether to override the warning when editing the content.

        Returns
        -------
        None

        Raises
        ------
        MissingBound
        ExtraSeparator
        DuplicateTerm
        NoDefinition
        """

        if self.category_names is not None and self.category_prefixes is not None:
            note.category_names = []
            note.category_prefixes = []
            for name, prefix in zip(self.category_names, self.category_prefixes):
                if content.startswith(prefix):
                    note.category_names.append(name)
                    note.category_prefixes.append(prefix)
                    content = content[len(prefix):].strip()

        if self.extension_names is not None and self.extension_bounds is not None:
            note.extensions = []
            note.extension_names = []
            for name, bounds in zip(self.extension_names, self.extension_bounds):
                lbound, rbound = bounds
                while lbound in content:
                    if rbound in content:
                        lindex = content.index(lbound) + len(lbound)
                        rindex = content.index(rbound, lindex)
                        note.extensions.append(Extension(content[lindex:rindex].strip(), name, lbound, rbound))
                        note.extension_names.append(name)

                        content = content[:lindex - len(lbound)].strip() + " " + content[rindex + len(rbound):].strip()
                        content = content.strip()
                    else:
                        if not override:
                            raise MissingBound(content, lbound, rbound)

        if self.separator is not None:
            if self.separator in content:
                if len(content.split(self.separator)) > 2:
                    if not override:
                        raise ExtraSeparator(content)

                term = content.split(self.separator)[0].strip()
                if note.term != term and term in map(lambda n: n.term, self.pairs):
                    if not override:
                        raise DuplicateTerm(term)

                definition = content.split(self.separator)[1].strip()
                if definition == "":
                    if not override:
                        raise NoDefinition(content)
                note.term = term
                note.definition = definition
                note.separator = self.separator
            else:
                note.term = None
                note.definition = None
                note.separator = None

        note.content = content
        if note.is_heading():
            note.heading_name = content

        self.notes[note.nindex] = note

    def save(self) -> None:
        """Writes all of the Notes back into what they were when they were being parsed into a .nu file.

        If any changes to the Notes were made, they will be written here as well.

        Returns
        -------
        None
        """

        raw_notes = "\n".join(list(map(lambda n: n.rcontent, self.notes)))
        with open(self.nu_file, mode="w") as f:
            f.write(raw_notes)

    def load(self) -> None:
        """Re-parses the .nu file, reverting any changes that could have been made to NoteUtil during use.

        Returns
        -------
        None
        """

        self.__init__(self.config_file)

    def refresh(self) -> None:
        """Re-initializes the NoteUtil from the note file instead of the .nu file.
        This is used to match a new or updated note file.

        Returns
        -------
        None
        """

        self.__init__(self.config_file, refresh=True)
















