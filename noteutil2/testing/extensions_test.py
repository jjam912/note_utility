from noteutil2.noteutil import NoteUtil
from noteutil2.comparisons import CompareOptions
from noteutil2.errors import NoteError
import os


def test_noteutil(noteutil):
    string = "NoteUtil" + "\n"
    string += "--------" + "\n"
    string += "Note File: " + str(noteutil.note_file) + "\n"
    string += "NoteUtil File: " + str(noteutil.nu_file) + "\n"
    string += "Comments: " + str(noteutil.comments) + "\n"
    string += "Separator: " + str(noteutil.separator) + "\n"
    string += "Notes List" + "\n"
    string += "----------" + "\n"
    for note in noteutil.notes:
        string += "\t" + test_note(note) + "\n"
    string += "----------" + "\n"

    string += "Pairs List Terms" + "\n"
    string += "----------------" + "\n"
    for pair in noteutil.pairs:
        string += "\t" + pair.term + "\n"
    string += "--------------------------" + "\n"
    string += "Extension Names and Bounds" + "\n"
    string += "--------------------------" + "\n"
    for name, bounds in zip(noteutil.extension_names, noteutil.extension_bounds):
        string += "\t" + name + ": " + bounds[0] + " " + bounds[1] + "\n"

    return string


def test_note(note):
    string = "Note: \t"
    string += "Content: {!s:<20}\t\t".format(note.content[:20])
    string += "Note Index: {!s:<5}\t\t".format(note.nindex)
    string += "Term: {!s:<10}\t\t".format(note.term[:10] if note.term else None)
    string += "Definition: {!s:<10}\t\t".format(note.definition[:10] if note.definition else None)
    string += "Separator: {0}\t\t".format(note.separator) + "\n"
    if note.has_extensions():
        string += "\t----------" + "\n"
        string += "\tExtensions" + "\n"
        string += "\t----------" + "\n"
        for ext in note.extensions:
            string += "\t\t" + test_extension(ext) + "\n"
    string += "\tRaw Content: {0}".format(note.rcontent)
    return string


def test_extension(ext):
    string = "Extension: \t"
    string += "Content: {0}\t\t".format(ext.content)
    string += "Name: {!s:<10}\t\t".format(ext.name[:10])
    string += "Left Bound: {!s:<10}\t\t".format(ext.lbound[:10])
    string += "Right Bound: {!s:<10}\t\t".format(ext.rbound[:10])
    return string


def test_note_list(note_list):
    print()
    return "\t\n".join((list(map(test_note, note_list))))


if os.path.exists("extensions_notes.nu"):
    os.remove("extensions_notes.nu")
noteutil = NoteUtil("extensions_config.txt")
print(test_noteutil(noteutil))
