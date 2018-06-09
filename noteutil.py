"""
This module contains 3 classes that are used to store data from a file and turn them into usable notes.
"""
import random


class NoteUtil:
    """
    Takes a file of notes and converts it to a string, a string with \n after each line, and a list of strings.
    Keys are used for to_dict().

    Attributes
    ----------
        notes : str
            Raw contents of the notes file.
        notes_newlines : str
            notes, but with newlines included.
        notes_list : list of str
            list created after splitting notes_newlines using "\n".

        Constants
        ---------
            KEY_NOTES : str
            KEY_NOTES_NEWLINES : str
            KEY_NOTES_LIST : str

    Special Methods
    ---------------
        __str__()
            Prints all variables separated by newlines \n.

    """

    KEY_NOTES = "notes"
    KEY_NOTES_NEWLINES = "notes_newlines"
    KEY_NOTES_LIST = "notes_list"

    def __init__(self, file_name: str=""):
        """
        Creates empty versions of all variables.
        If a file is supplied, set the variables.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into noteutil.
        """

        self.notes = ""
        self.notes_newlines = ""
        self.notes_list = []

        if file_name != "":
            NoteUtil.make_notes(self, file_name)

    def __str__(self):
        """
        Converts all variables into strings.

        Returns
        -------
        str
            All variables separated by newlines \n.
        """

        message = "NoteUtil:\n"
        message += "Notes string: " + self.get_notes() + "\n"
        message += "Notes string with newlines: " + self.get_notes_newlines() + "\n"
        message += "Notes list: " + str(self.get_notes_list()) + "\n"
        return message

    def make_notes(self, file_name: str):
        """
        Converts all the data from the file into variables.

        Parameters
        ----------
        file_name : str
            Name of the file to extract data from.

        Returns
        -------
        None

        Notes
        -----
        Implementation
            0. Read the file.
            1. Create notes by splitting by \n and then joining all the strings.
            2. Create notes_newlines, which is file.read() by default.
            3. Create notes_list by splitting by \n.

        In effect, this is also a setter method.

        """

        # Opening file 3 times just to make sure the data is not changed while reading
        file = open(file_name, mode="r", encoding="UTF-8")
        self.notes = "".join(file.read().split("\n"))
        file = open(file_name, mode="r", encoding="UTF-8")
        self.notes_newlines = file.read()
        file = open(file_name, mode="r", encoding="UTF-8")
        self.notes_list = file.read().split("\n")

    def to_dict(self):
        """
        Converts all current variables into a dictionary using key constants.

        Returns
        -------
        dict
            Dictionary of all variables {KEY_CONSTANT: variable}.
        """

        notes = dict()
        notes[self.KEY_NOTES] = self.get_notes()
        notes[self.KEY_NOTES_NEWLINES] = self.get_notes_newlines()
        notes[self.KEY_NOTES_LIST] = self.get_notes_list()
        return notes

    @staticmethod
    def parse_dict(notes: dict, noteutil=None):
        """
        Sets all of this class' variables by reading a dictionary.
        Reads using the key constants the dictionary should have been created with.

        Parameters
        ----------
        notes : dict
            Must be a dictionary created from to_dict().
        noteutil : NoteUtil, optional
            If a noteutil already exists, add on to that noteutil instead of creating a new one.

        Returns
        -------
        NoteUtil : NoteUtil
            An instance of NoteUtil or some subclass.
        """

        if noteutil is None:
            noteutil = NoteUtil()
        noteutil.notes = notes[NoteUtil.KEY_NOTES]
        noteutil.notes_newlines = notes[NoteUtil.KEY_NOTES_NEWLINES]
        noteutil.notes_list = notes[NoteUtil.KEY_NOTES_LIST]
        return noteutil

    def get_notes(self):
        """
        Returns
        -------
        str
        """

        return self.notes

    def get_notes_newlines(self):
        """
        Returns
        -------
        str
        """

        return self.notes_newlines

    def get_notes_list(self):
        """
        Returns
        -------
        list of str
        """

        return self.notes_list


class SubjectText(NoteUtil):
    """
    This class is designed to return a tip from a list of tips.
    The list is NoteUtil's notes_list.
    A subject is defined as an element in the list that appears twice.
    In between the subject are the tips.

    Key constants are used for to_dict().

    Attributes
    ----------
    subject : str
        Name of the element that appears twice.
    tips_start_index : int
        Start index in the list of the subject.
    tips_end_index : int
        End index in the list of the subject
    tips : list of str
        Elements in-between the subject
    tips_index : int
        Keeps track of how many tips have been used
    random : bool
        Determines whether the tips will be randomized

        Constants
        ---------
            KEY_TIPS: str
            KEY_TIPS_START_INDEX: str
            KEY_TIPS_END_INDEX: str
            KEY_TIPS_INDEX : str
            KEY_RANDOM : str
            KEY_SUBJECT : str

    Special Methods
    ---------------
        __str__()
            Prints all variables separated by newlines \n in addition to NoteUtil's variables.
    """

    KEY_TIPS = "tips"
    KEY_TIPS_START_INDEX = "tips_start_index"
    KEY_TIPS_END_INDEX = "tips_end_index"
    KEY_TIPS_INDEX = "tips_index"
    KEY_RANDOM = "random"
    KEY_SUBJECT = "subject"

    def __init__(self, file_name: str="", subject: str=""):
        """
        Creates empty versions of all variables.
        If a file and subject is supplied, set the variables.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into SubjectText.
        subject : str
            Name of the subject (that appears twice)
        """

        super(SubjectText, self).__init__(file_name)
        self.subject = ""
        self.tips_start_index = -1
        self.tips_end_index = -1
        self.tips = []
        self.tips_index = 0
        self.random = False

        if file_name != "" and subject != "":
            SubjectText.make_notes(self, file_name, subject)

    def __str__(self):
        """
        Converts all variables into strings.

        Returns
        -------
        str
            All variables separated by newlines \n.
        """

        message = super().__str__()
        message += "SubjectText:\n"
        message += "Start index: " + str(self.tips_start_index)
        message += "End index: " + str(self.tips_end_index)
        message += "Notes: " + str(self.tips)
        message += "Notes Index: " + str(self.tips_index)
        return message

    def to_dict(self):
        """
        Converts all current variables into a dictionary using key constants.

        Returns
        -------
        dict
            Dictionary of all variables {KEY_CONSTANT: variable}.
        """

        notes = super().to_dict()
        notes[self.KEY_TIPS] = self.tips
        notes[self.KEY_TIPS_START_INDEX] = self.tips_start_index
        notes[self.KEY_TIPS_END_INDEX] = self.tips_end_index
        notes[self.KEY_TIPS_INDEX] = self.tips_index
        notes[self.KEY_RANDOM] = self.random
        notes[self.KEY_SUBJECT] = self.get_subject()
        return notes

    def _find_tips(self):
        """
        Looks for the first occurence of subject, and then the second occurence of subject
        The subject is an element that occurs twice, and anything in between it will be tips.

        Returns
        -------
        None
        """

        for index in range(len(self.notes_list)):
            if self.notes_list[index] == self.get_subject():
                self.tips_start_index = index
                break
        for index in range(self.tips_start_index + 1, len(self.notes_list)):
            if self.notes_list[index] == self.get_subject():
                self.tips_end_index = index
                break

        if self.tips_start_index < 0 or self.tips_end_index < 0:
            raise EOFError("Start or end of subject not found. Please make sure that there are two lines"
                           " that have your subject.")

    def make_notes(self, file_name: str, subject: str):
        """
        Converts all the data from the file into variables.

        Parameters
        ----------
        file_name : str
            Name of the file to extract data from.
        subject : str
            Name of the subject (that appears twice)

        Returns
        -------
        None

        Notes
        -----
        Implementation
            0. Call NoteUtil's make_notes()
            1. Set the subject
            2. Find and make the tips using start and end index

        In effect, this is also a setter method.

        """

        super(SubjectText, self).make_notes(file_name)
        self.subject = subject
        self._find_tips()
        for index in range(self.tips_start_index + 1, self.tips_end_index):
            if self.notes_list[index] != "":
                self.tips.append(self.notes_list[index])

    def get_subject(self):
        """
        Returns
        -------
        str
        """

        return self.subject

    def randomize(self):
        """
        Shuffles the notes with random.shuffle()

        Returns
        -------
        None
        """

        random.shuffle(self.tips)
        self.random = True

    def get_next(self):
        """
        Retrieves data from tips.
        Increments the notes_index to advance to the next tip.
        If all tips have been retrieved, reset notes_index.
        If random is True, shuffle the notes again.

        Returns
        -------
        str
            The next tip.
        bool
            Whether all of the tips have been used.
        """
        nex = self.tips[self.tips_index]
        repeat = False
        self.tips_index += 1
        if self.tips_index == len(self.tips):
            repeat = True
            self.tips_index = 0
            if self.random:
                self.randomize()
        return nex, repeat

    @staticmethod
    def parse_dict(notes: dict, subject_text=None):
        """
        Sets all of this class' variables by reading a dictionary.
        Reads using the key constants the dictionary should have been created with.

        Parameters
        ----------
        notes : dict
            Must be a dictionary created from to_dict().
        subject_text : SubjectText, optional
            If a subject_text already exists, add on to that subject_text instead of creating a new one.

        Returns
        -------
        SubjectText
            An instance of SubjectText or some subclass.
        """

        if subject_text is None:
            subject_text = SubjectText()
        subject_text = NoteUtil.parse_dict(notes, subject_text)
        subject_text.tips = notes[SubjectText.KEY_TIPS]
        subject_text.tips_start_index = notes[SubjectText.KEY_TIPS_START_INDEX]
        subject_text.tips_end_index = notes[SubjectText.KEY_TIPS_END_INDEX]
        subject_text.tips_index = notes[SubjectText.KEY_TIPS_INDEX]
        subject_text.random = notes[SubjectText.KEY_RANDOM]
        subject_text.subject = notes[SubjectText.KEY_SUBJECT]
        return subject_text


class KeyValueNoteUtil(NoteUtil):
    """
    Takes a file of notes and converts it to a string, a string with \n after each line, and a list of strings.
    Keys are used for to_dict().

    Attributes
    ----------
        delim : str
            list created after splitting notes_newlines using "\n".
        notes_dict : dict of str: str
            Dictionary created from splitting each element in notes_list with delim
            {key [delim] val}
        key_indexes : list of int
            Keep tracks of what indexes (terms) have been used.
            Used to make sure terms are nonrepeating

        Constants
        ---------
            KEY_DELIM : str
            KEY_NOTES_DICT : dict of str: str
            KEY_KEY_INDEXES : list of int

    Special Methods
    ---------------
        __str__()
            Prints all variables separated by newlines \n.

    """

    KEY_DELIM = "delim"
    KEY_NOTES_DICT = "notes_dict"
    KEY_KEY_INDEXES = "key_indexes"

    def __init__(self, file_name: str="", delim: str=""):
        """
        Creates empty versions of all variables.
        If a file and delimeter is supplied, set the variables.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into noteutil.
        delim : str
            The delimeter character that separates the key from the value, or the term from the definition.
        """

        super().__init__(file_name)
        self.notes_dict = {}
        self.key_indexes = []
        self.delim = delim

        if file_name != "" and delim != "":
            KeyValueNoteUtil.make_notes(self, file_name, delim)

    def __str__(self):
        """
        Converts all variables into strings.

        Returns
        -------
        str
            All variables separated by newlines \n.
        """

        message = super().__str__()
        message += "KeyValueNoteUtil:\n"
        message += "Notes dict: " + str(self.get_notes_dict()) + "\n"
        message += "Notes dict key indexes: " + str(self.key_indexes) + "\n"
        return message

    def to_dict(self):
        """
        Converts all current variables into a dictionary using key constants.

        Returns
        -------
        dict
            Dictionary of all variables {KEY_CONSTANT: variable}.
        """

        notes = super().to_dict()
        notes[self.KEY_DELIM] = self.delim
        notes[self.KEY_NOTES_DICT] = self.get_notes_dict()
        notes[self.KEY_KEY_INDEXES] = self.key_indexes
        return notes

    def make_notes(self, file_name, delim):
        """
        Converts all the data from the file into variables.

        Parameters
        ----------
        file_name : str
            Name of the file to extract data from.
        delim : str
            The delimeter used to separate keys from values in the notes.

        Returns
        -------
        None

        In effect, this is also a setter method.
        """

        super(KeyValueNoteUtil, self).make_notes(file_name)
        self.delim = delim
        self._create_dict()
        self._create_key_indexes()

    def _create_dict(self):
        """
        Creates a dictionary based off the notes_list created in NoteUtil

        Returns
        -------
        None

        Notes
        -----
        Implementation
            0. Create a copy of the notes_list.
            1. Go through each element of the list and split it using the given delimeter.
            2. The above step will create a List[Tuple[str]] where the size of the Tuple is 2 in the order (key, value).
            3. Therefore, we must go through the List, and assign the Tuple[0] (key) to the Tuple[1] (value) for our
            notes_dict.
                4. Before assigning the key and value, we must make sure to .strip() the key and value because otherwise
                the keys may become inaccurate and filled with spaces, something we don't want.
                5. We can ignore any keys that are '' because those are just empty spaces.
                6. However, we cannot ignore any values that are '' because that means a term is not defined.
            7. Print an Error message and raise an IndexError if a key has no value.
            8. Print a different error message if the Tuple size is greater than 3, indicating an extra colon.
        """

        notes_list_copy = self.get_notes_list().copy()                                                          # 1
        for index in range(len(notes_list_copy)):
            notes_list_copy[index] = notes_list_copy[index].split(self.delim)                                   # 2, 3

        for index in range(len(notes_list_copy)):                                                               # 4
            try:
                if notes_list_copy[index][0] == "":                                                             # 6
                    continue
                else:
                    if notes_list_copy[index][1].strip() == "":                                                 # 7
                        raise IndexError
                    try:
                        notes_list_copy[index][2] = ""
                        raise ValueError
                    except IndexError:
                        self.notes_dict[notes_list_copy[index][0].strip()] = notes_list_copy[index][1].strip()  # 4,5
            except IndexError:
                print("ERROR: Missed pairing at index " + str(index))                                           # 7
                print("Term: " + str(notes_list_copy[index]))
                raise
            except ValueError:                                                                                  # 8
                print("ERROR: Extra delimeter at index " + str(index))
                print("Term: " + str(notes_list_copy[index]))
                raise

    def _create_key_indexes(self):
        """
        Creates key indexes for notes_dict

        Returns
        -------
        None
        """
        self.key_indexes = [x for x in range(len(self.get_notes_dict()))]

    def get_notes_dict(self):
        """
        Returns
        -------
        dict
        """
        return self.notes_dict

    def get_value(self, key: str):
        """
        Returns the value of a given key

        Parameters
        ----------
        key : str
            Key of the pair you want to find the value for

        Returns
        -------
        str
            Value of the given key
        None
            If no key is found
        """

        for k, val in self.notes_dict.items():
            if k.lower() == key.lower():
                return val
        return None

    def get_values(self, key: str):
        """
        Returns a list of values that have the key in it.

        Parameters
        ----------
        key : str
            Key that may appear in multiple other keys.
            "in" operator is used to find multiple keys.

        Returns
        -------
        list of str
            All of the values that corresponded with the found keys
        """

        value_list = []
        for k, v in self.get_notes_dict().items():
            if key.lower() in k.lower():
                value_list.append(v)
        return value_list

    def get_key(self, value: str=""):
        """
        Finds the first key that has the exact value (ignores case) as the value provided.

        Parameters
        ----------
        value : str
            Value/definition of the first key found with exact definition.

        Returns
        -------
        str
            Key of the first value that matches.
        None
            If no keys are found that have the exact value as the one provided.
        """

        for k, v in self.get_notes_dict().items():
            if v.lower() == value.lower():
                return k
        return None

    def get_keys(self, value: str):
        """
        Returns all of the keys that have the provided value inside the key's name or value.

        Parameters
        ----------
        value : str
            Value that may appear in multiple other values.
            "in" operator is used to find multiple values.

        Returns
        -------
        list of str
            All of the keys that have the provided value or name in their own respective value.

        Notes
        -----
        If any of the values are "", they will be ignored.
        If both of the values are "", an empty list will be returned.
        """

        key_list = []

        if value != "":
            for k, v in self.get_notes_dict().items():
                if value.lower() in v.lower() or value.lower() in k.lower():
                    key_list.append(k)

        return key_list

    def get_key_value(self, index: int):
        """
        Returns the key and value of the notes_dict at the provided index.

        Parameters
        ----------
        index : int
            Index of the key and value in the dictionary.

        Returns
        -------
        str
            Key of the notes_dict at the provided index.
        str
            Value of the notes_dict at the provided index.

        If index is out of range (greater than len(notes_dict) or less than 0), return None, None
        """

        ind = 0
        for key, val, in self.notes_dict.items():
            if ind == index:
                return key, val
            ind += 1
        return None, None

    def get_random_key_value_repeating(self):
        """
        Returns a random key and value of notes_dict

        Returns
        -------
        str
            Key of a random element in notes_dict
        str
            Value the same element in notes_dict
        """

        return self.get_key_value(random.randint(0, len(self.notes_dict) - 1))

    def get_random_key_value_nonrepeating(self):
        """
        Returns a random key and value from notes_dict, but without repeating.
        Used key and values are held in memory by key_indexes and deleting indexes from it.

        Returns
        -------
        str
            Key of a random element in notes_dict.
        str
            Value of the same element in notes_dict
        """

        rand_index = random.randint(0, len(self.notes_dict) - 1)
        while rand_index not in self.key_indexes:
            rand_index = random.randint(0, len(self.notes_dict) - 1)
        del self.key_indexes[self.key_indexes.index(rand_index)]
        if not self.key_indexes:
            self.key_indexes = [x for x in range(len(self.notes_dict))]
        return self.get_key_value(rand_index)

    def get_index(self, key: str="", value: str=""):
        """
        Returns the index of a key or value if it matches exactly.

        Parameters
        ----------
        key : str, optional if value is provided.
            Key of the element that is being searched for.
        value : str, optional if key is provided.
            Value of the element that is being searched for.
        Returns
        -------
        int
            Index of the key or value in the notes_dict.
        """

        index = 0
        for k, v in self.get_notes_dict().items():
            if k.lower() == key.lower() or v.lower() == value.lower():
                return index
            index += 1

    @staticmethod
    def parse_dict(notes: dict, noteutil=None):
        """
        Sets all of this class' variables by reading a dictionary.
        Reads using the key constants the dictionary should have been created with.

        Parameters
        ----------
        notes : dict
            Must be a dictionary created from to_dict().
        noteutil : KeyValueNoteUtil, optional
            If a noteutil already exists, add on to that noteutil instead of creating a new one.

        Returns
        -------
        KeyValueNoteUtil
            An instance of KeyValueNoteUtil or some subclass.
        """

        if noteutil is None:
            noteutil = KeyValueNoteUtil()
        noteutil = NoteUtil.parse_dict(notes, noteutil)
        noteutil.delim = notes[KeyValueNoteUtil.KEY_DELIM]
        noteutil.notes_dict = notes[KeyValueNoteUtil.KEY_NOTES_DICT]
        noteutil.key_indexes = notes[KeyValueNoteUtil.KEY_KEY_INDEXES]
        return noteutil


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
