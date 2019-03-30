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
    string = ("Content: {0} \t\t Note Index: {1} \t\t Term: {2} \t\t Definition: {3} \t\t Separator: {4}"
              .format(note.content, note.nindex, note.term, note.definition, note.separator))
    return string


def test_note_list(note_list):
    return str(list(map(test_note, note_list)))


noteutil = NoteUtil("basic_config.txt")
print(test_noteutil(noteutil))
print(test_note(noteutil.get(content="Line 1", nindex=0)))

print(test_note_list(noteutil.get_list(content="Line 5", compare=is_equal)))
print(test_note_list(noteutil.get_list(content="Pair", compare=is_in)))
print(test_note_list(noteutil.get_list(definition="pair", compare=is_similar)))
print(test_note_list(noteutil.get_list(content="line", compare=is_in_similar)))
print(test_note_list(noteutil.get_list(content="Line", definition="pair", compare=is_in)))

