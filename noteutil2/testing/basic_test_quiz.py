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

    return string


def test_note(note):
    string = "Note: \t"
    string += "Content: {!s:<20}\t\t".format(note.content[:20])
    string += "Note Index: {!s:<5}\t\t".format(note.nindex)
    string += "Term: {!s:<10}\t\t".format(note.term[:10] if note.term else None)
    string += "Definition: {!s:<10}\t\t".format(note.definition[:10] if note.definition is not None else None)
    string += "Separator: {0}\t\t".format(note.separator)
    return string


def test_note_list(note_list):
    return "\t\n".join((list(map(test_note, note_list))))


if os.path.exists("basic_notes.nu"):
    os.remove("basic_notes.nu")
noteutil = NoteUtil("basic_config.txt")
quiz = Quiz(noteutil)
print(test_noteutil(noteutil))
print(test_quiz(quiz))

print("Generate all in order:")
print("----------------------")
quiz.randomize = False
for note in quiz.generate():
    print("\t" + test_note(note) + "")
print("----------------------")

print("Generate all randomly:")
print("----------------------")
quiz.randomize = True
for note in quiz.generate():
    print("\t" + test_note(note) + "")
print("----------------------")

quiz.randomize = False
pairs = quiz.generate()
print("Add first two to correct:")
quiz.append(next(pairs), correct=True)
quiz.append(next(pairs), correct=True)

print("Add next two to incorrect:")
quiz.append(next(pairs), correct=False)
quiz.append(next(pairs), correct=False)

print(test_quiz(quiz))
print("Last note: " + noteutil.notes[quiz.last_nindex].term)
print("----------")

print("Clear quiz:")
quiz.clear()
print(test_quiz(quiz))
print("-----------")

quiz.randomize = True
pairs = quiz.generate()
print("Add random two to correct:")
quiz.append(next(pairs), correct=True)
quiz.append(next(pairs), correct=True)

print("Add random two to incorrect:")
quiz.append(next(pairs), correct=False)
quiz.append(next(pairs), correct=False)
print(test_quiz(quiz))
print("Last note: " + noteutil.notes[quiz.last_nindex].term)

print("Clear quiz:")
quiz.clear()
print(test_quiz(quiz))

print("Generate notes into list:")
print("Random: False")
quiz.randomize = False
print(test_note_list(list(quiz.generate())))
print("Random: True")
quiz.randomize = True
print(test_note_list(list(quiz.generate())))

