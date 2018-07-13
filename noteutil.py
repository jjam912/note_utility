"""
This module contains classes that are used to store data from a file and turn them into usable notes.
"""
import note_utility.errors as errors


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
        self.read_file(file_name, comments)

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

    def read_file(self, file_name: str, comments: list):
        """
        Converts all the data from the file into a list of notes.

        If a line contains nothing (possibly after strip), the line will be ignored.
        Even though this method is used in __init__(), this also a setter method.

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

    def lines(self, *, indexes: list=None, name: str=None, case_sensitive: bool=False):
        """
        Returns all lines that have the provided name "in" it.

        Uses the "in" operator to compare lines.

        Parameters
        ----------
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
        ValueError
            If no lines had the provided name in it.
        """

        lines = []
        for i, line in enumerate(self.notes_list):
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
            raise ValueError("No line had the name in it.")
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
            If index >= len(self.items) or index < 0.
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

    def key_with(self, *, index=None, val=None, func=None):
        """
        Returns the key of a given value if that key's value matches exactly with a key in the dictionary.

        Parameters
        ----------
        index : int, optional if val is provided.
            The index of the key
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
                if val == func(v):
                    return k
            elif val == v:
                return k
            if index == i:
                return k
            i += 1
        return KeyError("No key was found to have the name or associated value.")

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
                found_index = False
                for index in indexes:
                    if index == i:
                        keys.append(k)
                        found_index = True
                        break
                if found_index:
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

    def val_with(self, *, index=None, key=None, func=None):
        """
        Returns the value of a given key if that value's key matches exactly with the dictionary's key.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        index : int, optional if key is provided.
            Index of a key.
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

        i = 0
        for k, v in self.items():
            if func is not None:
                if key == func(k):
                    return v
            elif key == k:
                return v
            if index == i:
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
                found_index = False
                for index in indexes:
                    if index == i:
                        vals.append(v)
                        found_index = True
                        break
                if found_index:
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

    Keys are used for to_dict().
    Keys that are used for converting to a dictionary.
        KEY_DICT_INDEX : str
        KEY_DICT_INDEXES : str

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
        self.notes_paired = IndexedDict()
        self.split_terms()
        self.make_notes_paired()

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

        message += "Notes paired: " + str(self.notes_paired) + "\n"
        return message

    def split_terms(self):
        """
        Separates all terms in notes_list by splitting using the delimeter.

        This makes notes_list into a List[List[str]]

        Returns
        -------
        None
        """

        for i in range(len(self.notes_list)):
            try:
                self.notes_list[i] = self.notes_list[i].split(self.delimeter)
            except AttributeError:
                # List has already been split
                pass

            self.notes_list[i][0] = self.notes_list[i][0].strip()
            if len(self.notes_list[i]) == 2:
                self.notes_list[i][1] = self.notes_list[i][1].strip()

    def make_notes_paired(self):
        """
        Creates a IndexedDict based off the notes_list created in NoteUtil.

        If we want to create a new dictionary from a new file, we must first read_file()
            before calling this or recreate a PairedNoteUtil.

        Returns
        -------
        None

        """

        self.notes_paired = IndexedDict()

        for i in range(len(self.notes_list)):
            try:
                if len(self.notes_list[i]) > 2:
                    raise errors.ExtraDelimeterError
                elif len(self.notes_list[i]) == 1:
                    raise errors.MissingDelimeterError

                term, definition = self.notes_list[i]

                if definition == "":
                    raise errors.NoDefinitionError

                self.notes_paired[term] = definition

            except errors.ExtraDelimeterError:
                self.error_message += "WARNING: Extra delimeter at around line " + str(i+1) + ". "
                self.error_message += "Pair: " + str(self.notes_list[i]) + "\n"
            except errors.MissingDelimeterError:
                self.error_message += "WARNING: Missing delimeter at around line " + str(i+1) + ". "
                self.error_message += "Pair: " + str(self.notes_list[i]) + "\n"
            except errors.NoDefinitionError:
                self.error_message += "WARNING: Missed pairing at around line " + str(i+1) + ". "
                self.error_message += "Pair: " + str(self.notes_list[i]) + "\n"

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
        KeyError
            If the provided term or definition is not found within the notes_dict's keys.
        """

        if index is not None:
            return self.notes_paired.key_with(index=index)
        if not case_sensitive:
            return self.notes_paired.key_with(val=definition.lower() if definition is not None else definition,
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
            return self.notes_paired.val_with(index=index)
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
        IndexError
            If the term or definition is not found within the notes_dict's items.
        """

        if not case_sensitive:
            return self.notes_paired.index_with(key=term.lower() if term is not None else term,
                                                val=definition.lower() if definition is not None else definition,
                                                func=str.lower)
        return self.notes_paired.index_with(key=term, val=definition)

    def terms(self, *, indexes: list=None, term: str=None, definition: str=None, case_sensitive: bool=False):
        """
        Returns a list of terms that have part of the term name in it or part of the definition in its own definition.

        "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.

        Parameters
        ----------
        indexes : list of int, optional if term or definition is provided.
            Indexes of terms to be added.
        term : str, optional if indexes or definition is provided.
            Name that may appear in multiple other terms' names.
        definition : str, optional if indexes or term is provided.
            Name that may appear in multiple other definitions.
        case_sensitive : bool
            Whether case matters.

        Returns
        -------
        list of term
            All of the terms that corresponded with the term name or definition name.

        Raises
        ------
        KeyError
            If no term had the name in its name or had the definition in its value.
        """

        if not case_sensitive:
            return self.notes_paired.keys_with(indexes=indexes,
                                               name=term.lower() if term is not None else term,
                                               val=definition.lower() if definition is not None else definition,
                                               func=str.lower)
        return self.notes_paired.keys_with(name=term, val=definition)

    def definitions(self, *, indexes: list=None, term: str=None, definition: str=None, case_sensitive: bool=False):
        """
        Returns a list of definitions that have part of the term name as its key or part of the definition name in it.

        "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.

        Parameters
        ----------
        indexes : list of int
            Indexes of terms to be added.
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
            return self.notes_paired.vals_with(indexes=indexes,
                                               key=term.lower() if term is not None else term,
                                               name=definition.lower() if definition is not None else definition,
                                               func=str.lower)
        return self.notes_paired.vals_with(key=term, name=definition)

    def indexes(self, *, term: str=None, definition: str=None, case_sensitive: bool=False):
        """
        Returns the index of a term or definition if it is part of a key or definition in the paired notes.

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
        IndexError
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

    def pairs(self, indexes: list):
        """
        Returns a list of (key, value) tuples that represent term and definition pairs.

        Parameters
        ----------
        indexes : list of int
            Indexes of the pairs.

        Returns
        -------
        list of tuple(str, str)
            The list of term and definition pairs.
        """

        return self.notes_paired.items_at(indexes)


class CategorizedNoteUtil(PairedNoteUtil):
    """
    Uses prefixes to separate notes into categories, of which are either positional or generic.

    Definitions may contain additional information, known as extensions, which are separated by new lines.
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
    positional_dict : IndexedDict
        A dictionary with keys of each positional name and values of IndexedDicts.
        The positional dict ignores any nesting of prefixes.
        The note pairs in positional dict are pairs that are exclusive only to that name and prefix.
        An "Uncategorized" category contains all note pairs that do not have a category above them in the file.
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

        Parameters
        ----------
        file_name : str
            Name of the file
        comments
        delimeter
        skip_warnings
        generics
        positionals
        extensions
        ignore_generics
        filter_extensions
        remove_categories
        """
        super().__init__(file_name, comments, delimeter, skip_warnings=True)
        self.error_message = ""

        self.positionals = positionals
        self.generics = generics
        self.extensions = extensions

        self.notes_categorized = IndexedDict()
        self.positional_dict = IndexedDict()
        self.generic_dict = IndexedDict()

        if extensions is not None:
            self.add_extensions(filter_extensions)

        if generics is not None:
            for name, prefix in generics:
                self.generic_dict[name] = IndexedDict()
            self.make_generic_dict()

        if positionals is not None:
            for name, prefix in positionals:
                self.positional_dict[name] = IndexedDict()
                self.positional_dict["Uncategorized"] = IndexedDict()
            self.make_positional_dict(ignore_generics)

        self.make_notes_categorized(ignore_generics)
        self.clean_categories(remove_categories)
        self.make_notes_paired()

        if not skip_warnings:
            print(self.error_message)

    def __str__(self):
        message = super().__str__() + "\n"
        message += "CategorizedNoteUtil: \n"
        message += "Positionals: " + str(self.positionals) + "\n"
        message += "Generics: " + str(self.generics) + "\n"
        message += "Extensions: " + str(self.extensions) + "\n"

        message += "Generic dict: " + str(self.generic_dict) + "\n"
        message += "Positional dict: " + str(self.positional_dict) + "\n"
        message += "Notes categorized: " + str(self.notes_categorized) + "\n"

        return message

    def add_extensions(self, filter_extensions: bool=True):
        if self.extensions is not None:
            for i in range(len(self.notes_list)):
                if len(self.notes_list[i]) != 2:
                    continue

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
                                # No extensions left for this term, just pass
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
                            self.error_message += "WARNING: Missed bound at around line " + str(i+1) + ".\n"
                            self.error_message += "Pair: " + str(self.notes_list[i])
                            break

    def make_generic_dict(self):
        if self.generics is not None:
            for i in range(len(self.notes_list) - 1, -1, -1):

                if len(self.notes_list[i]) != 2:
                    continue

                for n, p in self.generics:
                    if self.notes_list[i][0].startswith(p):
                        self.notes_list[i][0] = self.notes_list[i][0][len(p):].strip()
                        self.generic_dict[n][self.notes_list[i][0]] = self.notes_list[i][1]

    def make_positional_dict(self, ignore_generics: bool=False):
        if self.positionals is not None:
            name, prefix, curr = None, None, None
            for i in range(len(self.notes_list)):

                if ignore_generics:
                    is_generic = False
                    for n, p in self.generics:
                        if self.notes_list[i][0].startswith(p):
                            is_generic = True
                            break
                    if is_generic:
                        continue

                for n, p in self.positionals[::-1]:
                    if self.notes_list[i][0].startswith(p):
                        name, prefix, curr = n, p, self.notes_list[i][0][len(p):].strip()
                        self.positional_dict[name][curr] = IndexedDict()
                        break
                else:
                    if len(self.notes_list[i]) != 2:
                        continue
                    if name is None or prefix is None:
                        self.positional_dict["Uncategorized"][self.notes_list[i][0]] = self.notes_list[i][1]
                    else:
                        self.positional_dict[name][curr][self.notes_list[i][0]] = self.notes_list[i][1]

    def make_notes_categorized(self, ignore_generics: bool=False):
            for name in self.positional_dict.keys():
                if name == "Uncategorized":
                    continue
                for category in self.positional_dict[name].keys():
                    self.notes_categorized[category] = IndexedDict()

            self.notes_categorized["Uncategorized"] = self.positional_dict["Uncategorized"]

            for name, prefix in self.positionals:
                curr = None
                for i in range(len(self.notes_list)):

                    if ignore_generics:
                        is_generic = False
                        for n, p in self.generics:
                            if self.notes_list[i][0].startswith(p):
                                is_generic = True
                                break
                        if is_generic:
                            continue

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

    def clean_categories(self, remove_categories: bool=True):
        for i in range(len(self.notes_list) - 1, -1, -1):
            for n, p in self.positionals:
                if self.notes_list[i][0].startswith(p):
                    if remove_categories:
                        del self.notes_list[i]
                    else:
                        self.notes_list[i][0] = self.notes_list[i][0][len(p):].strip()
            for n, p in self.generics:
                if self.notes_list[i][0].startswith(p):
                    self.notes_list[i][0] = self.notes_list[i][0][len(p):].strip()

    def generic(self, name: str, case_sensitive: bool=False):
        for c, d in self.generic_dict.items():
            if not case_sensitive:
                if name.lower() == c.lower():
                    return d
            else:
                if name == c:
                    return d

    def category(self, name: str, case_sensitive: bool=False):
        for c, d in self.notes_categorized.items():
            if not case_sensitive:
                if name.lower() == c.lower():
                    return d
            else:
                if name == c:
                    return d

    def excategory(self, name: str, case_sensitive: bool=False):
        for n in self.positional_dict.keys():

            if not case_sensitive:
                if name.lower() == n.lower():
                    return self.positional_dict[n]
            else:
                if name == n:
                    return self.positional_dict[n]

            for c, d in self.positional_dict[n]:
                if not case_sensitive:
                    if name.lower() == c.lower():
                        return d
                else:
                    if name == c:
                        return d


noteutil = CategorizedNoteUtil("test_notes.txt", ["#"], ":",
                               generics=[("Important", "!")],
                               positionals=[("Category 1", "~"), ("Category 2", "~~")],
                               extensions=[("Decimal", "%")],
                               ignore_generics=True)

print(noteutil)

