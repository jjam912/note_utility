from noteutil.noteutil2.noteutil import NoteUtil
from noteutil.noteutil2.comparisons import is_equal, is_in, is_similar, is_in_similar


noteutil = NoteUtil("basic_config.txt")
print(noteutil)
print(noteutil.get(content="Line 1", nindex=0))
print(list(map(str, noteutil.get_list(content="Line 5", compare=is_equal))))
print(list(map(str, noteutil.get_list(content="Pair", compare=is_in))))
print(list(map(str, noteutil.get_list(definition="pair", compare=is_similar))))
print(list(map(str, noteutil.get_list(content="line", compare=is_in_similar))))
