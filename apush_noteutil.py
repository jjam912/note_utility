from note_format.noteutil import KeyValueNoteUtil
import random


# Personal use, not intended to be extended.
class APUSHNoteUtil(KeyValueNoteUtil):
    KEY_NOTES_DICT_NO_PERIOD_NO_CHAPTER = "notes_dict_no_period_no_chapter"
    KEY_KEY_INDEXES_NO_PERIOD_NO_CHAPTER = "key_indexes_no_period_no_chapter"
    KEY_PERIOD_LIST = "period_list"
    KEY_KEY_INDEXES_PERIOD = "key_indexes_period"
    KEY_CHAPTER_LIST = "chapter_list"
    KEY_KEY_INDEXES_CHAPTER = "key_indexes_chapter"
    KEY_PERIOD = "period"
    KEY_CHAPTER = "chapter"
    KEY_PERIOD_INDEXES = "period_indexes"
    KEY_CHAPTER_INDEXES = "chapter_indexes"

    def __init__(self, file_name="", delim=""):
        """
        Create another dictionary from notes_dict, but without period and chapters in the keys
        Create another key_indexes from notes_dict_no_period_no_chapter, thus making a shorter list for the shorter dict
        Also init the prefixes for period and chapter for convenience when searching.
        :param file_name: str
        :param delim: str
        """
        super().__init__(file_name, delim)
        self.notes_dict_no_period_no_chapter = {}
        self.key_indexes_no_period_no_chapter = []
        self.period_list = []
        self.key_indexes_period = []
        self.chapter_list = []
        self.key_indexes_chapter = []
        self.period = "period"
        self.chapter = "chapter"
        self.period_indexes = []
        self.chapter_indexes = []

        if file_name != "" and delim != "":
            APUSHNoteUtil.make_notes(self, file_name, delim)

    def __str__(self):
        message = super().__str__()
        message += "APUSHNoteUtil:\n"
        message += "Notes dict no period no chapter: " + str(self.get_notes_dict_no_period_no_chapter()) + "\n"
        message += "Notes dict no period no chapter key indexes: " + str(self.key_indexes_no_period_no_chapter) + "\n"
        message += "Period list: " + str(self.get_period_list()) + "\n"
        message += "Period key indexes: " + str(self.key_indexes_period) + "\n"
        message += "Period indexes: " + str(self.get_period_indexes()) + "\n"
        message += "Chapter list: " + str(self.get_chapter_list()) + "\n"
        message += "Chapter key indexes: " + str(self.key_indexes_chapter) + "\n"
        message += "Chapter indexes: " + str(self.get_chapter_indexes()) + "\n"
        return message

    def to_dict(self):
        notes = super().to_dict()
        notes[self.KEY_NOTES_DICT_NO_PERIOD_NO_CHAPTER] = self.get_notes_dict_no_period_no_chapter()
        notes[self.KEY_KEY_INDEXES_NO_PERIOD_NO_CHAPTER] = self.key_indexes_no_period_no_chapter
        notes[self.KEY_PERIOD_LIST] = self.get_period_list()
        notes[self.KEY_KEY_INDEXES_PERIOD] = self.key_indexes_period
        notes[self.KEY_CHAPTER_LIST] = self.get_chapter_list()
        notes[self.KEY_KEY_INDEXES_CHAPTER] = self.key_indexes_chapter
        notes[self.KEY_PERIOD] = self.period
        notes[self.KEY_CHAPTER] = self.chapter
        notes[self.KEY_PERIOD_INDEXES] = self.get_period_indexes()
        notes[self.KEY_CHAPTER_INDEXES] = self.get_chapter_indexes()
        return notes

    def make_notes(self, file_name, delim):
        super(APUSHNoteUtil, self).make_notes(file_name, delim)
        self._find_period_indexes()
        self._find_chapter_indexes()
        self._create_dict_no_period_no_chapter()
        self._create_key_indexes_no_period_no_chapter()
        self._create_dict_each_chapter()
        self._create_key_indexes_each_chapter()
        self._create_dict_each_period()
        self._create_key_indexes_each_period()
        assert len(self.period_list) != 0
        assert len(self.chapter_list) != 0

    def _create_dict_no_period_no_chapter(self):
        """
        Create a copy of the notes_dict for deleting certain keys
        Search through each key, value using indexing and delete any keys with self.period or self.chapter in it
        Set the new dictionary, notes_dict_no_period_no_chapter = notes_dict_copy
        :return: None
        """
        notes_dict_copy = self.get_notes_dict().copy()
        for index in reversed(range(len(notes_dict_copy))):
            key, value = self.get_key_value(index)
            if self.period.lower() in key.lower() or self.chapter.lower() in key.lower():
                notes_dict_copy.pop(key)
        self.notes_dict_no_period_no_chapter = notes_dict_copy

    def _create_key_indexes_no_period_no_chapter(self):
        """
        Creates key indexes for the no_period_no_chapter dictionary that will hold which indexes have already been
        used when a random question has been selected.
        :return: None
        """
        self.key_indexes_no_period_no_chapter = [x for x in range(len(self.get_notes_dict_no_period_no_chapter()))]

    def _create_dict_each_period(self):
        """
        Pre-condition: chapter_list has been created
        Post-condition: A List[Dict[str: str]] has been created, and each Dict may have multiple chapters
        1. Create a chapter index that will be used to track each chapter's index
        2. Run through each index in period_indexes
            3. While the current chapter index is less than the next period's index,
                4. Add a chapter to the current dictionary (period) and increment chapter_index
            5. We will eventually run into an IndexError because we use period_index + 1
                6. Since we kept track of chapter_index, just add everything from there to the end of chapter_list
        7. Add dictionaries to period_list
        :return: None
        """
        chapter_index = 0                                                                                           # 1
        for period_index in range(len(self.get_period_indexes())):                                                  # 2
            curr_period = {}
            try:
                while self.get_chapter_indexes()[chapter_index] < self.get_period_indexes()[period_index + 1]:      # 3
                    curr_period.update(self.get_chapter_list()[chapter_index])                                      # 4
                    chapter_index += 1
                self.period_list.append(curr_period)                                                                # 7
            except IndexError:                                                                                      # 5
                for chapter in range(chapter_index, len(self.get_chapter_indexes())):                               # 6
                    curr_period.update(self.get_chapter_list()[chapter])
                self.period_list.append(curr_period)                                                                # 7

    def _create_key_indexes_each_period(self):
        """
        Creates a list of key indexes for each period, as found in period_list
        :return: None
        """
        for per in self.get_period_list():
            self.key_indexes_period.append([x for x in range(len(per))])

    def _create_dict_each_chapter(self):
        """
        Pre-condition: chapter_indexes and period_indexes have been defined
        Post-condition: A List[Dict[str: str]] has been created, and each Dict is a chapter

        1. Run through each index in chapter_indexes
            2. From that index + 1 to the next index - 1, create a dictionary of all keys and values that are
            in between those indexes, inclusive.
            index + 1 is used because there is a chapter at index
            Chapter 1: A New World of Many Cultures <-- this is what is at index
            Encomienda System: ----  <-- this is what is at index + 1
            Period 2: 1607-1754  <-- this is what is sometimes at next index - 2 -> We will have to ignore this
            3. Ignore any periods by detecting if self.period is in the key
        4. Since we go through all of the indexes, we are bound to run into an IndexError on the last index.
            When this happens, we catch the error, and then use index and len(notes_dict) since we want to go
            from index to the end of the dictionary. Again, use index + 1
        5. Add every dictionary to chapter_list
        :return: None
        """
        for chapter_index in range(len(self.get_chapter_indexes())):                                     # 1
            curr_chapter = {}
            try:
                for index in range(self.get_chapter_indexes()[chapter_index] + 1,
                                   self.get_chapter_indexes()[chapter_index + 1]):                       # 2
                    key, value = self.get_key_value(index)
                    if not (self.period.lower() in key.lower()):                                         # 3
                        curr_chapter[key] = value
                self.chapter_list.append(curr_chapter)                                                   # 5
            except IndexError:                                                                           # 4
                for index in range(self.get_chapter_indexes()[-1] + 1, len(self.get_notes_dict())):
                    # The last chapter will not have any periods after it, so we don't have to ignore any
                    key, value = self.get_key_value(index)
                    curr_chapter[key] = value
                self.chapter_list.append(curr_chapter)                                                   # 5

    def _create_key_indexes_each_chapter(self):
        """
        Creates a list of key indexes for each chapter, as found in chapter_list
        :return: None
        """
        for chap in self.get_chapter_list():
            self.key_indexes_chapter.append([x for x in range(len(chap))])

    def _find_period_indexes(self):
        """
        1. Get all the values of the periods
        2. Get the indexes of the periods from those values
        :return: None
        """
        period_values = self.get_values(self.period)                    # 1
        for per in period_values:
            self.period_indexes.append(self.get_index(value=per))       # 2

    def _find_chapter_indexes(self):
        """
        1. Get all the values of the chapters
        2. Get the indexes of the chapters from those values
        :return: None
        """
        chapter_values = self.get_values(self.chapter)                  # 1
        for chap in chapter_values:
            self.chapter_indexes.append(self.get_index(value=chap))     # 2

    def get_notes_dict_no_period_no_chapter(self):
        """
        Returns notes_dict_no_period_no_chapter, the dictionary without periods or chapters
        :return: Dict{str: str}
        """
        return self.notes_dict_no_period_no_chapter

    def get_period_list(self):
        """
        Returns period_list
        :return: List[Dict[str: str]]
        """
        return self.period_list

    def get_chapter_list(self):
        """
        Returns chapter_list
        :return: List[Dict[str: str]]
        """
        return self.chapter_list

    def get_key_value_no_period_no_chapter(self, index: int):
        """
        Returns the key and value of the notes_dict at a given index
        :param index: int
        :return: Tuple(str, str) or None if index is out of range
        """
        ind = 0
        for key, val, in self.notes_dict_no_period_no_chapter.items():
            if ind == index:
                return key, val
            ind += 1
        return None

    def get_index_no_period_no_chapter(self, key: str=None, value: str=None):
        """
        Returns the index of a key or value by searching through the whole dictionary
        :param key: str
        :param value: str
        :return: int
        """
        index = 0
        for k, v in self.get_notes_dict_no_period_no_chapter().items():
            if k.lower() == key.lower() or v.lower() == value.lower():
                return index
            index += 1

    def get_period(self, key: str):
        """
        1. Find a value for this term to see if it exists
        2. If there is a KeyError, the term does not exist, and thus we will raise a ValueError
        3. If there is not a KeyError, the term exists
        4. We will then find the index of the value in the regular notes_dict using self.get_index()
        5. We will lower the index until it reaches a 'Period ' as denoted by self.period
        6. Return key, value of notes_dict using the get_key_value() method from KeyValueNoteUtil
        :param key: str
        :return: Tuple(str, str)
        """
        try:
            value = self.get_value(key)                     # 1
        except KeyError:                                    # 2
            raise ValueError(key + " does not exist")
        index = self.get_index(value=value)                 # 3, 4
        k, v = self.get_key_value(index)
        while self.period.lower() not in k.lower():         # 5
            index -= 1
            k, v = self.get_key_value(index)
        return k, v                                         # 6

    def get_chapter(self, key: str):
        """
        1. Find a value for this term to see if it exists
        2. If there is a KeyError, the term does not exist, and thus we will raise a ValueError
        3. If there is not a KeyError, the term exists
        4. We will then find the index of the value in the regular notes_dict
        5. We will lower the index until it reaches a 'Chapter ' as denoted by self.chapter
        6. Return key, value of notes_dict using the get_key_value() method from KeyValueNoteUtil
        :param key: str
        :return: Tuple(str, str)
        """
        try:
            value = self.get_value(key)                     # 1
        except KeyError:
            raise ValueError(key + " does not exist")       # 2
        index = self.get_index(value=value)                 # 3, 4
        k, v = self.get_key_value(index)
        while self.chapter.lower() not in k.lower():        # 5
            index -= 1
            k, v = self.get_key_value(index)
        return k, v                                         # 6

    def get_period_indexes(self):
        """
        Return period_indexes
        :return: List[int]
        """
        return self.period_indexes

    def get_chapter_indexes(self):
        """
        Return chapter_indexes
        :return: List[int]
        """
        return self.chapter_indexes

    def get_key_value_period(self, index: int, period: int):
        """
        Returns the key and value of the period_list at a given index
        :param index: int
        :param period: int
        :return: Tuple(str, str) or None if index is out of range
        """
        ind = 0
        for key, val, in self.get_period_list()[period].items():
            if ind == index:
                return key, val
            ind += 1
        return None

    def get_key_value_chapter(self, index: int, chapter: int):
        """
        Returns the key and value of the chapter_dict at a given index
        :param index: int
        :param chapter: int
        :return: Tuple(str, str) or None if index is out of range
        """
        ind = 0
        for key, val, in self.get_chapter_list()[chapter].items():
            if ind == index:
                return key, val
            ind += 1
        return None

    def get_random_key_value_repeating_no_period_no_chapter(self):
        """
        Returns a random key and value using the no_period_no_chapter dictionary
        :return: Tuple(str, str)
        """
        return self.get_key_value_no_period_no_chapter(random.randint(0, len(self.notes_dict_no_period_no_chapter) - 1))

    def get_random_key_value_nonrepeating_no_period_no_chapter(self):
        """
        Returns a random key and value using an index that is still in key_indexes_no_period_no_chapter.
        If key_indexes_no_period_no_chapter becomes empty, recreate it.
        :return: Tuple(str, str)
        """
        rand_index = random.randint(0, len(self.get_notes_dict_no_period_no_chapter()) - 1)
        while rand_index not in self.key_indexes_no_period_no_chapter:
            rand_index = random.randint(0, len(self.get_notes_dict_no_period_no_chapter()) - 1)
        del self.key_indexes_no_period_no_chapter[self.key_indexes_no_period_no_chapter.index(rand_index)]
        if not self.key_indexes_no_period_no_chapter:
            print("One Cycle Completed")
            self._create_key_indexes_no_period_no_chapter()
        return self.get_key_value_no_period_no_chapter(rand_index)

    def get_random_key_value_nonrepeating_period(self, period: int):
        """
        0. Subtract 1 from period because arrays are 0-indexed
        1. Determine whether :param: period is within bounds of period_list if not, throw IndexError
        2. Generate a random integer within the range of the period
        3. Make sure this random integer is unique and has not been called before
        4. Delete the random integer from key_indexes to make sure it's been called
        5. If key_indexes is empty, recreate it
        6. Return a key and value at the given random integer
        :param period: int
        :return: Tuple(str, str)
        """
        period -= 1                                                                                 # 0
        if period < 0 or period >= len(self.get_period_list()):
            raise IndexError("Period index is out of range")                                        # 1
        period_dict = self.get_period_list()[period]
        rand_index = random.randint(0, len(period_dict) - 1)                                        # 2
        while rand_index not in self.key_indexes_period[period]:                                    # 3
            rand_index = random.randint(0, len(period_dict) - 1)
        del self.key_indexes_period[period][self.key_indexes_period[period].index(rand_index)]      # 4
        if not self.key_indexes_period[period]:                                                     # 5
            print("One Cycle Completed")
            self.key_indexes_period[period] = [x for x in range(len(period_dict))]
        return self.get_key_value_period(rand_index, period)                                        # 6

    def get_random_key_value_nonrepeating_chapter(self, chapter: int):
        """
        0. Subtract 1 from chapter because arrays are 0-indexed
        1. Determine whether :param: chapter is within bounds of chapter_list if not, throw IndexError
        2. Generate a random integer within the range of the chapter
        3. Make sure this random integer is unique and has not been called before
        4. Delete the random integer from key_indexes to make sure it's been called
        5. If key_indexes is empty, recreate it
        6. Return a key and value at the given random integer
        :param chapter: int
        :return: Tuple(str, str)
        """
        chapter -= 1                                                                                  # 0
        if chapter < 0 or chapter >= len(self.get_chapter_list()):
            raise IndexError("Chapter index is out of range")                                         # 1
        chapter_dict = self.get_chapter_list()[chapter]
        rand_index = random.randint(0, len(chapter_dict) - 1)                                         # 2
        while rand_index not in self.key_indexes_chapter[chapter]:                                    # 3
            rand_index = random.randint(0, len(chapter_dict) - 1)
        del self.key_indexes_chapter[chapter][self.key_indexes_chapter[chapter].index(rand_index)]    # 4
        if not self.key_indexes_chapter[chapter]:                                                     # 5
            print("One Cycle Completed")
            self.key_indexes_chapter[chapter] = [x for x in range(len(chapter_dict))]
        return self.get_key_value_chapter(rand_index, chapter)                                        # 6

    @staticmethod
    def parse_dict(notes: dict, noteutil=None):
        """
        Parses the dictionary version of this class
        Particularly useful with JSON
        :param: dic - dictionary
        :return: NoteUtil
        """
        if noteutil is None:
            noteutil = APUSHNoteUtil()
        noteutil = KeyValueNoteUtil.parse_dict(notes, noteutil)
        noteutil.notes_dict_no_period_no_chapter = notes[APUSHNoteUtil.KEY_NOTES_DICT_NO_PERIOD_NO_CHAPTER]
        noteutil.key_indexes_no_period_no_chapter= notes[APUSHNoteUtil.KEY_KEY_INDEXES_NO_PERIOD_NO_CHAPTER]
        noteutil.period_list = notes[APUSHNoteUtil.KEY_PERIOD_LIST]
        noteutil.key_indexes_period = notes[APUSHNoteUtil.KEY_KEY_INDEXES_PERIOD]
        noteutil.chapter_list = notes[APUSHNoteUtil.KEY_CHAPTER_LIST]
        noteutil.key_indexes_chapter = notes[APUSHNoteUtil.KEY_KEY_INDEXES_CHAPTER]
        noteutil.period = notes[APUSHNoteUtil.KEY_PERIOD]
        noteutil.chapter = notes[APUSHNoteUtil.KEY_CHAPTER]
        noteutil.period_indexes = notes[APUSHNoteUtil.KEY_PERIOD_INDEXES]
        noteutil.chapter_indexes = notes[APUSHNoteUtil.KEY_CHAPTER_INDEXES]
        return noteutil