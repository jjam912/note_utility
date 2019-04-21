from noteutil2.noteutil import NoteUtil
from noteutil2.quiz import Leitner
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


def test_leitner(leitner):
    string = "Leitner" + "\n"
    string += "------" + "\n"

    string += "Last Note Index: " + str(leitner.last_nindex) + "\n"
    string += "Times: " + str(leitner.times) + "\n"
    string += "Session: " + str(leitner.session) + "\n"

    string += "Boxes" + "\n"
    string += "-----" + "\n"
    for box_number, pairs in leitner.boxes.items():
        string += "\t" + str(box_number) + "\n\t\t"
        string += "\n\t\t".join(list(map(lambda p: p.term, pairs))) + "\n"
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
if os.path.exists("basic_notes.lt"):
    os.remove("basic_notes.lt")
noteutil = NoteUtil("basic_config.txt")
leitner = Leitner(noteutil)
print(test_noteutil(noteutil))
print(test_leitner(leitner))

import random
pairs = noteutil.pairs
for _ in range(29):
    for pair in leitner.generate():
        if random.choice([0, 1]):
            leitner.correct(pair)
        else:
            leitner.incorrect(pair)

    print(test_leitner(leitner))

noteutil2 = NoteUtil("basic_config.txt")
for pair in noteutil2.pairs[:2]:
    noteutil2.edit(pair, content="Yeet ayy" + pair.content)
print(test_noteutil(noteutil2))
leitner.refresh(noteutil2)
print(test_leitner(leitner))
leitner.reset()
print(test_leitner(leitner))

for _ in range(29):
    for pair in leitner.generate():
        if random.choice([0, 1]):
            leitner.correct(pair)
        else:
            leitner.incorrect(pair)

print(test_leitner(leitner))
leitner.save()
with open("basic_notes.lt", mode="r") as f:
    print(f.read())
leitner.load()
print(test_leitner(leitner))

leitner.refresh(noteutil)
leitner.load()
print(test_leitner(leitner))

