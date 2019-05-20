from noteutil.noteutil import NoteUtil
from noteutil.comparisons import CompareOptions
from noteutil.errors import NoteError
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

    string += "Heading Character: " + noteutil.heading_char + "\n"
    string += "Levels: " + str(noteutil.levels) + "\n"
    string += "Heading Level" + "\n"
    string += "--------" + "\n"
    for gname, anames in noteutil.heading_level.items():     # General name, Actual names
        string += "\t" + gname + ": " + str(list(map(lambda x: x.heading_name, anames))) + "\n"
    string += "--------" + "\n"
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


def test_note_list(note_list):
    print()
    return "\t\n".join((list(map(test_note, note_list))))


if os.path.exists("category_notes.nu"):
    os.remove("category_notes.nu")
noteutil = NoteUtil("category_config.txt")
print(test_noteutil(noteutil))
