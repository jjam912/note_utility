"""
This module contains classes that are used to store data from a file and turn them into usable notes.
"""
import random
import note_format.errors as errors


class NoteUtil:
    """
    Takes a file of notes and converts it into several data structures.

    Keys are used for to_dict().
    Keys that are used for converting to a dictionary:
        KEY_LINE_INDEX : str
        KEY_LINE_INDEXES : str
        KEY_LAST_INDEX : str

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

    Special Methods
    ---------------
        __str__()
            Prints all variables separated by newlines \n.

    """
    KEY_LINE_INDEX = "line_index"
    KEY_LINE_INDEXES = "line_indexes"
    KEY_LAST_INDEX = "last_index"

    def __init__(self, file_name: str, comments: list):
        """
        Creates empty versions of all variables.

        Initialize all variables with the file given.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into NoteUtil.
        comments : list of str
            List of prefixes of lines to be ignored.
        """

        self.notes_list = []
        self.line_index = 0
        self.line_indexes = []
        self.last_index = 0
        self.read_file(file_name, comments)

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

    def read_file(self, file_name: str, comments: list):
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

        Returns
        -------
        None

        Notes
        -----
        Implementation
            0. Open and read the file.
            1. Iterate through each line.
            2. Skip any lines that begin with the 'comments' parameter.
            3. Strip the line.
            4. Check again if the line begins with the 'comments' parameter.
            5. Make the notes list.
            6. When iteration is complete, create line_indexes of the same size as the notes_list.

        Even though this method is used in __init__(), this also a setter method.
        """

        file = open(file_name, mode="r", encoding="UTF-8")
        for line in file.readlines():
            skip = False
            for c in comments:
                if line.startswith(c):
                    skip = True
                    break
            if skip:
                continue
            line = line.strip()
            for c in comments:
                if line.startswith(c):
                    skip = True
                    break
            if skip:
                continue

            if line == "":
                continue
            self.notes_list.append(line)
        self.line_indexes = [x for x in range(len(self.notes_list))]

    def to_dict(self):
        """
        Converts all changeable variables into a dictionary using key constants.

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

    def line(self, index: int):
        """
        Returns a line of text from the notes_list.

        Parameters
        ----------
        index : int
            The index of the line in notes_list.

        Returns
        -------
        str
            The line of text in the notes_list.
        """

        return self.notes_list[index]

    def lines(self, name: str, case_sensitive: bool=False):
        """
        Returns all lines that have the provided name "in" it.

        Uses the "in" operator to compare lines.

        Parameters
        ----------
        name : str
            A part of a line in the notes_list.
        case_sensitive : bool
            Whether case matters.

        Returns
        -------
        list of str
            All lines that had the provided name in it.

        Raises
        ------
        ValueError
            If no lines had the provided name in it.
        """

        lines = []
        if case_sensitive:
            name = name.lower()
        for line in self.notes_list:
            if case_sensitive:
                if name == line.lower():
                    lines.append(line)
            else:
                if name == line:
                    lines.append(line)
        if not lines:
            raise ValueError("No line had the name in it.")
        return lines

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


class IndexedDict(dict):

    def item_at(self, index: int):
        """
        Returns a (key, value) tuple given a specific index in the dictionary.

        Parameters
        ----------
        index : int
            The index of the desired item.

        Returns
        -------
        object
            Key at the given index.
        object
            Value at the given index.

        Raises
        ------
        IndexError
            If index >= len(self.items) or index < 0.
        """

        return list(self.keys())[index], list(self.values())[index]

    def key_at(self, index: int):
        """
        Returns a key given a specific index in the dictionary.

        Parameters
        ----------
        index : int
            The index of the desired key.

        Returns
        -------
        object
            Key at the given index.

        Raises
        ------
        IndexError
            If index >= len(self.items) or index < 0.
        """

        return list(self.keys())[index]

    def val_at(self, index: int):
        """
        Returns a value given a specific index in the dictionary.

        Parameters
        ----------
        index : int
            The index of the desired value.

        Returns
        -------
        object
            Value at the given index.

        Raises
        ------
        IndexError
            If index >= len(self.items) or index < 0.
        """

        return list(self.values())[index]

    def index_with(self, *, key=None, val=None, func=None):
        """
        Returns the first index where the key or value matches exactly as the given key or value.

        Parameters
        ----------
        key : object, optional if value is provided.
            Specific key to look for in the dictionary's keys.
        val : object, optional if key is provided.
            Specific value to look for in the dictionary's values.
        func : function, optional
            Function to apply to dictionary's key or value before comparison of equality.
            Does not affect the provided key or value.

        Returns
        -------
        int
            The first index where the specific key or value was found.

        Raises
        ------
        IndexError
            If the key or value doesn't exist in the dictionary.
        """

        for i, kv in enumerate(self.items()):
            k, v = kv
            if func is not None:
                if key == func(k):
                    return i
                if val == func(v):
                    return i
            elif key == k or val == v:
                return i
        raise IndexError("Equivalent key or value not found in items.")

    def indexes_with(self, *, key=None, val=None, func=None):
        """
        Returns multiple indexes where the provided key or value is "in" a key or value of the dictionary.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        key : object, optional if value is provided.
            Part of a key that exists in the dictionary's keys.
        val : object, optional if key is provided.
            Part of a value that exists in the dictionary's values.
        func : function, optional
            Function to apply to dictionary's key or value before comparison of equality.
            Does not affect the provided key or value.

        Returns
        -------
        list of int
            Multiple indexes where the key or value provided was found in a dictionary's key or value.

        Raises
        ------
        IndexError
            If no keys or values had the provided key or value in them (thus, the list is empty).
        """

        indexes = []
        for i, kv in enumerate(self.items()):
            k, v = kv
            if func is not None:
                try:
                    if key in func(k):
                        indexes.append(i)
                        continue
                except TypeError:
                    if key == func(k):
                        indexes.append(i)
                        continue
                try:
                    if val in func(v):
                        indexes.append(i)
                        continue
                except TypeError:
                    if val == func(v):
                        indexes.append(i)
                        continue
            else:
                try:
                    if key in k:
                        indexes.append(i)
                        continue
                except TypeError:
                    if key == k:
                        indexes.append(i)
                        continue
                try:
                    if val in v:
                        indexes.append(i)
                        continue
                except TypeError:
                    if val == v:
                        indexes.append(i)
                        continue

        if not indexes:
            raise IndexError("No keys or values were found to have the key or value in them.")
        return indexes

    def key_with(self, val, *, func=None):
        """
        Returns the key of a given value if that key's value matches exactly with a key in the dictionary.

        Parameters
        ----------
        val : object
            The value that matches to a dictionary key's value.
        func : function, optional
            Function to apply to the dictionary's value before comparison of equality.
            Does not affect the provided value.

        Returns
        -------
        object
            The first key that has the exact corresponding value.

        Raises
        ------
        KeyError
            If no keys were found to have the exact value provided.
        """

        for k, v in self.items():
            if func is not None:
                if val == func(v):
                    return k
            elif val == v:
                return k
        return KeyError("No key was found to have the name or associated value.")

    def keys_with(self, *, name=None, val=None, func=None):
        """
        Returns the keys that have the given name in the key or the given value in their corresponding value.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        name : object, optional if value is provided.
            The name of the key that are part of the dictionary's keys.
        val : object, optional if name is provided.
            The name of the value that are part of the dictionary's values.
        func : function, optional
            Function to apply to the dictionary's keys and values before comparison of "in" or equality.
            Does not affect the provided name or value.

        Returns
        -------
        list of object
            List of all of the keys that had the name or the value provided in them.

        Raises
        ------
        KeyError
            If no keys were found to have part of the name provided or no values have part of the value provided.
        """

        keys = []
        for i, kv in enumerate(self.items()):
            k, v = kv
            if func is not None:
                try:
                    if name in func(k):
                        keys.append(k)
                        continue
                except TypeError:
                    if name == func(k):
                        keys.append(k)
                        continue
                try:
                    if val in func(v):
                        keys.append(k)
                        continue
                except TypeError:
                    if val == func(v):
                        keys.append(k)
                        continue
            else:
                try:
                    if name in k:
                        keys.append(k)
                        continue
                except TypeError:
                    if name == k:
                        keys.append(k)
                        continue
                try:
                    if val in v:
                        keys.append(k)
                        continue
                except TypeError:
                    if val == v:
                        keys.append(k)
                        continue
        if not keys:
            raise KeyError("No keys were found that had the name or value in them.")
        return keys

    def val_with(self, key, *, func=None):
        """
        Returns the value of a given key if that value's key matches exactly with the dictionary's key.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        key : object
            The key that matches to a value's key exactly.
        func : function, optional
            Function to apply to the dictionary's key before comparison of equality.
            Does not affect the provided key.

        Returns
        -------
        object
            The first value that has the exact corresponding key.

        Raises
        ------
        ValueError
            If no values were found to have the exact key provided.
        """

        for k, v in self.items():
            if func is not None:
                if key == func(k):
                    return v
            elif key == k:
                return v
        raise ValueError("No values were found to have the name or associated key.")

    def vals_with(self, *, key=None, name=None, func=None):
        """
        Returns the values that have the given name in the value or the given key in their corresponding key.

        Parameters
        ----------
        key : object, optional if name is provided.
            The name of the key that is part of the dictionary's keys.
        name : object, optional if key is provided.
            The name of the value that is part of the dictionary's values.
        func : function, optional
            Function to apply to the dictionary's key and value before comparison of "in" or equality.
            Does not affect the provided key or name.

        Returns
        -------
        list of object
            List of all of the values that had the name provided in them or the key name in their corresponding key.

        Raises
        ------
        ValueError
            If no values were found to have part of the name provided or no keys have part of the key provided.
        """

        vals = []
        for i, kv in enumerate(self.items()):
            k, v = kv
            if func is not None:
                try:
                    if key in func(k):
                        vals.append(v)
                        continue
                except TypeError:
                    if key == func(k):
                        vals.append(v)
                        continue
                try:
                    if name in func(v):
                        vals.append(v)
                        continue
                except TypeError:
                    if name == func(v):
                        vals.append(v)
                        continue
            else:
                try:
                    if key in k:
                        vals.append(v)
                        continue
                except TypeError:
                    if key == k:
                        vals.append(v)
                        continue
                try:
                    if name in v:
                        vals.append(v)
                        continue
                except TypeError:
                    if name == v:
                        vals.append(v)
                        continue
        if not vals:
            raise ValueError("No values were found to have the name or associated key in them.")
        return vals


class PairedNoteUtil(NoteUtil):
    """
    Splits all lines in notes_list into key, value pairs known as terms and definitions.

    Terms and definitions are separated by delimeters, which occur only once in each line but can be any character.
    Creates a dictionary out of all of the terms and definitions by splitting by the delimeter.

    Keys are used for to_dict().
    Keys that are used for converting to a dictionary.
        KEY_DICT_INDEX : str
        KEY_DICT_INDEXES : str

    Attributes
    ----------
        delimeter : str
            The character that separates terms from definitions.
        notes_paired : IndexedDict of {str: str}
            IndexedDict (see mydas.py) created from splitting each element in notes_list with the delimeter.
        pair_index : int
            Chronological index of the next pair of term and definitions.
        pair_indexes : list of int
            Keep tracks of what pairs (terms and definitions) have been used.
            Used to make sure terms are not repeating.

    Special Methods
    ---------------
        __str__()
            Prints all variables separated by newlines \n.

    """

    KEY_DICT_INDEX = "dict_index"
    KEY_DICT_INDEXES = "dict_indexes"

    def __init__(self, file_name: str, comments: list, delimeter: str, skip_warnings=False):
        """
        Initialize all variables with the file given.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into PairedNoteUtil.
        comments : list of str
            The prefixes of lines that will be ignored, checked both before and after strip.
        delimeter : str
            The character that separates the key from the value, or the term from the definition.

        """

        super().__init__(file_name, comments)
        self.delimeter = delimeter
        self.notes_paired = IndexedDict()
        self.pair_index = 0
        self.pair_indexes = []
        self.make_notes_paired(skip_warnings)

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

        message += "Notes paired: " + str(self.notes_paired) + "\n"

        message += "Dict index: " + str(self.pair_index) + "\n"
        message += "Dict indexes: " + str(self.pair_indexes) + "\n"

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
        notes[self.KEY_DICT_INDEX] = self.pair_index
        notes[self.KEY_DICT_INDEXES] = self.pair_indexes
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
        noteutil.pair_index = var_dict[PairedNoteUtil.KEY_DICT_INDEX]
        noteutil.pair_indexes = var_dict[PairedNoteUtil.KEY_DICT_INDEXES]

    def make_notes_paired(self, skip_warnings=False):
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
                4. Before assigning the term to the definition, we .strip() the term and definition
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

        error_message = ""
        self.notes_paired = IndexedDict()

        for i in range(len(self.notes_list)):
            try:
                try:
                    self.notes_list[i] = self.notes_list[i].split(self.delimeter)
                except AttributeError:
                    # List has already been split
                    pass

                if len(self.notes_list[i]) > 2:
                    raise errors.ExtraDelimeterError
                elif len(self.notes_list[i]) == 1:
                    raise errors.MissingDelimeterError

                self.notes_list[i][0] = self.notes_list[i][0].strip()
                self.notes_list[i][1] = self.notes_list[i][1].strip()

                term, definition = self.notes_list[i]

                if definition == "":
                    raise errors.NoDefinitionError

                self.notes_paired[term] = definition

            except errors.ExtraDelimeterError:
                error_message += "WARNING: Extra delimeter at around line " + str(i+1) + ". "
                error_message += "Pair: " + str(self.notes_list[i]) + "\n"
            except errors.MissingDelimeterError:
                error_message += "WARNING: Missing delimeter at around line " + str(i+1) + ". "
                error_message += "Pair: " + str(self.notes_list[i]) + "\n"
            except errors.NoDefinitionError:
                error_message += "WARNING: Missed pairing at around line " + str(i+1) + ". "
                error_message += "Pair: " + str(self.notes_list[i]) + "\n"

        if error_message != "" and not skip_warnings:
            print("Warnings: (All pairs with warnings have been skipped)\n" + error_message)

        self.pair_indexes = [x for x in range(len(self.notes_paired))]

    def term(self, *, index: int=None, definition: str=None, case_sensitive: bool=False):
        """
        Returns a list of terms that matches exactly with the given definition.

        Parameters
        ----------
        index : int, optional if definition is provided.
            Index of the term.
        definition : str, optional if index is provided.
            Name that matches a definition in notes_dict.
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

        if index is not None:
            return self.notes_paired.key_at(index)
        if not case_sensitive:
            return self.notes_paired.key_with(definition.lower() if definition is not None else definition,
                                              func=str.lower)
        return self.notes_paired.key_with(val=definition)

    def definition(self, *, index: int=None, term: str=None, case_sensitive: bool=False):
        """
        Returns a list of definitions that have part of the term name as its key or part of the definition name in it.

        Parameters
        ----------
        index : int, optional if term is provided.
            Index of the definition.
        term : str, optional if index is provided.
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

        if index is not None:
            return self.notes_paired.val_at(index)
        if not case_sensitive:
            return self.notes_paired.val_with(key=term.lower() if term is not None else term,
                                              func=str.lower)
        return self.notes_paired.val_with(key=term)

    def index(self, *, term: str=None, definition: str=None, case_sensitive: bool=False):
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

        if not case_sensitive:
            return self.notes_paired.index_with(key=term.lower() if term is not None else term,
                                                val=definition.lower() if definition is not None else definition,
                                                func=str.lower)
        return self.notes_paired.index_with(key=term, val=definition)

    def terms(self, *, term: str=None, definition: str=None, case_sensitive: bool=False):
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

        if not case_sensitive:
            return self.notes_paired.keys_with(name=term.lower() if term is not None else term,
                                               val=definition.lower() if definition is not None else definition,
                                               func=str.lower)
        return self.notes_paired.keys_with(name=term, val=definition)

    def definitions(self, *, term: str=None, definition: str=None, case_sensitive: bool=False):
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

        if not case_sensitive:
            return self.notes_paired.vals_with(key=term.lower() if term is not None else term,
                                               name=definition.lower() if definition is not None else definition,
                                               func=str.lower)
        return self.notes_paired.vals_with(key=term, name=definition)

    def indexes(self, *, term: str=None, definition: str=None, case_sensitive: bool=False):
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

        if not case_sensitive:
            return self.notes_paired.indexes_with(key=term if term is not None else term,
                                                  val=definition.lower() if definition is not None else definition,
                                                  func=str.lower)
        return self.notes_paired.indexes_with(key=term, val=definition)

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

        return self.notes_paired.item_at(index)

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
            6. Return the term, definition, and if repeat occurred.
        """

        repeat = False
        if rand:
            rand_index = random.randint(0, len(self.notes_paired) - 1)
            while rand_index not in self.pair_indexes:
                rand_index = random.randint(0, len(self.notes_paired) - 1)
            del self.pair_indexes[self.pair_indexes.index(rand_index)]
            if not self.pair_indexes:
                self.pair_indexes = [x for x in range(len(self.notes_paired))]
                repeat = True
            self.last_index = rand_index
            pair = self.pair(rand_index)
        else:
            pair = self.pair(self.pair_index)
            self.last_index = self.pair_index
            self.pair_index += 1
            if self.pair_index == len(self.notes_paired):
                self.pair_index = 0
                repeat = True
        return pair[0], pair[1], repeat

    def reset_all(self):
        """
        Resets all indexes except last_index to default.

        Does not reset notes (use make_notes() for that).

        Returns
        -------
        None
        """

        super().reset_all()
        self.pair_index = 0
        self.pair_indexes = [x for x in range(len(self.notes_paired))]

    def reset_chronological(self):
        """
        Resets only the chronological index back to 0.

        Returns
        -------
        None
        """

        super().reset_all()
        self.pair_index = 0

    def reset_random(self):
        """
        Resets the list of indexes that have not been randomly retrieved from yet.

        Returns
        -------
        None
        """

        super().reset_random()
        self.pair_indexes = [x for x in range(len(self.notes_paired))]


class CategorizedNoteUtil(PairedNoteUtil):

    def __init__(self, file_name: str, comments: list, delimeter: str,
                 *, generics: list=None, positionals: list=None, extensions: list=None,
                 ignore_generics: bool=False, filter_extensions: bool=True):

        super().__init__(file_name, comments, delimeter, skip_warnings=True)

        self.positionals = positionals
        self.generics = generics
        self.extensions = extensions

        self.notes_categorized = IndexedDict()
        self.exclusive_dict = IndexedDict()
        self.generic_dict = IndexedDict()

        if positionals is not None:
            for name, prefix in positionals:
                self.exclusive_dict[name] = IndexedDict()
                self.exclusive_dict["Uncategorized"] = IndexedDict()
        if generics is not None:
            for name, prefix in generics:
                self.generic_dict[name] = IndexedDict()

        self.make_notes_categorized(ignore_generics, filter_extensions)
        self.make_notes_paired(skip_warnings=False)

    def __str__(self):
        message = super().__str__() + "\n"
        message += "CategorizedNoteUtil: \n"
        message += "Positionals: " + str(self.positionals) + "\n"
        message += "Generics: " + str(self.generics) + "\n"
        message += "Extensions: " + str(self.extensions) + "\n"

        message += "Generic dict: " + str(self.generic_dict) + "\n"
        message += "Positional dict: " + str(self.exclusive_dict) + "\n"
        message += "Notes categorized: " + str(self.notes_categorized) + "\n"

        return message

    def to_dict(self):
        notes = super().to_dict()

    @staticmethod
    def parse_dict(noteutil, var_dict: dict):
        pass

    def make_notes_categorized(self, ignore_generics: bool=False, filter_extensions: bool=True, skip_warnings=False):

        error_message = ""

        if self.extensions is not None:
            for i in range(len(self.notes_list)):
                if len(self.notes_list[i]) == 2:
                    orig_len = len(self.notes_list[i][1])
                    for nb in self.extensions:
                        name, bound1, bound2 = None, None, None
                        if len(nb) == 2:
                            name, bound1 = nb
                            bound2 = bound1
                        elif len(nb) == 3:
                            name, bound1, bound2 = nb
                        while True:     # There could be multiple extensions of a single name.
                            try:
                                try:
                                    b1 = self.notes_list[i][1].index(bound1, 0, orig_len)
                                except ValueError:
                                    # No extension for this term, just pass
                                    break
                                try:
                                    b2 = self.notes_list[i][1].index(bound2, b1 + 1, orig_len)
                                except ValueError:
                                    # Only one bound is probably an error
                                    raise errors.MissingBoundError
                                self.notes_list[i][1] += "\n" + name + self.delimeter + " " + \
                                                         self.notes_list[i][1][b1 + len(bound1): b2]
                                if filter_extensions:
                                    self.notes_list[i][1] = self.notes_list[i][1][:b1] + \
                                                            self.notes_list[i][1][b2 + len(bound2):]
                                    orig_len -= (b2 - b1 + len(bound1))
                                self.notes_list[i][1] = self.notes_list[i][1].strip()
                            except errors.MissingBoundError:
                                error_message += "WARNING: Missed bound at around line " + str(i+1) + ".\n"
                                error_message += "Pair: " + str(self.notes_list[i])
                                break

        if self.generics is not None:
            for i in range(len(self.notes_list) - 1, -1, -1):

                if len(self.notes_list[i]) != 2:
                    continue

                for n, p in self.generics:
                    if self.notes_list[i][0].startswith(p):
                        self.notes_list[i][0] = self.notes_list[i][0][len(p):].strip()
                        self.generic_dict[n][self.notes_list[i][0]] = self.notes_list[i][1]
                        if ignore_generics:
                            del self.notes_list[i]

        if self.positionals is not None:
            name, prefix, curr = None, None, None
            for i in range(len(self.notes_list)):

                for n, p in self.positionals[::-1]:
                    if self.notes_list[i][0].startswith(p):
                        name, prefix, curr = n, p, self.notes_list[i][0][len(p):].strip()
                        self.exclusive_dict[name][curr] = IndexedDict()
                        break
                else:
                    if len(self.notes_list[i]) != 2:
                        continue
                    if name is None or prefix is None:
                        self.exclusive_dict["Uncategorized"][self.notes_list[i][0]] = self.notes_list[i][1]
                    else:
                        self.exclusive_dict[name][curr][self.notes_list[i][0]] = self.notes_list[i][1]

            for name in self.exclusive_dict.keys():
                if name == "Uncategorized":
                    continue
                for category in self.exclusive_dict[name].keys():
                    self.notes_categorized[category] = IndexedDict()

            self.notes_categorized["Uncategorized"] = self.exclusive_dict["Uncategorized"]

            for name, prefix in self.positionals:
                curr = None
                for i in range(len(self.notes_list)):
                    if self.notes_list[i][0].startswith(prefix):
                        for n, p in self.positionals[::-1]:
                            if n == name:
                                curr = self.notes_list[i][0][len(prefix):].strip()
                                break
                            elif self.notes_list[i][0].startswith(p):
                                if p.startswith(prefix):
                                    break
                        continue
                    else:
                        for n, p in self.positionals[::-1]:
                            if self.notes_list[i][0].startswith(p):
                                if p != prefix and not p.startswith(prefix):
                                    curr = None
                        if len(self.notes_list[i]) != 2:
                            continue
                        elif curr is None:
                            continue
                        else:
                            self.notes_categorized[curr][self.notes_list[i][0]] = self.notes_list[i][1]

        for i in range(len(self.notes_list) - 1, -1, -1):
            for n, p in self.positionals:
                if self.notes_list[i][0].startswith(p):
                    del self.notes_list[i]

        if error_message != "" and not skip_warnings:
            print("Warnings: ( All pairs with warnings have been skipped)\n" + error_message)

    def generic(self, name: str, case_sensitive: bool=False):
        pass

    def category(self, name: str, case_sensitive: bool=False):
        pass

    def excategory(self, name: str, case_sensitive: bool=False):
        pass

    def generics(self, name: str, case_sensitive: bool=False):
        pass

    def categories(self, name: str, case_sensitive: bool=False):
        pass

    def excategories(self, name: str, case_sensitive: bool=False):
        pass


noteutil = CategorizedNoteUtil("test_notes2.txt", ["#"], ":",
                               positionals=[("Periods", "~"), ("Chapters", "~~")])

# noteutil = CategorizedNoteUtil("test_notes.txt", ["#"], ":", generics=[("Important", "!")],
#                                positionals=[("Cat1", "~"), ("Cat2", "~~")],
#                                extensions=[("Decimal", "%")], ignore_generics=False, filter_extensions=True)

print(noteutil)








