import noteutil as nu
import os


basic_noteutil = nu.NoteUtil("test_data/basic_config.txt", refresh=True)
# pair_noteutil = nu.NoteUtil("test_data/pair_config.txt", refresh=True)
# heading_noteutil = nu.NoteUtil("test_data/heading_config.txt", refresh=True)
# extension_noteutil = nu.NoteUtil("test_data/extension_config.txt", refresh=True)
# category_noteutil = nu.NoteUtil("test_data/category_config.txt", refresh=True)
# all1_noteutil = nu.NoteUtil("test_data/all1_config.txt", refresh=True)
# all2_noteutil = nu.NoteUtil("test_data/all2_config.txt", refresh=True)
# all3_noteutil = nu.NoteUtil("test_data/all3_config.txt", refresh=True)


class TestNoteUtilConfig:
    def test_note_file(self):
        assert basic_noteutil.note_file == "test_data/basic_notes.txt"

    def test_nu_file(self):
        assert basic_noteutil.nu_file == "test_data/basic_notes.nu"

    def test_comments(self):
        assert basic_noteutil.comments == "#"

    def test_blocks(self):
        assert basic_noteutil.blocks == "`"


class TestNoteUtilAttributes:
    def test_line(self):
        pass

    def test_block(self):
        pass


class TestNoteUtilMethods:
    pass


class TestNoteAttributes:
    pass


class TestExtensionAttributes:
    pass