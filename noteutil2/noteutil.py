from .notes import Note


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
        yield line


class NoteUtil:
    """NoteUtil is used for retrieving and manipulating `Notes`.
    It must be configured with a config file

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
    notes_list : List[`Note`]
        All `Note`s created from the .nu file.
    """

    def __init__(self, config_file: str):
        self.notes_list = []
        self.config_file = config_file
        self._parse_config()
        self._read_config()
        self._parse_notes()
        self._read_notes()

    def _parse_config(self):
        with open(self.config_file, mode="r") as f:
            raw_config = ""
            for line in f.readlines():
                line = line.strip()

                # Remove any comments and leave only intended lines
                if line.startswith("#"):
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

    def _parse_notes(self):
        with open(self.note_file, mode="r") as f:
            raw_notes = ""
            for line in f.readlines():
                line = line.strip()

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
            for nindex, line in enumerate(f.readlines()):
                kwargs = {}
                line = line.strip()

                if self.separator is not None:
                    if self.separator in line:      # Line is a pair, add additional parameters
                        kwargs["term"] = line.split(self.separator)[0].strip()
                        kwargs["definition"] = line.split(self.separator)[1].strip()
                        kwargs["separator"] = self.separator
                        note = Note(line, nindex, **kwargs)
                    else:
                        note = Note(line, nindex)
                else:
                    note = Note(line, nindex)

                self.notes_list.append(note)

    def __str__(self):
        string = "NoteUtil" + "\n"
        string += "--------" + "\n"
        string += "Note File: " + str(self.note_file) + "\n"
        string += "NoteUtil File: " + str(self.nu_file) + "\n"
        string += "Comments: " + str(self.comments) + "\n"
        string += "Separator: " + str(self.separator) + "\n"
        string += "Notes List" + "\n"
        string += "----------" + "\n"
        for note in self.notes_list:
            string += "\t" + str(note) + "\n"
        string += "----------" + "\n"
        return string














