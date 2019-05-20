from noteutil.noteutil import NoteUtil
from noteutil.quiz import Quiz
from noteutil.comparisons import CompareOptions
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
    string += "Category Names and Prefixes" + "\n"
    string += "---------------------------" + "\n"
    for name, prefix in zip(noteutil.category_names, noteutil.category_prefixes):
        string += "\t" + name + ": " + prefix + "\n"
    string += "----------" + "\n"
    string += "Categories" + "\n"
    string += "----------" + "\n"
    for name, note_list in noteutil.categories.items():
        string += "\t" + name + ":" + "\n"
        for note in note_list:
            string += "\t\t" + note.content + "\n"
    string += "--------------------------" + "\n"
    string += "Extension Names and Bounds" + "\n"
    string += "--------------------------" + "\n"
    for name, bounds in zip(noteutil.extension_names, noteutil.extension_bounds):
        string += "\t" + name + ": " + bounds[0] + " " + bounds[1] + "\n"
    return string


def test_quiz(quiz):
    string = "Quiz" + "\n"
    string += "----" + "\n"

    string += "Last Note Index: " + str(quiz.last_nindex) + "\n"

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
    for note in quiz.generate(randomize=False):
        string += "\t" + test_note(note) + "\n"
    string += "----------------------" + "\n"

    string += "Generate all randomly:" + "\n"
    string += "----------------------" + "\n"
    for note in quiz.generate(randomize=True):
        string += "\t" + test_note(note) + "" + "\n"
    string += "----------------------" + "\n"

    return string


def test_quiz_save(noteutil, quiz):
    string = ""
    string += "=====================" + "\n"
    string += "Testing Save and Load" + "\n"
    string += "=====================" + "\n"

    string += "Add 5 random pairs to correct and incorrect" + "\n"
    for note in list(quiz.generate(randomize=True))[:5]:
        quiz.append(note, correct=True)
    # Some Notes might be taken away from the correct set when other Notes are added to the incorrect set

    for note in list(quiz.generate(randomize=True))[:5]:
        quiz.append(note, correct=False)

    string += "Correct Set:" + "\n"
    string += "------------" + "\n"
    string += "\t" + "\n\t".join(map(lambda p: p.content, quiz.correct)) + "\n"
    string += "------------" + "\n"

    string += "Incorrect Set:" + "\n"
    string += "--------------" + "\n"
    string += "\t" + "\n\t".join(map(lambda p: p.content, quiz.incorrect)) + "\n"
    string += "--------------" + "\n"

    quiz.save()
    with open(quiz.qz_file, mode="r") as f:
        string += f.read() + "\n"

    # Edit all incorrect terms, therefore no incorrect terms should load.
    for note in quiz.incorrect:
        noteutil.edit(note, content=note.content + " Yee")
    quiz.clear()

    quiz.load()

    string += test_quiz(quiz) + "\n"
    return string


def test_quiz_refresh(noteutil, quiz):
    string = ""
    string += "===============" + "\n"
    string += "Testing Refresh" + "\n"
    string += "===============" + "\n"

    string += "Add 5 random pairs to correct and incorrect" + "\n"
    for note in list(quiz.generate(randomize=True))[:5]:
        quiz.append(note, correct=True)
    # Some Notes might be taken away from the correct set when other Notes are added to the incorrect set

    for note in list(quiz.generate(randomize=True))[:5]:
        quiz.append(note, correct=False)

    string += "Correct Set:" + "\n"
    string += "------------" + "\n"
    string += "\t" + "\n\t".join(map(lambda p: p.content, quiz.correct)) + "\n"
    string += "------------" + "\n"

    string += "Incorrect Set:" + "\n"
    string += "--------------" + "\n"
    string += "\t" + "\n\t".join(map(lambda p: p.content, quiz.incorrect)) + "\n"
    string += "--------------" + "\n"

    # Edit all incorrect terms, therefore no incorrect terms should remain after refreshing.
    for note in quiz.incorrect:
        noteutil.edit(note, content=note.content + " Yeet")
    # Create a fresh new NoteUtil so that the new incorrect terms aren't found in the original
    noteutil2 = NoteUtil("heading_config.txt")

    string += "=======" + "\n"
    string += "Refresh" + "\n"
    string += "=======" + "\n"
    quiz.refresh(noteutil2)

    string += test_quiz(quiz) + "\n"
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
    string += "Ending Note Index: {!s:<5}\t\t".format(note.end_nindex) + "\n"
    if note.has_categories():
        string += "\t\t|| "
        for category_name in note.category_names:
            string += category_name + " || "
        string += "\n"
    if note.has_extensions():
        for ext in note.extensions:
            string += "\t\t" + test_extension(ext) + "\n"
    string += "\t\tRaw Content: {0}".format(note.rcontent)
    return string


def test_extension(ext):
    string = "Extension:\t"
    string += "Content: {0}\t\t".format(ext.content)
    string += "Name: {!s:<10}\t\t".format(ext.name[:10])
    string += "Left Bound: {!s:<10}\t\t".format(ext.lbound[:10])
    string += "Right Bound: {!s:<10}\t\t".format(ext.rbound[:10])
    return string


def test_note_list(note_list) -> str:
    print()
    return "\t\n".join((list(map(test_note, note_list))))


if os.path.exists("category_notes.nu"):
    os.remove("category_notes.nu")
if os.path.exists("category_notes.qz"):
    os.remove("category_notes.qz")

noteutil = NoteUtil("category_config.txt")
quiz = Quiz(noteutil)
print(test_noteutil(noteutil))
print(test_quiz(quiz))

print("Change heading to APink")
quiz.select_pairs("Exclamation")
print(test_quiz(quiz))

# print("Change back to all pairs")
# quiz.select_pairs(None)
# print(test_quiz(quiz))
#
# print(test_quiz_save(noteutil, quiz))
# print(test_noteutil(noteutil))
# quiz.reset()
# print(test_quiz_refresh(noteutil, quiz))
# print(test_noteutil(noteutil))
#
# print()
#
# pairs = quiz.generate(randomize=True)
# print("Add random five to correct")
# for _ in range(5):
#     quiz.append(next(pairs), correct=True)
# print(test_quiz(quiz))
# print("Generate unmarked terms and print them out in chronological order:")
# quiz.select_pairs("unmarked")
# pairs = quiz.generate(randomize=False)
# print(test_note_list(list(pairs)))
# print("Generate unmarked terms and print them out in random order:")
# pairs = quiz.generate(randomize=True)
# print(test_note_list(list(pairs)))
#
#
#
#
#

