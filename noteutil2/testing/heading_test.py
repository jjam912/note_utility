from noteutil.noteutil2.noteutil import NoteUtil
from noteutil.noteutil2.comparisons import is_equal, is_in, is_similar, is_in_similar


def test_noteutil(noteutil):
    string = "NoteUtil" + "\n"
    string += "--------" + "\n"
    string += "Note File: " + str(noteutil.note_file) + "\n"
    string += "NoteUtil File: " + str(noteutil.nu_file) + "\n"
    string += "Comments: " + str(noteutil.comments) + "\n"
    string += "Separator: " + str(noteutil.separator) + "\n"
    string += "Notes List" + "\n"
    string += "----------" + "\n"
    for note in noteutil.notes_list:
        string += "\t" + test_note(note) + "\n"
    string += "----------" + "\n"
    string += "Pairs List Length: " + str(len(noteutil.pairs_list)) + "\n"
    return string


def test_note(note):
    string = "Note: \t"
    string += "Content: {!s:<20}\t\t".format(note.content[:20])
    string += "Note Index: {!s:<5}\t\t".format(note.nindex)
    string += "Term: {!s:<10}\t\t".format(note.term[:10] if note.term else None)
    string += "Definition: {!s:<10}\t\t".format(note.definition[:10] if note.definition else None)
    string += "Separator: {0}\t\t".format(note.separator)
    return string


def test_note_list(note_list):
    return "\t\t".join((list(map(test_note, note_list))))


noteutil = NoteUtil("heading_config.txt")
print(test_noteutil(noteutil))
