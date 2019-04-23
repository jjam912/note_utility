from noteutil2.noteutil import NoteUtil
from noteutil2.comparisons import CompareOptions
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
    string += "----------------" + "\n"

    return string


def test_note(note):
    string = "Note: \t"
    string += "Content: {!s:<20}\t\t".format(note.content[:20])
    string += "Note Index: {!s:<5}\t\t".format(note.nindex)
    string += "Term: {!s:<10}\t\t".format(note.term[:10] if note.term else None)
    string += "Definition: {!s:<10}\t\t".format(note.definition[:10] if note.definition else None)
    string += "Separator: {!s:<5}\t\t".format(note.separator)
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


def before_after_edit(note, content):
    print("Before:\n"
          "-------\n" + test_note(note) + "\n" +
          "-------")
    noteutil.edit(note, content)
    print("After:\n"
          "------\n" + test_note(note) + "\n" +
          "------")


if os.path.exists("edit_notes.nu"):
    os.remove("edit_notes.nu")
noteutil = NoteUtil("edit_config.txt")
print(test_noteutil(noteutil))

n1 = noteutil.get(nindex=0)
before_after_edit(n1, "Wumbo")
n2 = noteutil.get(nindex=1)
before_after_edit(n2, "Eung Eung %% APink %%")

print(test_noteutil(noteutil))

noteutil.reformat()

print(noteutil.get(extension_names="Cool beans", compare=CompareOptions.IN))


