from noteutil2.noteutil import NoteUtil
from noteutil2.quiz import Quiz
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

    string += "Heading Character: " + noteutil.heading_char + "\n"
    string += "Levels: " + str(noteutil.levels) + "\n"
    string += "Heading Level" + "\n"
    string += "--------" + "\n"
    for gname, anames in noteutil.heading_level.items():     # General name, Actual names
        string += "\t" + gname + ": " + str(list(map(lambda x: x.heading_name, anames))) + "\n"
    string += "--------" + "\n"
    string += "Heading Names" + "\n"
    string += "-------------\n"
    for i, heading_name in enumerate(noteutil.heading_names):
        string += "\t" + str(i+1) + ". " + heading_name + "\n"
    string += "Heading Order" + "\n"
    string += "-------------" + "\n"
    for note in noteutil.heading_order:
        string += "\tLevel " + str(note.level) + ": \t" + note.heading_name + "\n"
    string += "-------------" + "\n"
    return string


def test_quiz(quiz):
    string = "Quiz" + "\n"
    string += "----" + "\n"

    string += "Last Note Index: " + str(quiz.last_nindex) + "\n"
    string += "Randomize: " + str(quiz.randomize) + "\n"

    string += "Correct Set:\n"
    string += "----------\n"
    for pair in quiz.correct:
        string += "\t" + pair.term + "\n"
    string += "----------\n"

    string += "Incorrect Set:\n"
    string += "----------\n"
    for pair in quiz.incorrect:
        string += "\t" + pair.term + "\n"
    string += "----------\n"

    string += "Generate all in order:" + "\n"
    string += "----------------------" + "\n"
    quiz.randomize = False
    for note in quiz.generate():
        string += "\t" + test_note(note) + "\n"
    string += "----------------------" + "\n"

    string += "Generate all randomly:" + "\n"
    string += "----------------------" + "\n"
    quiz.randomize = True
    for note in quiz.generate():
        string += "\t" + test_note(note) + "" + "\n"
    string += "----------------------" + "\n"

    return string


def test_note(note):
    string = "Note: \t"
    string += "Content: {!s:<20}\t\t".format(note.content[:20])
    string += "Note Index: {!s:<5}\t\t".format(note.nindex)
    string += "Term: {!s:<10}\t\t".format(note.term[:10] if note.term else None)
    string += "Definition: {!s:<10}\t\t".format(note.definition[:10] if note.definition else None)
    string += "Separator: {!s:<5}\t\t".format(note.separator)
    string += "Heading Character: {!s:<5}\t\t".format(note.heading_char)
    string += "Level: {!s:<3}\t\t".format(note.level)
    string += "Heading: {!s:<10}\t\t".format(note.heading)
    string += "Heading Name: {!s:<10}\t\t".format(note.heading_name[:10] if note.heading_name else None)
    string += "Beginning Note Index: {!s:<5}\t\t".format(note.begin_nindex)
    string += "Ending Note Index: {!s:<5}\t\t".format(note.end_nindex)
    if note.nindexes:
        string += "Notes Indexes: " + str(note.nindexes)
    else:
        string += "Notes Indexes: None"
    return string


def test_note_list(note_list) -> str:
    print()
    return "\t\n".join((list(map(test_note, note_list))))


if os.path.exists("heading_notes.nu"):
    os.remove("heading_notes.nu")
noteutil = NoteUtil("heading_config.txt")
quiz = Quiz(noteutil)
print(test_noteutil(noteutil))
print(test_quiz(quiz))

print("Change heading to 2. Basic Structures: Sets, Functions, Sequences, Sums, and Matrices")
quiz.select_heading(noteutil.get(heading_name="2. Basic Structures:", compare=CompareOptions.SIN))
print(test_quiz(quiz))

print("Change back to all pairs")
quiz.select_heading(None)
print(test_quiz(quiz))



