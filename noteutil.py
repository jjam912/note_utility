"""
This module contains classes that are used to store data from a file and turn them into usable notes.
"""
import note_utility.errors as errors
import copy


class NoteUtil:
    """
    Takes a file of notes and converts it into a list of notes.

    Attributes
    ----------
        notes_list : list of str
            List created after splitting file contents.

    Special Methods
    ---------------
        __str__()
            Prints all variables separated by new lines.
    """

    def __init__(self, file_name: str, comments: list=None):
        """
        Creates empty versions of all variables.

        Initialize all variables with the file given.

        Parameters
        ----------
        file_name : str
            Name of the file to be converted into NoteUtil.
        comments : list of str, optional
            List of prefixes of lines to be ignored.
        """

        self.notes_list = []
        self._read_file(file_name, comments)

    def __str__(self):
        """
        Converts all variables into strings.

        Returns
        -------
        str
            All variables with labels, separated by new lines.
        """

        message = "NoteUtil:\n"

        message += "Notes list: " + str(self.notes_list) + "\n"
        return message

    def _read_file(self, file_name: str, comments: list=None):
        """
        Converts all the data from the file into a list of notes.

        If a line contains nothing (possibly after strip), the line will be ignored.

        Parameters
        ----------
        file_name : str
            Name of the file to extract data from.
        comments : str, optional
            Prefix of lines to be ignored.
            Having '' in this list will skip all lines.

        Returns
        -------
        None
        """

        self.notes_list = []
        file = open(file_name, mode="r", encoding="UTF-8")
        for line in file.readlines():
            skip = False

            if comments is not None:
                for c in comments:
                    if line.startswith(c):
                        skip = True
                        break

            line = line.strip()

            if comments is not None and not skip:
                for c in comments:
                    if line.startswith(c):
                        skip = True
                        break

            if line == "" or skip:
                continue
            self.notes_list.append(line)

    def line_index(self, name: str, *, notes_list: list=None, case_sensitive: bool=False):
        """
        Finds the index of a line in a notes list.

        Parameters
        ----------
        name : str
            The name of the full line.
        notes_list : list, optional
            A list of notes that should contain the line that is being searched for.
            Default list is self.notes_list (made from the file).
        case_sensitive : bool, optional
            Whether case matters while searching for the line.

        Returns
        -------
        int
            Index of the line in the notes list provided.

        Raises
        ------
        NotesNotFoundError
            If no line is found to be equivalent to the name given.
        """

        if notes_list is None:
            notes_list = self.notes_list
        if not case_sensitive:
            insensitive_notes_list = list(map(str.lower, notes_list))
            for i in range(len(insensitive_notes_list)):
                if name == insensitive_notes_list[i]:
                    return i
        else:
            for i in range(len(notes_list)):
                if name == notes_list[i]:
                    return i
        raise errors.NotesNotFoundError

    def line_indexes(self, name: str, *, notes_list: list=None, case_sensitive: bool=False):
        """
        Finds the index of all lines that have the name in them.

        Parameters
        ----------
        notes_list : list
            A list of notes that should contain the lines being searched for.
            Default list is self.notes_list (made from the file).
        name : str
            A name that may be part of a line or the entire line.
        case_sensitive : bool
            Whether case matters while searching for lines.

        Returns
        -------
        list of int
            All indexes that were matched with the name.

        Raises
        ------
        NotesNotFoundError
            If no line is found to be equivalent to the name given.
        """

        indexes = []
        if notes_list is None:
            notes_list = self.notes_list
        if not case_sensitive:
            insensitive_notes_list = list(map(str.lower, notes_list))
            for i in range(len(insensitive_notes_list)):
                if name in insensitive_notes_list[i]:
                    indexes.append(i)
        if not indexes:
            raise errors.NotesNotFoundError
        return indexes

    def line(self, *, notes_list: list=None, index: int=None, name: str=None, case_sensitive: bool=False):
        """
        Returns a line of text from the notes_list.

        Parameters
        ----------
        notes_list : list of str, optional - default is self.notes_list
            A list of notes
        index : int
            The index of the line in notes_list.
        name : str
            The name of the line in notes_list
        case_sensitive : bool
            Whether case matters

        Returns
        -------
        str
            The line of text in the notes_list.

        Raises
        ------
        NotesNotFoundError
            If no lines are found to be equivalent to the name provided.
        """

        if notes_list is None:
            notes_list = self.notes_list

        if index is not None:
            return notes_list[index]
        if name is not None:
            if not case_sensitive:
                insensitive_notes_list = map(str.lower, notes_list)
                if name in insensitive_notes_list:
                    return name
                else:
                    raise errors.NotesNotFoundError
            else:
                if name in notes_list:
                    return name
                else:
                    raise errors.NotesNotFoundError

    def lines(self, *, notes_list: list=None, indexes: list=None, name: str=None, case_sensitive: bool=False):
        """
        Returns all lines that have the provided name "in" it.

        Uses the "in" operator to compare lines.

        Parameters
        ----------
        notes_list : list of str, optional - default is self.notes_list
            A list of notes.
        indexes : list of int
            Indexes of lines.
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
        NotesNotFoundError
            If no lines had the provided name in it.
        """

        if notes_list is None:
            notes_list = self.notes_list
        lines = []
        for i, line in enumerate(notes_list):
            if not case_sensitive:
                if name.lower() in line.lower():
                    lines.append(line)
                    continue
            else:
                if name in line:
                    lines.append(line)
                    continue
            if indexes is not None:
                for j in indexes:
                    if i == j:
                        lines.append(line)
                        continue

        if not lines:
            raise errors.NotesNotFoundError
        return lines


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
            If index >= len(self.items).
        """

        return list(self.keys())[index], list(self.values())[index]

    def items_at(self, indexes: list):
        """
        Returns a list of (key, value) tuples at the provided indexes.

        Parameters
        ----------
        indexes : list of int
            All indexes of items that are wanted.

        Returns
        -------
        list of tuple(object, object)
            All items in the (key, value) pairing.

        Raises
        ------
        IndexError
            If one of the indexes in the list is >= len(self.items).
        """

        indexed_items = []
        for i in indexes:
            indexed_items.append(self.item_at(i))
        return indexed_items

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

    def key_with(self, *, index=None, name=None, val=None, func=None):
        """
        Returns the key of a given value if that key's value matches exactly with a key in the dictionary.

        Parameters
        ----------
        index : int, optional if val is provided.
            The index of the key
        name : object
            The name of the key that may equal the key after func is applied.
        val : object, optional if index is provided.
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
        i = 0
        for k, v in self.items():
            if func is not None:
                if name == func(k) or val == func(v) or index == i:
                    return k
            elif val == v or name == k or index == i:
                return k
            i += 1
        raise KeyError("No key was found to have the name or associated value.")

    def keys_with(self, *, indexes: list=None, name=None, val=None, func=None):
        """
        Returns the keys that have the given name in the key or the given value in their corresponding value.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        indexes: list of int, optional if name or value is provided.
            Indexes of keys.
        name : object, optional if indexes or value is provided.
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

            if indexes is not None:
                if i in indexes:
                    keys.append(k)
                    continue

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

    def val_with(self, *, index=None, key=None, name=None, func=None):
        """
        Returns the value of a given key if that value's key matches exactly with the dictionary's key.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        index : int, optional if key is provided.
            Index of a key.
        key : object
            The key that matches to a value's key exactly.
        name : object
            The name of the value that may equal the val after func is applied.
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

        i = 0
        for k, v in self.items():
            if func is not None:
                if key == func(k) or name == func(v) or index == i:
                    return v
            elif key == k or name == v or index == i:
                return v
            i += 1
        raise ValueError("No values were found to have the name or associated key.")

    def vals_with(self, *, indexes: list=None, key=None, name=None, func=None):
        """
        Returns the values that have the given name in the value or the given key in their corresponding key.

        Parameters
        ----------
        indexes : list of int
            Indexes of values that are wanted.
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

            if indexes is not None:
                if i in indexes:
                    vals.append(v)
                    continue

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

    Attributes
    ----------
        delimeter : str
            The character that separates terms from definitions.
        notes_paired : IndexedDict of {str: str}
            IndexedDict created from splitting each element in notes_list with the delimeter.
        error_message : str
            Any errors that occurred while creating the paired notes.
    Special Methods
    ---------------
        __str__()
            Prints all variables separated by new lines.
    """

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
        self.error_message = ""
        self.delimeter = delimeter

        self.notes_split = self.notes_list.copy()
        self.notes_paired = IndexedDict()
        self._split_terms()
        self._make_notes_paired()

        if not skip_warnings:
            print(self.error_message)

    def __str__(self):
        """
        Converts all variables into strings.

        Returns
        -------
        str
            All variables with labels separated by new lines.
        """

        message = super().__str__() + "\n"
        message += "PairedNoteUtil:\n"
        message += "Delimeter: " + self.delimeter + "\n"

        message += "Notes split: " + str(self.notes_split) + "\n"
        message += "Notes paired: " + str(self.notes_paired) + "\n"
        return message

    def _split_terms(self):
        """
        Separates all terms in notes_list by splitting using the delimeter.

        This makes notes_list into a List[List[str]]

        Returns
        -------
        None
        """

        self.notes_split = self.notes_list.copy()
        for i in range(len(self.notes_split)):
            try:
                self.notes_split[i] = self.notes_split[i].split(self.delimeter)
            except AttributeError:  # List has already been split
                pass

            self.notes_split[i][0] = self.notes_split[i][0].strip()
            if len(self.notes_split[i]) == 2:
                self.notes_split[i][1] = self.notes_split[i][1].strip()

    def _make_notes_paired(self, notes_split: list=None):
        """
        Creates a IndexedDict based off the notes_list created in NoteUtil.

        If we want to create a new dictionary from a new file, we must first read_file()
            before calling this or recreate a PairedNoteUtil.

        Parameters
        ----------
        notes_split : list of list [str, str]
            A list of terms and definitions - (as a list).

        Returns
        -------
        None
        """

        self.notes_paired = IndexedDict()

        if notes_split is None:
            notes_split = self.notes_split
        for i in range(len(notes_split)):
            try:
                if len(notes_split[i]) > 2:
                    raise errors.ExtraDelimeterError
                elif len(notes_split[i]) == 1:
                    raise errors.MissingDelimeterError

                term, definition = notes_split[i]

                if definition == "":
                    raise errors.NoDefinitionError

                if term in self.notes_paired:
                    raise errors.DuplicateTermError

                self.notes_paired[term] = definition

            except errors.ExtraDelimeterError:
                self.error_message += "WARNING: Extra delimeter at around line " + str(i+1) + ". "
                self.error_message += "Pair: " + str(notes_split[i]) + "\n"
            except errors.MissingDelimeterError:
                self.error_message += "WARNING: Missing delimeter at around line " + str(i+1) + ". "
                self.error_message += "Pair: " + str(notes_split[i]) + "\n"
            except errors.NoDefinitionError:
                self.error_message += "WARNING: Missed pairing at around line " + str(i+1) + ". "
                self.error_message += "Pair: " + str(notes_split[i]) + "\n"
            except errors.DuplicateTermError:
                self.error_message += "WARNING: Duplicate term at around line " + str(i+1) + ". "
                self.error_message += "Pair: " + str(notes_split[i]) + "\n"

    def term(self, *, notes_dict: IndexedDict=None,
             index: int=None, term: str=None, definition: str=None, func=str.lower):
        """
        Returns a list of terms that matches exactly with the given definition.

        Parameters
        ----------
        notes_dict : IndexedDict
            Any IndexedDict that contains terms and definitions.
        index : int, optional if definition is provided.
            Index of the term.
        term : str
            A name of the term that may not match exactly (cases).
        definition : str, optional if index is provided.
            Name that matches a definition in notes_dict.
        func : function
            Function to apply to the notes_dict term and definition. Default is lower case.
            Will also apply to term and definition if they are not None.

        Returns
        -------
        str
            First term that corresponded with the term name or definition name.

        Raises
        ------
        NotesNotFoundError
            If the provided term or definition is not found within the notes_dict's keys and values.
        """

        if notes_dict is None:
            notes_dict = self.notes_paired
        try:
            if index is not None:
                return notes_dict.key_with(index=index)
            if func:
                return notes_dict.key_with(name=func(term) if term is not None else term,
                                           val=func(definition) if definition is not None else definition,
                                           func=func)
            return notes_dict.key_with(name=term, val=definition)
        except KeyError:
            raise errors.NotesNotFoundError

    def definition(self, *, notes_dict: IndexedDict=None,
                   index: int=None, term: str=None, definition: str=None, func=str.lower):
        """
        Returns a list of definitions that have part of the term name as its key or part of the definition name in it.

        Parameters
        ----------
        notes_dict : IndexedDict
            Any IndexedDict that contains terms and definitions.
        index : int, optional if term is provided.
            Index of the definition.
        term : str, optional if index is provided.
            Name of the term that may be in a definition's key.
        definition : str
            The name of the definition that may not match exactly (cases).
        func : function
            Function to apply to the notes_dict term and definition. Default is lower case.
            Will also apply to term and definition if they are not None.

        Returns
        -------
        str
            A definition that had a key that corresponded with term or the definition. See IndexedDict.

        Raises
        ------
        NotesNotFoundError
            If the provided term or definition is not found within the notes_dict's keys or values.
        """

        if notes_dict is None:
            notes_dict = self.notes_paired
        try:
            if index is not None:
                return notes_dict.val_with(index=index)
            if func:
                return notes_dict.val_with(key=func(term) if term is not None else term,
                                           name=func(term) if definition is not None else definition,
                                           func=func)
            return notes_dict.val_with(key=term)
        except ValueError:
            raise errors.NotesNotFoundError

    def pair_index(self, *, notes_dict: IndexedDict=None,
                   term: str=None, definition: str=None, func=str.lower):
        """
        Returns the index of a term or definition if it matches exactly.

        Parameters
        ----------
        notes_dict : IndexedDict
            Any IndexedDict that contains terms and definitions.
        term : str, optional if definition is provided.
            Key of the element that is being searched for.
        definition : str, optional if term is provided.
            Value of the element that is being searched for.
        func : function
            Function to apply to the notes_dict term and definition. Default is lower case.
            Will also apply to term and definition if they are not None.

        Returns
        -------
        int
            Index of the term or definition in the notes_dict.

        Raises
        ------
        NotesIndexError
            If the index is out of range (and thus no terms or definitions are found).
        """

        if notes_dict is None:
            notes_dict = self.notes_paired
        try:
            if func:
                return notes_dict.index_with(key=func(term) if term is not None else term,
                                             val=func(definition) if definition is not None else definition,
                                             func=func)
            return notes_dict.index_with(key=term, val=definition)
        except IndexError:
            raise errors.NotesIndexError

    def terms(self, *, notes_dict: IndexedDict=None,
              indexes: list=None, term: str=None, definition: str=None, func=str.lower):
        """
        Returns a list of terms that have part of the term name in it or part of the definition in its own definition.

        "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.

        Parameters
        ----------
        notes_dict : IndexedDict
            Any IndexedDict that contains terms and definitions.
        indexes : list of int, optional if term or definition is provided.
            Indexes of terms to be added.
        term : str, optional if indexes or definition is provided.
            Name that may appear in multiple other terms' names.
        definition : str, optional if indexes or term is provided.
            Name that may appear in multiple other definitions.
        func : function
            Function to apply to the notes_dict term and definition. Default is lower case.
            Will also apply to term and definition if they are not None.

        Returns
        -------
        list of str
            All of the terms that corresponded with the term name or definition name.

        Raises
        ------
        NotesNotFoundError
            If no term had the name in its name or had the definition in its value.
        """

        if notes_dict is None:
            notes_dict = self.notes_paired
        try:
            if func:
                return notes_dict.keys_with(indexes=indexes,
                                            name=func(term) if term is not None else term,
                                            val=func(definition) if definition is not None else definition,
                                            func=func)
            return notes_dict.keys_with(indexes=indexes, name=term, val=definition)
        except KeyError:
            raise errors.NotesNotFoundError

    def definitions(self, *, notes_dict: IndexedDict=None,
                    indexes: list=None, term: str=None, definition: str=None, func=str.lower):
        """
        Returns a list of definitions that have part of the term name as its key or part of the definition name in it.

        "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.

        Parameters
        ----------
        notes_dict : IndexedDict
            Any IndexedDict that contains terms and definitions.
        indexes : list of int
            Indexes of terms to be added.
        term : str, optional if definition is provided.
            Name of the term that may be in a definition's key.
        definition : str, optional if term is provided.
            Part of a definition that appears in the desired definition.
        func : function
            Function to apply to the notes_dict term and definition. Default is lower case.
            Will also apply to term and definition if they are not None.

        Returns
        -------
        list of str
            All definitions that had a key that corresponded with term or part of the definition. See IndexedDict.

        Raises
        ------
        NotesNotFoundError
            If no definition had the definition in its name or had the term in its key.
        """

        if notes_dict is None:
            notes_dict = self.notes_paired
        try:
            if func:
                return notes_dict.vals_with(indexes=indexes,
                                            key=func(term) if term is not None else term,
                                            name=func(term) if definition is not None else definition,
                                            func=func)
            return notes_dict.vals_with(indexes=indexes, key=term, name=definition)
        except ValueError:
            raise errors.NotesNotFoundError

    def pair_indexes(self, *, notes_dict: IndexedDict=None,
                     term: str=None, definition: str=None, func=str.lower):
        """
        Returns the index of a term or definition if it is part of a key or definition in the paired notes.

        "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.

        Parameters
        ----------
        notes_dict : IndexedDict
            Any IndexedDict that contains terms and definitions.
        term : str, optional if definition is provided.
            Key of the element that is being searched for.
        definition : str, optional if term is provided.
            Value of the element that is being searched for.
        func : function
            Function to apply to the notes_dict term and definition. Default is lower case.
            Will also apply to term and definition if they are not None.

        Returns
        -------
        int
            Index of the term or definition in the notes_dict.

        Raises
        ------
        NotesIndexError
            If all indexes were out of range of the IndexedDict and no items were found.
        """

        if notes_dict is None:
            notes_dict = self.notes_paired
        try:
            if func:
                return notes_dict.indexes_with(key=func(term) if term is not None else term,
                                               val=func(definition) if definition is not None else definition,
                                               func=func)
            return notes_dict.indexes_with(key=term, val=definition)
        except IndexError:
            raise errors.NotesIndexError

    def pair(self, index: int, *, notes_dict: IndexedDict=None):
        """
        Returns the term and definition of the notes_dict at the provided index.

        Parameters
        ----------
        index : int
            Index of the term and definition in the dictionary.
        notes_dict : IndexedDict
            Any IndexedDict that contains terms and definitions.

        Returns
        -------
        str
            term of the notes_dict at the provided index.
        str
            definition of the notes_dict at the provided index.

        Raises
        ------
        NotesIndexError
            If the provided index is out of range of the IndexedDict.
        """

        if notes_dict is None:
            notes_dict = self.notes_paired
        try:
            return notes_dict.item_at(index)
        except IndexError:
            raise errors.NotesIndexError

    def pairs(self, indexes: list, *, notes_dict: IndexedDict=None):
        """
        Returns a list of (key, value) tuples that represent term and definition pairs.

        Parameters
        ----------
        indexes : list of int
            Indexes of the pairs.
        notes_dict : IndexedDict
            Any IndexedDict that contains terms and definitions.

        Returns
        -------
        list of tuple(str, str)
            The list of term and definition pairs.

        Raises
        ------
        NotesIndexError
            If one of the indexes are out of range of the IndexedDict.
        """

        if notes_dict is None:
            notes_dict = self.notes_paired
        try:
            return notes_dict.items_at(indexes)
        except IndexError:
            raise errors.NotesIndexError


class CategorizedNoteUtil(PairedNoteUtil):
    """
    Uses prefixes to separate notes into categories, of which are either positional or generic.

    Definitions may contain additional information, known as extensions, which are separated by new lines.
        Extensions must be surrounded by given characters.

    Generic terms are added to a category based on a generic prefix.
    The position of generic terms do not matter and they will never be nested within another generic term.

    Positional terms are added to a category based on their relative position in notes.
    In order to nest positional terms,
        the term must have a prefix of a previous positional prefix with its own additional prefix.

    Attributes
    ----------
    error_message : str
        Any errors that occur while making categorized notes.
    extensions : list of tuple of either (str, str) or (str, str, str).
        Each extension is a group of (name, surrounding character(s)) or (name, beginning character, ending character).
        When an extension is found in a definition, it will be added to the end of the string, separated by a \n
        Extensions can then optionally be removed from the main definition.
    generics : list of tuple of (str, str).
        Each generic is a group of (name, prefix).
        The name is independent of the terms themselves.
        The position of generics do not matter, only that it starts with the prefix.
    positionals : list of tuple of (str, str).
        Each positional is a group of (name, prefix).
        The name is independent of the term name itself.
        Any terms with specifically that prefix will be added to the value of the name.

    generic_dict : IndexedDict
        A dictionary with keys of generic names and values of IndexedDicts of note pairs.
        Each generic's name in generics serves as a key and the values are the note pairs as an IndexedDict.
    extension_dict : IndexedDict
        A dictionary with keys of each extension name and values of IndexedDicts.
        Each dictionary will have terms that have the extension in their definition.
    positional_dict : IndexedDict
        A dictionary with keys of each positional name and values of IndexedDicts.
        The positional dict ignores any nesting of prefixes.
        The note pairs in positional dict are pairs that are exclusive only to that name and prefix.
        An "Uncategorized" category contains all note pairs that do not have a category above them in the file.
        "Uncategorized" is double nested to maintain continuity with the rest of positional_dict.
    notes_categorized : IndexedDict
        A dictionary with keys of each positional name but values of IndexedDicts of note pairs from several categories.
        Think of it as curriculum Units and Chapters.
            All Units have Chapters, thus the Units will have all of the note pairs of the Chapters.
            In this case, Unit may have a prefix of, for example, "~", and Chapter "~~".
        For the notes to be nested, one inner one must start with the prefix of the outer one.
        Otherwise, notes will not be added to the outer positional key.

    Special Methods
    ---------------
        __str__()
            Prints all of the variables separated by new lines.
    """
    def __init__(self, file_name: str, comments: list, delimeter: str, skip_warnings=False,
                 *, generics: list=None, positionals: list=None, extensions: list=None,
                 ignore_generics: bool=False, filter_extensions: bool=True, remove_categories: bool=True):
        """
        Sets up all variables and creates notes.

        Parameters
        ----------
        file_name : str
            Name of the file to retrieve notes from.
        comments : list of str
            All prefixes to ignore while reading notes.
        delimeter : str
            Character that separates terms from definitions.
        skip_warnings : bool
            Whether to not print out the error message.
        generics : list of tuple(str, str)
            List of generics that are in the tuple (name, prefix)
        positionals : list of tuple(str, str)
            List of positionals that are in the tuple (name, prefix).
        extensions : list of tuple(str, str)
            List of extensions that are in the tuple (name, surround char) or (name, begin char, end char).
        ignore_generics : bool
            Whether to exclude generic terms from the positional and categorized notes.
        filter_extensions : bool
            Whether to remove extensions from the main definition.
        remove_categories : bool
            Whether to remove lines with the category prefix from the notes.
        """

        super().__init__(file_name, comments, delimeter, skip_warnings=True)
        self.error_message = ""

        self.positional_list = positionals
        self.generic_list = generics
        self.extension_list = extensions

        self.notes_extended = copy.deepcopy(self.notes_split)
        self.generic_dict = IndexedDict()
        self.extension_dict = IndexedDict()
        self.positional_dict = IndexedDict()
        self.notes_categorized = IndexedDict()

        if extensions is not None:
            self._add_extensions(filter_extensions)
            for nb in extensions:
                self.extension_dict[nb[0]] = IndexedDict()
            self._make_extension_dict(ignore_generics)

        if generics is not None:
            for name, prefix in generics:
                self.generic_dict[name] = IndexedDict()
            self._make_generic_dict()

        if positionals is not None:
            for name, prefix in positionals:
                self.positional_dict[name] = IndexedDict()
            self.positional_dict["Uncategorized"] = IndexedDict()
            self.positional_dict["Uncategorized"]["Uncategorized"] = IndexedDict()
            self._make_positional_dict(ignore_generics)
            self._make_notes_categorized(ignore_generics)

        self._clean_categories(remove_categories)
        self._make_notes_paired(notes_split=self.notes_extended)

        if not skip_warnings:
            print(self.error_message)

    def __str__(self):
        """
        Turns all variables into strings.

        Returns
        -------
        str
            All variables separated by new lines.
        """

        message = super().__str__() + "\n"
        message += "CategorizedNoteUtil: \n\n"
        message += "Positionals: " + str(self.positional_list) + "\n"
        message += "Generics: " + str(self.generic_list) + "\n"
        message += "Extensions: " + str(self.extension_list) + "\n"

        message += "Notes extended: " + str(self.notes_extended) + "\n"
        message += "Generic dict: " + str(self.generic_dict) + "\n"
        message += "Extension dict: " + str(self.extension_dict) + "\n"
        message += "Positional dict: " + str(self.positional_dict) + "\n"
        message += "Notes categorized: " + str(self.notes_categorized) + "\n"

        return message

    def _add_extensions(self, filter_extensions: bool=True):
        """
        Adds extensions (as provided with the extensions parameter in __init__, to each definition.

        The notes_extended list is what contains definitions with extensions, and is separate from notes_split.

        Parameters
        ----------
        filter_extensions : bool
            Whether to remove extensions from the main definition of the term.

        Returns
        -------
        None
        """

        if self.extension_list is not None:
            for i in range(len(self.notes_extended)):
                if len(self.notes_extended[i]) != 2:
                    continue

                orig_len = len(self.notes_extended[i][1])
                for nb in self.extension_list:
                    name, bound1, bound2 = None, None, None
                    if len(nb) == 2:
                        name, bound1 = nb
                        bound2 = bound1
                    elif len(nb) == 3:
                        name, bound1, bound2 = nb

                    while True:     # There could be multiple extensions of a single name.
                        try:
                            try:
                                b1 = self.notes_extended[i][1].index(bound1, 0, orig_len)
                            except ValueError:
                                # No extensions left for this term, move to next extension
                                break

                            try:
                                b2 = self.notes_extended[i][1].index(bound2, b1 + 1, orig_len)
                            except ValueError:
                                # Only one bound is an error
                                raise errors.MissingBoundError

                            self.notes_extended[i][1] += "\n" + name + self.delimeter + " " + \
                                                         self.notes_extended[i][1][b1 + len(bound1): b2]
                            if filter_extensions:
                                self.notes_extended[i][1] = self.notes_extended[i][1][:b1] + \
                                                            self.notes_extended[i][1][b2 + len(bound2):]
                                orig_len -= (b2 - b1 + len(bound1))
                            self.notes_extended[i][1] = self.notes_extended[i][1].strip()
                            if "\n" not in self.notes_extended[i][1]:
                                self.notes_extended[i][1] = "\n" + self.notes_extended[i][1]

                        except errors.MissingBoundError:
                            self.error_message += "WARNING: Missed bound at around line " + str(i+1) + ".\n"
                            self.error_message += "Pair: " + str(self.notes_extended[i])
                            break

    def _make_generic_dict(self):
        """
        Creates a dict of keys as the name of generics and values as all terms and definitions with that generic.

        Returns
        -------
        None
        """
        for i in range(len(self.notes_extended)):

            if len(self.notes_extended[i]) != 2:
                continue

            for n, p in self.generic_list:
                if self.notes_extended[i][0].startswith(p):
                    self.notes_extended[i][0] = self.notes_extended[i][0][len(p):].strip()
                    self.generic_dict[n][self.notes_extended[i][0]] = self.notes_extended[i][1]

    def _make_extension_dict(self, ignore_generics: bool=False):
        """
        Creates a dict of keys as the name of extensions and values as all terms and definitions with that extension.

        Parameters
        ----------
        ignore_generics : bool
            Whether to ignore generics while creating this dictionary.

        Returns
        -------
        None
        """

        for i in range(len(self.notes_extended)):
            if len(self.notes_extended[i]) != 2:
                continue

            if ignore_generics:
                is_generic = False
                for n, p in self.generic_list:
                    if self.notes_extended[i][0].startswith(p):
                        is_generic = True
                        break
                if is_generic:
                    continue

            split_extensions = self.notes_extended[i][1].split("\n")
            for ex in split_extensions:
                for nb in self.extension_list:
                    if ex.startswith(nb[0]):
                        self.extension_dict[nb[0]][self.notes_extended[i][0]] = self.notes_extended[i][1]

    def _make_positional_dict(self, ignore_generics: bool=False):
        """
        Makes a dict where each term and definition is under the correct category.

        Creates a dict of keys as names of positionals and values as another dict of keys as names of the notes
        positional with the value of an IndexedDict with terms and definitions in that positional.

        Parameters
        ----------
        ignore_generics : bool
            Whether to ignore generic terms while creating this dict.

        Returns
        -------
        None
        """

        name, prefix, curr = None, None, None
        for i in range(len(self.notes_extended)):

            if ignore_generics:
                is_generic = False
                for n, p in self.generic_list:
                    if self.notes_extended[i][0].startswith(p):
                        is_generic = True
                        break
                if is_generic:
                    continue

            for n, p in self.positional_list[::-1]:
                if self.notes_extended[i][0].startswith(p):
                    name, prefix, curr = n, p, self.notes_extended[i][0][len(p):].strip()
                    self.positional_dict[name][curr] = IndexedDict()
                    break
            else:
                if len(self.notes_extended[i]) != 2:
                    continue
                if name is None or prefix is None:
                    self.positional_dict["Uncategorized"]["Uncategorized"][
                        self.notes_extended[i][0]] = self.notes_extended[i][1]
                else:
                    self.positional_dict[name][curr][self.notes_extended[i][0]] = self.notes_extended[i][1]

    def _make_notes_categorized(self, ignore_generics: bool=False):
        """
        Creates a dict with keys as positional names and values as all terms and definitions "under" that category.

        Parameters
        ----------
        ignore_generics : bool
            Whether to ignore generic terms while creating this dict.

        Returns
        -------
        None
        """

        for name in self.positional_dict.keys():
            for category in self.positional_dict[name].keys():
                self.notes_categorized[category] = IndexedDict()

        self.notes_categorized["Uncategorized"] = self.positional_dict["Uncategorized"]["Uncategorized"]

        for name, prefix in self.positional_list:
            curr = None
            for i in range(len(self.notes_extended)):

                if ignore_generics:
                    is_generic = False
                    for n, p in self.generic_list:
                        if self.notes_extended[i][0].startswith(p):
                            is_generic = True
                            break
                    if is_generic:
                        continue

                if self.notes_extended[i][0].startswith(prefix):
                    for n, p in self.positional_list[::-1]:
                        if n == name:
                            curr = self.notes_extended[i][0][len(prefix):].strip()
                            break
                        elif self.notes_extended[i][0].startswith(p):
                            if p.startswith(prefix):
                                break
                    continue
                else:
                    for n, p in self.positional_list[::-1]:
                        if self.notes_extended[i][0].startswith(p):
                            if p != prefix and not p.startswith(prefix):
                                curr = None
                    if len(self.notes_extended[i]) != 2:
                        continue
                    elif curr is None:
                        continue
                    else:
                        self.notes_categorized[curr][self.notes_extended[i][0]] = self.notes_extended[i][1]

    def _clean_categories(self, remove_categories: bool=True):
        """
        Removes all prefixes from notes_extended and notes_split terms that start with a category prefix.

        Parameters
        ----------
        remove_categories : bool
            Whether to remove the whole line altogether.

        Returns
        -------
        None
        """

        for i in range(len(self.notes_extended) - 1, -1, -1):
            if self.positional_list is not None:
                for n, p in self.positional_list:
                    if self.notes_extended[i][0].startswith(p):
                        if remove_categories:
                            del self.notes_extended[i]
                        else:
                            self.notes_extended[i][0] = self.notes_extended[i][0][len(p):].strip()
            if self.generic_list is not None:
                for n, p in self.generic_list:
                    if self.notes_extended[i][0].startswith(p):
                        self.notes_extended[i][0] = self.notes_extended[i][0][len(p):].strip()

        for i in range(len(self.notes_split) - 1, -1, -1):
            if self.positional_list is not None:
                for n, p in self.positional_list:
                    if self.notes_split[i][0].startswith(p):
                        if remove_categories:
                            del self.notes_split[i]
                        else:
                            self.notes_split[i][0] = self.notes_split[i][0][len(p):].strip()
            if self.generic_list is not None:
                for n, p in self.generic_list:
                    if self.notes_split[i][0].startswith(p):
                        self.notes_split[i][0] = self.notes_split[i][0][len(p):].strip()

    def term(self, *, notes_dict: IndexedDict=None,
             index: int=None, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """Excludes extensions from definition while searching."""

        return super().term(notes_dict=notes_dict, index=index, term=term, definition=definition, func=func)

    def definition(self, *, notes_dict: IndexedDict=None,
                   index: int=None, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """Excludes extensions from definition while searching."""

        return super().definition(notes_dict=notes_dict, index=index, term=term, definition=definition, func=func)

    def pair_index(self, *, notes_dict: IndexedDict=None,
                   term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """Excludes extensions from definition while searching."""

        return super().pair_index(notes_dict=notes_dict, term=term, definition=definition, func=func)

    def terms(self, *, notes_dict: IndexedDict=None,
              indexes: int=None, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """Excludes extensions from definition while searching."""

        return super().terms(notes_dict=notes_dict, indexes=indexes, term=term, definition=definition, func=func)

    def definitions(self, *, notes_dict: IndexedDict = None,
                    indexes: int=None, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """Excludes extensions from definition while searching."""

        return super().definitions(notes_dict=notes_dict, indexes=indexes, term=term, definition=definition, func=func)

    def pair_indexes(self, *, notes_dict: IndexedDict=None,
                     term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """Excludes extensions from definition while searching."""

        return super().pair_indexes(notes_dict=notes_dict, term=term, definition=definition, func=func)

    def extension(self, name: str, *, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """
        Finds all values of the extension of a definition given the name of the extension.

        Parameters
        ----------
        name : str
            Name of the extension of the wanted value.
        term : str, optional if definition is provided.
            Name of the term to find.
        definition : str, optional if the term is provided.
            Name of the definition to find.
        func : function
            Removes the extensions from the definition if left blank.
            Otherwise applies this function to the term, definition, and key and value of the parameter and notes dict.

        Returns
        -------
        list of str
            All values of the wanted extension.

        Raises
        ------
        NoExtensionError
            If the term has no extension or the name of the extension given was incorrect.
        """

        all_values = []
        for ex in self.extension_dict.keys():
            if name.lower() == ex.lower():
                exact_definition = self.definition(notes_dict=self.extension_dict[ex],
                                                   term=term, definition=definition, func=func)
                extensions = exact_definition.split("\n")[1:]
                for ext in extensions:
                    if ext.startswith(ex):
                        all_values.append(ext[ext.index(self.delimeter) + len(self.delimeter) + 1:])
        if not all_values:
            raise errors.NoExtensionError
        return all_values

    def generic(self, *, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """
        Finds whether the term is part of a generic.

        Parameters
        ----------
        term : str, optional if definition is provided.
            Name of the term to find.
        definition : str, optional if the term is provided.
            Name of the definition to find.
        func : function
            Removes the extensions from the definition if left blank.
            Otherwise applies this function to the term, definition, and key and value of the parameter and notes dict.

        Returns
        -------
        str
            The name of the generic the term is a part of

        Raises
        ------
        NoCategoryError
            If no generic is found.
        """

        for g in self.generic_dict.keys():
            try:
                self.term(notes_dict=self.generic_dict[g], term=term, definition=definition,
                          func=func)
            except errors.NotesNotFoundError:
                pass
            else:
                return g
        raise errors.NoCategoryError

    def category(self, *, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """
        Finds whether the term is part of a positional category.

        Parameters
        ----------
        term : str, optional if definition is provided.
            Name of the term to find.
        definition : str, optional if the term is provided.
            Name of the definition to find.
        func : function
            Removes the extensions from the definition if left blank.
            Otherwise applies this function to the term, definition, and key and value of the parameter and notes dict.

        Returns
        -------
        str
            The name of the category the term is a part of

        Raises
        ------
        NoCategoryError
            If no category is found.
        """

        for n in self.positional_dict.keys():
            for c in self.positional_dict[n].keys():
                try:
                    self.term(notes_dict=self.positional_dict[n][c], term=term, definition=definition, func=func)
                except errors.NotesNotFoundError:
                    pass
                else:
                    return c
        raise errors.NoCategoryError

    def extensions(self, *, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """
        Returns all extensions that a term has.

        Parameters
        ----------
        term : str, optional if definition is provided.
            Name of the term to find.
        definition : str, optional if the term is provided.
            Name of the definition to find.
        func : function
            Removes the extensions from the definition if left blank.
            Otherwise applies this function to the term, definition, and key and value of the parameter and notes dict.

        Returns
        -------
        dict
            Keys of the name of the extension with the value as a list of all values of that extension.

        Raises
        ------
        NoExtensionError
            If no extensions are found.
        """

        all_extensions = {}
        for ex in self.extension_dict.keys():
            try:
                exact_definition = self.definition(notes_dict=self.extension_dict[ex],
                                                   term=term, definition=definition, func=func)
            except errors.NotesNotFoundError:
                continue

            extensions = exact_definition.split("\n")[1:]
            for ext in extensions:
                if ext.startswith(ex):
                    try:
                        all_extensions[ex].append(ext[ext.index(self.delimeter) + len(self.delimeter) + 1:])
                    except KeyError:
                        all_extensions[ex] = [ext[ext.index(self.delimeter) + len(self.delimeter) + 1:]]
        if not all_extensions:
            raise errors.NoExtensionError

        return all_extensions

    def categories(self, *, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
        """
        Returns all positional categories the term is a part of.

        Parameters
        ----------
        term : str, optional if definition is provided.
            Name of the term to find.
        definition : str, optional if the term is provided.
            Name of the definition to find.
        func : function
            Removes the extensions from the definition if left blank.
            Otherwise applies this function to the term, definition, and key and value of the parameter and notes dict.

        Returns
        -------
        list of str
            All names of the categories the term is a part of.

        Raises
        ------
        NoCategoryError
            If no categories are found.
        """

        all_categories = []
        for n in self.notes_categorized.keys():
            try:
                self.term(notes_dict=self.notes_categorized[n], term=term, definition=definition, func=func)
            except errors.NotesNotFoundError:
                pass
            else:
                all_categories.append(n)
        if not all_categories:
            raise errors.NoCategoryError

        return all_categories


# noteutil = CategorizedNoteUtil("test_notes.txt", ["#"], ":",
#                                generics=[("Important", "!")],
#                                positionals=[("Category 1", "~"), ("Category 2", "~~")],
#                                extensions=[("Decimal", "%")],
#                                ignore_generics=True)

# noteutil = CategorizedNoteUtil("test_notes2.txt", ["#"], ":")

# noteutil = CategorizedNoteUtil("test_notes3.txt", ["#"], ":",
#                                generics=[("Important", "!")],
#                                positionals=[("Chapters", "~~")],
#                                extensions=[("Latex", "$$"), ("Abbreviation", "(", ")"),
#                                            ("Example", "{", "}")], )

# print(noteutil)
# try:
#     print(noteutil.category(term="beatniks (1950)"))
# except errors.NotesNotFoundError as e:
#     print("error")
#     print(e)
