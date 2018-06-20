"""
This module contains classes that are used to store data from a file and turn them into usable notes.
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
        line_index : int
            Pointer to the next line to pass chronologically

        Constants
        ---------
            KEY_NOTES : str
            KEY_NOTES_NEWLINES : str
            KEY_NOTES_LIST : str
            KEY_LINE_INDEX : str

    Special Methods
    ---------------
        __str__()
            Prints all variables separated by newlines \n.

    """

    KEY_NOTES = "notes"
    KEY_NOTES_NEWLINES = "notes_newlines"
    KEY_NOTES_LIST = "notes_list"
    KEY_LINE_INDEX = "line_index"

    def __init__(self, file_name: str="", comments: str=""):
        """
        Creates empty versions of all variables.
        If a file is supplied, set the variables.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into noteutil.
        comments : str
            Prefix of lines to be ignored.
        """

        self.notes = ""
        self.notes_newlines = ""
        self.notes_list = []
        self.line_index = 0

        if file_name != "" and comments != "":
            NoteUtil.make_notes(self, file_name, comments)

    def __str__(self):
        """
        Converts all variables into strings.

        Returns
        -------
        str
            All variables separated by newlines \n.
        """

        message = "NoteUtil:\n"
        message += "Notes string: " + self.notes + "\n"
        message += "Notes string with newlines: " + self.notes_newlines + "\n"
        message += "Notes list: " + str(self.notes_list) + "\n"
        return message

    def make_notes(self, file_name: str, comments: str):
        """
        Converts all the data from the file into variables.

        Parameters
        ----------
        file_name : str
            Name of the file to extract data from.
        comments : str
            Prefix of lines to be ignored.

        Returns
        -------
        None

        Notes
        -----
        Implementation
            0. Open and read the file.
            1. Iterate through each line.
            2. Skip any lines that begin with the 'comments' parameter.
            3. Make the raw notes, notes with newlines, and notes list.

        In effect, this is also a setter method.

        """

        # Opening file 3 times just to make sure the data is not changed while reading
        file = open(file_name, mode="r", encoding="UTF-8")
        data = file.readlines()
        for line in data:
            line = line.strip()
            if line.startswith(comments):
                continue
            self.notes += line
            self.notes_newlines += line + "\n"
            self.notes_list.append(line)

    def to_dict(self):
        """
        Converts all current variables into a dictionary using key constants.

        Returns
        -------
        dict
            Dictionary of all variables {KEY_CONSTANT: variable}.
        """

        notes = dict()
        notes[self.KEY_NOTES] = self.get_notes
        notes[self.KEY_NOTES_NEWLINES] = self.notes_newlines
        notes[self.KEY_NOTES_LIST] = self.notes_list
        notes[self.KEY_LINE_INDEX] = self.line_index
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

    def reset(self):
        """
        Resets any pointers to notes
        Does not reset notes (use make_notes() for that)

        Returns
        -------
        None
        """

        self.line_index = 0

    def get_line(self):
        """
        Retrieves a line of notes, moving chronologically.
        Resets to the first (top) line when all lines have been retrieved.

        Returns
        -------
        str
            The next line in the notes list.
        """

        line = self.notes_list[self.line_index]
        self.line_index += 1
        if self.line_index == len(self.notes_list):
            self.line_index = 0
            print("All notes have been read.")
        return line

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

    def __init__(self, file_name: str="", comments: str="", subject: str=""):
        """
        Creates empty versions of all variables.
        If a file and subject is supplied, set the variables.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into SubjectText.
        comments : str
            Prefix of lines to be ignored
        subject : str
            Name of the subject (that appears twice)
        """

        super(SubjectText, self).__init__(file_name, comments)
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
        notes[self.KEY_SUBJECT] = self.subject
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
            if self.notes_list[index] == self.subject:
                self.tips_start_index = index
                break
        for index in range(self.tips_start_index + 1, len(self.notes_list)):
            if self.notes_list[index] == self.subject:
                self.tips_end_index = index
                break

        if self.tips_start_index < 0 or self.tips_end_index < 0:
            raise EOFError("Start or end of subject not found. Please make sure that there are two lines"
                           " that have your subject.")

    def make_notes(self, file_name: str, comments: str, subject: str):
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

        super(SubjectText, self).make_notes(file_name, comments)
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
        message += "Notes dict: " + str(self.notes_dict) + "\n"
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
        notes[self.KEY_NOTES_DICT] = self.notes_dict
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

        notes_list_copy = self.notes_list.copy()                                                                # 1
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
        self.key_indexes = [x for x in range(len(self.notes_dict))]

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
        for k, v in self.notes_dict.items():
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

        for k, v in self.notes_dict.items():
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
            for k, v in self.notes_dict.items():
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
        for k, v in self.notes_dict.items():
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


notes = NoteUtil("test_notes.txt", "#")
print(notes)
for _ in range(10):
    print(notes.get_line())
notes.reset()
print(notes.get_line())

