"""
This module contains classes that are used to store data from a file and turn them into usable notes.
"""
import random
from note_format.mydas import IndexedDict


class NoteUtil:
    """
    Takes a file of notes and converts it into several data structures.
    Keys are used for to_dict().

    Attributes
    ----------
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
        strip : bool
            Whether to strip() the file lines when they are read.
        """

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
        message += "Notes list: " + str(self.notes_list) + "\n"
        message += "Line index: " + str(self.line_index) + "\n"
        message += "Line indexes: " + str(self.line_indexes) + "\n"
        message += "Last index: " + str(self.last_index) + "\n"
        return message

    def read_file(self, file_name: str, comments: str, strip=True):
        """
        Converts all the data from the file into a list of notes.
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
            5. Make the notes list.
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
    def parse_dict(noteutil, var_dict: dict):
        """
        Sets changeable class variables by reading a dictionary.
        Reads using the key constants the dictionary should have been created with.

        Parameters
        ----------
        noteutil : NoteUtil
            If a NoteUtil already exists, add on to that NoteUtil instead of creating a new one.
        var_dict : dict
            Should be a dictionary created from to_dict().
            Contains all of the keys and values of a saved NoteUtil state.

        Returns
        -------
        None
        """

        noteutil.line_index = var_dict[NoteUtil.KEY_LINE_INDEX]
        noteutil.line_indexes = var_dict[NoteUtil.KEY_LINE_INDEXES]
        noteutil.last_index = var_dict[NoteUtil.KEY_LAST_INDEX]

    def get_line(self, rand=False):
        """
        Retrieves a line of notes, moving chronologically or randomly.
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


class PairedNoteUtil(NoteUtil):
    """
    Splits all lines in notes_list into key, value pairs known as terms and definitions.

    Terms and definitions are separated by delimeters, which occur only once in each line but can be any character.
    Creates a dictionary out of all of the terms and definitions by splitting by the delimeter.
    Keys are used for to_dict().

    Attributes
    ----------
        delimeter : str
            The character that separates terms from definitions.
        notes_dict : IndexedDict of {str: str}
            IndexedDict (see mydas.py) created from splitting each element in notes_list with the delimeter.
        dict_index : int
            Chronological index of the next pair of term and definitions.
        dict_indexes : list of int
            Keep tracks of what pairs (terms and definitions) have been used.
            Used to make sure terms are not repeating.

        Keys that are used for converting to a dictionary.
            KEY_DICT_INDEX : str
            KEY_DICT_INDEXES : str

    Special Methods
    ---------------
        __str__()
            Prints all variables separated by newlines \n.

    """

    KEY_DICT_INDEX = "dict_index"
    KEY_DICT_INDEXES = "dict_indexes"

    def __init__(self, file_name: str, comments: str, delimeter: str, strip=True):
        """
        Initialize all variables with the file given.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into PairedNoteUtil.
        comments : str
            The prefix of lines that will be ignored, checked both before and after strip.
        delimeter : str
            The character that separates the key from the value, or the term from the definition.
        strip : bool
            Whether to strip() the file line of whitespace.

        """

        super().__init__(file_name, comments, strip)
        self.delimeter = delimeter
        self.notes_dict = IndexedDict()
        self.dict_index = 0
        self.dict_indexes = []
        self.make_notes_dict(strip)

    def __str__(self):
        """
        Converts all variables into strings.

        Returns
        -------
        str
            All variables with labels separated by newlines.
        """

        message = super().__str__() + "\n"
        message += "PairedNoteUtil:\n"
        message += "Delimeter: " + self.delimeter + "\n"
        message += "Notes dict: \n"
        for i, td in enumerate(self.notes_dict.items()):
            t, d = td
            message += t + " " + self.delimeter + " " + d + " Index: " + str(i) + "\n"
        message += "Dict index: " + str(self.dict_index) + "\n"
        message += "Dict indexes: " + str(self.dict_indexes) + "\n"

        return message

    def to_dict(self):
        """
        Converts all changeable variables into a dictionary using key constants.

        Will not convert any 'notes' because those can be remade from the notes files.

        Returns
        -------
        dict
            Dictionary of all variables {KEY_CONSTANT: variable}.
        """

        notes = super().to_dict()
        notes[self.KEY_DICT_INDEX] = self.dict_index
        notes[self.KEY_DICT_INDEXES] = self.dict_indexes
        return notes

    @staticmethod
    def parse_dict(noteutil, var_dict: dict):
        """
        Sets all of this class' changeable variables by reading a dictionary.

        Reads using the key constants the dictionary should have been created with.

        Parameters
        ----------
        noteutil : PairedNoteUtil
            An instance of NoteUtil that has been initialized with the same file as the dictionary was created from.
        var_dict : dict
            A dictionary created from PairedNoteUtil.to_dict() that has all of the key constants.

        Returns
        -------
        None
        """

        super().parse_dict(noteutil, var_dict)
        noteutil.dict_index = var_dict[PairedNoteUtil.KEY_DICT_INDEX]
        noteutil.dict_indexes = var_dict[PairedNoteUtil.KEY_DICT_INDEXES]

    def make_notes_dict(self, strip=True):
        """
        Creates a IndexedDict based off the notes_list created in NoteUtil.

        If we want to create a new dictionary from a new file, we must first read_file()
            before calling this or recreate a PairedNoteUtil.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If there is a syntax error or value error while parsing the notes_list for terms and definitions.

        Notes
        -----
        Implementation
            0. Create a shallow copy of the notes_list (all elements are Strings, so no need for deep copy).
            1. Go through each element of the list and split it using the given delimeter.
            2. The above step will create a List[Tuple[str]] where the size of the Tuple
                is 2 in the order (term, definition).
            3. Therefore, we must go through the List, and assign the Tuple[0] (term) to the Tuple[1] (definition)
                for our notes_dict.
                4. Before assigning the term to the definition, we have the option to .strip() the term and definition
                5. We can ignore any keys that are '' because those are just empty lines.
                6. However, we cannot ignore any values that are '' because that means a term is not defined.
            7. Print an error message if the Tuple size is greater than 2, meaning a delimeter appeared
                more than once in a line.
            8. Print a different error message for each term that has no definition.
            9. Check for any duplicates and print a warning message.
            10. Create the dict indexes once all notes have been iterated through.

        Errors are not raised until the loop has exited because there could be
             many Syntax or Value errors in a file, and it may be easier just to print all the errors at once.
        """

        notes_list = self.notes_list[:]
        error = False
        error_message = "Errors: " + "\n"
        for i in range(len(notes_list)):
            notes_list[i] = notes_list[i].split(self.delimeter)

        for i in range(len(notes_list)):
            try:
                if len(notes_list[i]) > 2:
                    raise SyntaxError       # More than 1 delimeter in the line.
                term = notes_list[i][0]
                definition = notes_list[i][1]
                if strip:
                    term = term.strip()
                    definition = definition.strip()
                if term == "":              # Blank space (baby, and I'll write your name ~help me~)
                    continue
                if definition == "":
                    raise ValueError        # Term has no definition

                if term in self.notes_dict:
                    raise KeyError          # Term already exists

                self.notes_dict[term] = definition

            except SyntaxError:
                error_message += "ERROR: Extra delimeter at around line " + str(i+1) + ". "
                error_message += "Pair: " + str(notes_list[i]) + "\n"
                error = True
            except ValueError:
                error_message += "ERROR: Missed pairing at around line " + str(i+1) + ". "
                error_message += "Pair: " + str(notes_list[i]) + "\n"
                error = True
            except KeyError:
                error_message += "WARNING: Repeated term at around line " + str(i+1) + ". "
                error_message += "Pair: " + str(notes_list[i]) + "\n"

        print(error_message)
        assert error is False, \
            "There were syntax errors found in your file.\n" "Please review above error messages and fix them."

        self.dict_indexes = [x for x in range(len(self.notes_dict))]

    def term(self, definition: str, case_sensitive: bool=True):
        """
        Returns a list of terms that matches exactly with the given definition.

        Parameters
        ----------
        definition : str
            Name that mtaches a definition in notes_dict.
        case_sensitive : bool
            Whether case matters.

        Returns
        -------
        list of term
            All of the terms that corresponded with the term name or definition name.

        Raises
        ------
        ValueError
            If the provided term or definition is not found within the notes_dict's keys.
        """

        return self.notes_dict.key_with(definition, case_sensitive=case_sensitive)

    def definition(self, term: str, case_sensitive: bool=True):
        """
        Returns a list of definitions that have part of the term name as its key or part of the definition name in it.

        Parameters
        ----------
        term : str
            Name of the term that may be in a definition's key.
        case_sensitive : bool
            Whether case matters.

        Returns
        -------
        list of str
            All definitions that had a key that corresponded with term or part of the definition. See IndexedDict.

        Raises
        ------
        ValueError
            If the provided term or definition is not found within the notes_dict's values.
        """

        return self.notes_dict.val_with(key=term, case_sensitive=case_sensitive)

    def index(self, *, term: str=None, definition: str=None, case_sensitive: bool=True):
        """
        Returns the index of a term or definition if it matches exactly.

        Parameters
        ----------
        term : str, optional if definition is provided.
            Key of the element that is being searched for.
        definition : str, optional if term is provided.
            Value of the element that is being searched for.
        case_sensitive : bool, optional
            Whether case matters.

        Returns
        -------
        int
            Index of the term or definition in the notes_dict.

        Raises
        ------
        ValueError
            If the term or definition is not found within the notes_dict's items.
        """

        return self.notes_dict.index_with(key=term, val=definition, case_sensitive=case_sensitive)

    def terms(self, *, term: str=None, definition: str=None, case_sensitive: bool=True):
        """
        Returns a list of terms that have part of the term name in it or part of the definition in its own definition.

        "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.

        Parameters
        ----------
        term : str, optional if definition is provided.
            Name that may appear in multiple other terms' names.
        definition : str, optional if term is provided.
            Name that may appear in multiple other definitions.
        case_sensitive : bool
            Whether case matters.

        Returns
        -------
        list of term
            All of the terms that corresponded with the term name or definition name.

        Raises
        ------
        ValueError
            If no term had the name in its name or had the definition in its value.
        """

        return self.notes_dict.keys_with(name=term, val=definition, case_sensitive=case_sensitive)

    def definitions(self, *, term: str=None, definition: str=None, case_sensitive: bool=True):
        """
        Returns a list of definitions that have part of the term name as its key or part of the definition name in it.

        "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.

        Parameters
        ----------
        term : str, optional if definition is provided.
            Name of the term that may be in a definition's key.
        definition : str, optional if term is provided.
            Part of a definition that appears in the desired definition.
        case_sensitive : bool
            Whether case matters.

        Returns
        -------
        list of str
            All definitions that had a key that corresponded with term or part of the definition. See IndexedDict.

        Raises
        ------
        ValueError
            If no definition had the definition in its name or had the term in its key.
        """

        return self.notes_dict.vals_with(key=term, name=definition, case_sensitive=case_sensitive)

    def indexes(self, *, term: str=None, definition: str=None, case_sensitive: bool=True):
        """
        Returns the index of a term or definition if it matches exactly.

        "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.

        Parameters
        ----------
        term : str, optional if definition is provided.
            Key of the element that is being searched for.
        definition : str, optional if term is provided.
            Value of the element that is being searched for.
        case_sensitive : bool, optional
            Whether case matters.

        Returns
        -------
        int
            Index of the term or definition in the notes_dict.

        Raises
        ------
        ValueError
            If no items had part of the term in its key or part of the definition in its value.
        """

        return self.notes_dict.indexes_with(key=term, val=definition, case_sensitive=case_sensitive)

    def pair(self, index: int):
        """
        Returns the term and definition of the notes_dict at the provided index.

        Parameters
        ----------
        index : int
            Index of the term and definition in the dictionary.

        Returns
        -------
        str
            term of the notes_dict at the provided index.
        str
            definition of the notes_dict at the provided index.

        If index is out of range (greater than len(notes_dict) or less than 0), raise an IndexError.
        """

        return self.notes_dict.item_at(index)

    def get_pair(self, rand=False):
        """
        Retrieves a pair (term and definition), moving chronologically or randomly.

        Resets to the first (top) pair when all pairs have been retrieved.
        Resets the dict indexes when all of them are used for random generation.

        Parameters
        ----------
        rand : bool
            Whether to return a line from a random index or from chronological order.

        Returns
        -------
        str
            The term of a pair that is either next chronologically or randomly chosen.
        str
            The definition of a pair that is either next chronologically or randomly chosen.
        bool
            Whether the chronological index or random index has repeated.

        Notes
        -----
        Implementation
            0. If a random pair is wanted (rand=True)
                1. Continuously generate random indexes until we find one that is in dict_indexes (unused).
                2. Delete the index from dict_indexes because that index is now used.
                3. If we have used all indexes from dict_indexes, recreate it.
            0. If a line in chronological order is wanted (rand=False)
                1. Get the next line using dict_index
                2. Increment the dict_index
                3. Reset the dict_index if it equals the length of the notes_dict (out of bounds)
            4. Set repeat to True if 3 occurs.
            5. Set the last index retrieved to whichever index was used.
            6. Return the line and if repeat occurred.
        """

        repeat = False
        if rand:
            rand_index = random.randint(0, len(self.notes_dict) - 1)
            while rand_index not in self.dict_indexes:
                rand_index = random.randint(0, len(self.notes_dict) - 1)
            del self.dict_indexes[self.dict_indexes.index(rand_index)]
            if not self.dict_indexes:
                self.dict_indexes = [x for x in range(len(self.notes_dict))]
                repeat = True
            self.last_index = rand_index
            pair = self.pair(rand_index)
        else:
            pair = self.pair(self.dict_index)
            self.last_index = self.dict_index
            self.dict_index += 1
            if self.dict_index == len(self.notes_dict):
                self.dict_index = 0
                repeat = True
        return pair, repeat

    def reset_all(self):
        """
        Resets all indexes except last_index to default.

        Does not reset notes (use make_notes() for that).

        Returns
        -------
        None
        """

        super().reset_all()
        self.dict_index = 0
        self.dict_indexes = [x for x in range(len(self.notes_dict))]

    def reset_chronological(self):
        """
        Resets only the chronological index (line_index) back to 0.

        Returns
        -------
        None
        """

        super().reset_all()
        self.dict_index = 0

    def reset_random(self):
        """
        Resets the list of indexes that have not been randomly retrieved from yet.

        Returns
        -------
        None
        """

        super().reset_random()
        self.dict_indexes = [x for x in range(len(self.notes_dict))]
