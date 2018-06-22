"""
This module contains classes that are used to store data from a file and turn them into usable notes.
"""
import random


class NoteUtil:
    """
    Takes a file of notes and converts it into several data structures.
    Keys are used for to_dict().

    Attributes
    ----------
        notes_string : str
            Raw contents of the notes file.
        notes_newlines : str
            notes, but with newlines included.
        notes_list : list of str
            list created after splitting notes_newlines using "\n".
        line_index : int
            Index to the next line to pass chronologically.
        line_indexes : list of int
            Indexes to lines that have not been retrieved randomly yet.
        last_index : int
            Index to the previous line that was retrieved.

        Keys that are used for converting to a dictionary.
            KEY_LINE_INDEX : str
            KEY_LINE_INDEXES : str
            KEY_LAST_INDEX : str

    Special Methods
    ---------------
        __str__()
            Prints all variables separated by newlines \n.

    """
    KEY_LINE_INDEX = "line_index"
    KEY_LINE_INDEXES = "line_indexes"
    KEY_LAST_INDEX = "last_index"

    def __init__(self, file_name: str, comments: str, strip=True):
        """
        Creates empty versions of all variables.
        Initialize all variables with the file given.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into NoteUtil.
        comments : str
            Prefix of lines to be ignored.
        """

        self.notes_string = ""
        self.notes_newlines = ""
        self.notes_list = []
        self.line_index = 0
        self.line_indexes = []
        self.last_index = 0
        self.read_file(file_name, comments, strip)

    def __str__(self):
        """
        Converts all variables into strings.

        Returns
        -------
        str
            All variables with labels, separated by newlines \n.
        """

        message = "NoteUtil:\n"
        message += "Notes string: " + self.notes_string + "\n"
        message += "Notes string with newlines: " + self.notes_newlines + "\n"
        message += "Notes list: " + str(self.notes_list) + "\n"
        message += "Line index: " + str(self.line_index) + "\n"
        message += "Line indexes: " + str(self.line_indexes) + "\n"
        message += "Last index: " + str(self.last_index) + "\n"
        return message

    def read_file(self, file_name: str, comments: str, strip=True):
        """
        Converts all the data from the file into variables.
        If a line contains nothing (possibly after strip), the line will be ignored.

        Parameters
        ----------
        file_name : str
            Name of the file to extract data from.
        comments : str
            Prefix of lines to be ignored.
            Setting this to '' will skip all lines.
        strip : bool, optional
            Whether to remove whitespace / tabs / newlines for each line.

        Returns
        -------
        None

        Notes
        -----
        Implementation
            0. Open and read the file.
            1. Iterate through each line.
            2. Skip any lines that begin with the 'comments' parameter.
            3. If strip is True, strip the line.
            4. Check again if the line begins with the 'comments' parameter.
            5. Make the raw notes, notes with newlines, and notes list.
            6. When iteration is complete, create line_indexes of the same size as the notes_list.

        Even though this method is used in __init__(), this also a setter method.
        """

        file = open(file_name, mode="r", encoding="UTF-8")
        data = file.readlines()
        for line in data:
            if line.startswith(comments):
                continue
            if strip:
                line = line.strip()
            if line.startswith(comments):
                continue
            # The \n may vary if strip=True or strip=False, so use ternary conditions to add to the notes
            self.notes_string += line[:-1] if line.endswith("\n") else line
            self.notes_newlines += line if line.endswith("\n") else line + "\n"
            self.notes_list.append(line[:-1] if line.endswith("\n") else line)
        self.line_indexes = [x for x in range(len(self.notes_list))]

    def to_dict(self):
        """
        Converts all current variables into a dictionary using key constants.
        Will not convert any 'notes' because those can be remade from the notes files.

        Returns
        -------
        dict
            Dictionary of all variables {KEY_CONSTANT: variable}.
        """

        notes = dict()
        notes[self.KEY_LINE_INDEX] = self.line_index
        notes[self.KEY_LINE_INDEXES] = self.line_indexes
        notes[self.KEY_LAST_INDEX] = self.last_index
        return notes

    @staticmethod
    def parse_dict(noteutil, notes_dict: dict):
        """
        Sets changeable class variables by reading a dictionary.
        Reads using the key constants the dictionary should have been created with.

        Parameters
        ----------
        noteutil : NoteUtil
            If a NoteUtil already exists, add on to that NoteUtil instead of creating a new one.
        notes_dict : dict
            Should be a dictionary created from to_dict().
            Contains all of the keys and values of a saved NoteUtil state.

        Returns
        -------
        None
        """

        noteutil.line_index = notes_dict[NoteUtil.KEY_LINE_INDEX]
        noteutil.line_indexes = notes_dict[NoteUtil.KEY_LINE_INDEXES]
        noteutil.last_index = notes_dict[NoteUtil.KEY_LAST_INDEX]

    @staticmethod
    def empty_noteutil():
        """
        Provides a NoteUtil with default instance variables.
        The notes will only consist of an empty string ''.
        notes_list will have 1 element: ['']

        Returns
        -------
        NoteUtil
            NoteUtil with default instance variables
        """

        return NoteUtil("empty_file.txt", ":")

    def get_line(self, rand=False):
        """
        Retrieves a line of notes, moving chronologically.
        Resets to the first (top) line when all lines have been retrieved.

        Parameters
        ----------
        rand : bool
            Whether to return a line from a random index or from chronological order.

        Returns
        -------
        str
            The next line in the notes list or a random line that hasn't been requested before.
        bool
            Whether the chronological index or random index has repeated.

        Notes
        -----
        Implementation
            0. If a random line is wanted (rand=True)
                1. Continuously generate random indexes until we find one that is in line_indexes (unused).
                2. Delete the index from line_indexes because that index is now used.
                3. If we have used all indexes from line_indexes, recreate it.
            0. If a line in chronological order is wanted (rand=False)
                1. Get the next line using line_index
                2. Increment the line_index
                3. Reset the line_index if it equals the length of the notes_list (out of bounds)
            4. Set repeat to True if 3 occurs.
            5. Set the last index retrieved to whichever index was used.
            6. Return the line and if repeat occurred.
        """

        repeat = False
        if rand:
            rand_index = random.randint(0, len(self.notes_list) - 1)
            while rand_index not in self.line_indexes:
                rand_index = random.randint(0, len(self.notes_list) - 1)
            del self.line_indexes[self.line_indexes.index(rand_index)]
            if not self.line_indexes:
                self.line_indexes = [x for x in range(len(self.notes_list))]
                repeat = True
            line = self.notes_list[rand_index]
            self.last_index = rand_index

        else:
            line = self.notes_list[self.line_index]
            self.line_index += 1
            if self.line_index == len(self.notes_list):
                self.line_index = 0
                repeat = True
            self.last_index = self.line_index - 1

        return line, repeat

    def reset_all(self):
        """
        Resets all indexes except last_index to default.
        Does not reset notes (use make_notes() for that).

        Returns
        -------
        None
        """

        self.line_index = 0
        self.line_indexes = [x for x in range(len(self.notes_list))]

    def reset_chronological(self):
        """
        Resets only the chronological index (line_index) back to 0.

        Returns
        -------
        None
        """

        self.line_index = 0

    def reset_random(self):
        """
        Resets the list of indexes that have not been randomly retrieved from yet.

        Returns
        -------
        None
        """

        self.line_indexes = [x for x in range(len(self.notes_list))]

    def get_notes(self):
        """
        Returns
        -------
        str
        """

        return self.notes_string

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

    def get_line_index(self):
        """
        Returns
        -------
        int
        """

        return self.line_index


# class SubjectText(NoteUtil):
#     """
#     This class is designed to return a tip from a list of tips.
#     The list is NoteUtil's notes_list.
#     A subject is defined as an element in the list that appears twice.
#     In between the subject are the tips.
#
#     Key constants are used for to_dict().
#
#     Attributes
#     ----------
#     subject : str
#         Name of the element that appears twice.
#     tips_start_index : int
#         Start index in the list of the subject.
#     tips_end_index : int
#         End index in the list of the subject
#     tips : list of str
#         Elements in-between the subject
#     tips_index : int
#         Keeps track of how many tips have been used
#     random : bool
#         Determines whether the tips will be randomized
#
#         Constants
#         ---------
#             KEY_TIPS: str
#             KEY_TIPS_INDEX : str
#             KEY_RANDOM : str
#
#     Special Methods
#     ---------------
#         __str__()
#             Prints all variables separated by newlines \n in addition to NoteUtil's variables.
#     """
#
#     KEY_TIP_INDEX = "tip_index"
#     KEY_TIPS_INDEXES = "tips_indexes"
#     KEY_RANDOM = "random"
#
#     def __init__(self, file_name: str, comments: str, subject: str):
#         """
#         Creates empty versions of all variables.
#         If a file and subject is supplied, set the variables.
#
#         Parameters
#         ----------
#         file_name : str
#             Name of the file to be converted into SubjectText.
#         comments : str
#             Prefix of lines to be ignored.
#         subject : str
#             Name of the subject (that appears twice).
#         """
#
#         super(SubjectText, self).__init__(file_name, comments)
#         self.subject = subject
#         self.tips_start_index = -1
#         self.tips_end_index = -1
#         self.tips = []
#         self.tip_index = 0
#         self.tips_indexes = []
#         self.random = False
#
#         # SubjectText.make_notes(self, file_name, subject)
#
#     def __str__(self):
#         """
#         Converts all variables into strings.
#
#         Returns
#         -------
#         str
#             All variables separated by newlines \n.
#         """
#
#         message = super().__str__()
#         message += "SubjectText:\n"
#         message += "Start index: " + str(self.tips_start_index)
#         message += "End index: " + str(self.tips_end_index)
#         message += "Notes: " + str(self.tips)
#         message += "Tip index: " + str(self.tip_index)
#         message += "Tip indexes: " + str(self.tips_indexes)
#         message += "Random: " + str(self.random)
#         return message
#
#     def to_dict(self):
#         """
#         Converts all current variables into a dictionary using key constants.
#
#         Returns
#         -------
#         dict
#             Dictionary of all variables {KEY_CONSTANT: variable}.
#         """
#
#         notes = super().to_dict()
#         notes[self.KEY_TIP_INDEX] = self.tip_index
#         notes[self.KEY_TIPS_INDEXES] = self.tips_indexes
#         notes[self.KEY_RANDOM] = self.random
#         return notes
#
#     def _find_indexes(self):
#         """
#         Looks for the first occurrence of subject, and then the second occurrence of subject.
#         The subject is an element that occurs twice, and anything in between it will be tips.
#         Reads the notes_list created from NoteUtil.
#
#         Returns
#         -------
#         None
#         """
#
#         for index in range(len(self.notes_list)):
#             if self.notes_list[index] == self.subject:
#                 self.tips_start_index = index
#                 break
#         for index in range(self.tips_start_index + 1, len(self.notes_list)):
#             if self.notes_list[index] == self.subject:
#                 self.tips_end_index = index
#                 break
#
#         if self.tips_start_index < 0 or self.tips_end_index < 0:
#             raise EOFError("Start or end of subject not found. Please make sure that there are two lines"
#                            " that have your subject.")
#
#     def make_tips(self, subject: str, strip=True):
#         """
#         Take all elements from notes_list between the start index and end index and convert into tips.
#         If there is nothing after the whitespace (possibly after strip), the tip will be ignored.
#
#         Parameters
#         ----------
#         subject : str
#             Name of the subject (that appears twice)
#         strip : bool, optional
#             Whether to remove whitespace and tabs from the tip before adding to the tips.
#
#         Returns
#         -------
#         None
#
#         Notes
#         -----
#         Implementation
#             0. Call NoteUtil's make_notes()
#             1. Set the subject
#             2. Find and make the tips using start and end index
#
#         Even though this method is used in __init__(), this is also a setter method.
#
#         """
#
#         self.subject = subject
#         self._find_indexes()
#         for index in range(self.tips_start_index + 1, self.tips_end_index):
#             tip = self.notes_list[index]
#             if strip:
#                 tip = tip.strip()
#             if tip != "":
#                 self.tips.append(self.notes_list[index])
#
#     def get_subject(self):
#         """
#         Returns
#         -------
#         str
#         """
#
#         return self.subject
#
#     def get_tip(self):
#         """
#         Retrieves a tip.
#         Resets to the first (top) tip when all tips have been returned.
#         If randomize() has been used, the tips will be shuffled after all tips are used.
#
#         Returns
#         -------
#         str
#             The next tip.
#         bool
#             Whether all of the tips have been used.
#         """
#         tip = self.tips[self.tips_index]
#         repeat = False
#         self.tips_index += 1
#         if self.tips_index == len(self.tips):
#             repeat = True
#             self.tips_indexes = [x for x in range(len(self.tips))]
#             if self.random:
#                 self.randomize()
#         return tip, repeat
#
#     @staticmethod
#     def parse_dict(notes: dict, subject_text=None):
#         """
#         Sets all of this class' variables by reading a dictionary.
#         Reads using the key constants the dictionary should have been created with.
#
#         Parameters
#         ----------
#         notes : dict
#             Must be a dictionary created from to_dict().
#         subject_text : SubjectText, optional
#             If a subject_text already exists, add on to that subject_text instead of creating a new one.
#
#         Returns
#         -------
#         SubjectText
#             An instance of SubjectText or some subclass.
#         """
#
#         if subject_text is None:
#             subject_text = SubjectText()
#         subject_text = NoteUtil.parse_dict(notes, subject_text)
#         subject_text.tips = notes[SubjectText.KEY_TIPS]
#         subject_text.tips_start_index = notes[SubjectText.KEY_TIPS_START_INDEX]
#         subject_text.tips_end_index = notes[SubjectText.KEY_TIPS_END_INDEX]
#         subject_text.tips_index = notes[SubjectText.KEY_TIPS_INDEX]
#         subject_text.random = notes[SubjectText.KEY_RANDOM]
#         subject_text.subject = notes[SubjectText.KEY_SUBJECT]
#         return subject_text


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

    def make_notes(self, file_name, comments, delim):
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


notes = NoteUtil("test_notes.txt", "!", strip=False)
print(notes)