from .notes import Note


def readlines(f):
    lines = f.read().split("\n")
    for line in lines:
        yield line


class NoteUtil:
    def __init__(self, config_file: str):
        self.notes_list = []
        self.parse_config(config_file)
        self.read_config()
        self.parse_notes()
        self.read_notes()

    def parse_config(self, config_file):
        with open(config_file, mode="r") as f:
            raw_config = ""
            for line in f.readlines():
                line = line.strip()
                if line.startswith("#"):
                    continue
                else:
                    raw_config += line + "\n"

        with open("temp.cfg", mode="w") as f:
            f.write(raw_config)

    def read_config(self):
        with open("temp.cfg", mode="r") as f:
            lines = readlines(f)
            self.note_file = next(lines)
            self.nu_file = self.note_file.split(".")[0] + ".nu"
            self.comments = next(lines) or None
            self.separator = next(lines) or None

    def parse_notes(self):
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

                # Passed, add it to the raw notes_list
                raw_notes += line + "\n"

        with open(self.nu_file, mode="w") as f:
            f.write(raw_notes)

    def read_notes(self):
        with open(self.nu_file, mode="r") as f:
            for nindex, line in enumerate(f.readlines()):
                kwargs = {}
                line = line.strip()

                if self.separator is not None:
                    if self.separator in line:      # Line is a pair
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














