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
    return string


def test_note_list(note_list):
    return "\t\t".join((list(map(test_note, note_list))))


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

print(test_noteutil(noteutil))

noteutil.reformat()
