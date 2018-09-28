import errors
import copy
import textwrap
import inspect


class Note:
    def __init__(self, content, nindex):
        self.content = content
        self.nindex = nindex

    def __eq__(self, other):
        return self.content == other.content

    def __ne__(self, other):
        return self.content != other.content

    def __str__(self):
        return self.content

    def __repr__(self):
        return "Note(\"{0}\"}, {1})".format(self.content, self.nindex)


def one(func):
    def wrapper():
        sign = inspect.signature(func)
        params = sign.parameters
        for val in params.values():
            if val is not None:
                break
        else:
            raise errors.NoArgsPassed
    return wrapper


class NoteUtil:

    def __init__(self, file_name: str, *, separator: str="\n", comment: str=None):
        self.notes = []
        self.file_name = file_name
        self.separator = separator
        self.comment = comment
        if self.file_name.endswith(".nu"):
            self._read_file()
        else:
            self._compile_file()
            self._read_file()

    def __str__(self):

        message = ("NoteUtil:\n"
                   "---------\n")

        message += "File name: " + repr(self.file_name) + "\n"
        message += "Notes: " + repr(self.notes) + "\n"
        message += "Separator: " + repr(self.separator) + "\n"
        message += "Comment prefix: " + repr(self.comment) + "\n"
        return message

    def _compile_file(self):

        with open(self.file_name, mode="r", encoding="UTF-8") as f:
            for line in f.read().split(self.separator):
                if self.comment is not None:
                    if line.startswith(self.comment):
                        continue

                line = line.strip()

                if self.comment is not None:
                    if line.startswith(self.comment):
                        continue

                if line == "":
                    continue

                self.notes.append(line)

        self.file_name = self.file_name.split(".")[0] + ".nu"
        with open(self.file_name, mode="w", encoding="UTF-8") as f:
            f.write(self.separator.join(self.notes))

    def _read_file(self):

        len_notes = len(self.notes)
        with open(self.file_name, mode="r", encoding="UTF-8") as f:
            for i, line in enumerate(f.read().split(self.separator)):
                self.notes.append(Note(line, len_notes + i,))

    def format(self):

        return self.separator.join(self.notes)

    def nindex(self, *, content: str=None):
        if content is not None:
            for note in self.notes:
                if note.content.lower() == content.lower():
                    return note.nindex
            raise errors.NotesNotFoundError("No note was found to equal the content: {0}".format(content))
        raise errors.NoArgsPassed

    def nindexes(self, *, content: str=None):
        nindexes = []
        if content is not None:
            for note in self.notes:
                if note.content.lower() in content.lower():
                    nindexes.append(note.nindex)
            if not nindexes:
                raise errors.NotesNotFoundError("No note was found containing the content: {0}.".format(content))
            return nindexes
        raise errors.NoArgsPassed

    def note(self, *, content: str=None, nindex: int=None):
        if nindex is not None:
            try:
                return self.notes[nindex]
            except IndexError:
                raise errors.NotesIndexError("The note index: {0} was out of bounds of the notes.".format(nindex))
        if content is not None:
            for note in self.notes:
                if note.content.lower() == content.lower():
                    return note
            raise errors.NotesNotFoundError("No note was found to equal content: {0}".format(content))
        raise errors.NoArgsPassed

    def notes(self, *, content: str=None, nindexes: list=None):
        notes = []
        if content is not None or nindexes is not None:
            for note in self.notes:
                if content is not None:
                    if note.content.lower() == content.lower():
                        notes.append(note)
                        continue
                if nindexes is not None:
                    if note.nindex in set(nindexes):
                        notes.append(note)
                        continue
            if not notes:
                raise errors.NotesNotFoundError(
                    "No note was found to contain content: {0} or have any indexes in: {1}".format(content, nindexes))
            return notes
        raise errors.NoArgsPassed


class Line(Note):
    def __init__(self, content, nindex, lindex):
        super().__init__(content, nindex)
        self.lindex = lindex

    def __repr__(self):
        return "Line(\"{0}\", {1}, {2})".format(self.content, self.nindex, self.lindex)


class LineNoteUtil(NoteUtil):

    def __init__(self, file_name: str, *, separator: str="\n", comment: str=None):

        self.lines = []
        super().__init__(file_name, separator=separator, comment=comment)

    def __str__(self):
        message = super().__str__() + "\n"
        message += ("LineNoteUtil:\n"
                    "-------------\n")
        message += "Lines: " + repr(self.lines) + "\n"
        return message

    def _read_file(self):

        for i in range(len(self.notes)):
            self.notes[i] = Line(self.notes[i], i, i)
            self.lines.append(Line(self.notes[i], i, i))

    def nindex(self, *, content: str=None, lindex: int=None):
        if content is not None or lindex is not None:
            for note in self.notes:
                if content is not None:
                    if note.content.lower() == content.lower():
                        return note.nindex
                if lindex is not None:
                    if isinstance(note, Line):
                        if note.lindex == lindex:
                            return note.nindex
            raise errors.NotesNotFoundError(
                "No note was found to equal the content: {0} or have the lindex: {1}".format(content, lindex))
        raise errors.NoArgsPassed

    def nindexes(self, *, content: str=None, lindexes: list=None):
        nindexes = []
        if content is not None or lindexes is not None:
            for note in self.notes:
                if content is not None:
                    if note.content.lower() in content.lower():
                        nindexes.append(note.nindex)
                        continue
                if lindexes is not None:
                    if isinstance(note, Line):
                        if note.lindex in set(lindexes):
                            nindexes.append(note.nindex)
                            continue
            if not nindexes:
                raise errors.NotesNotFoundError("No note was found containing the content: {0} or "
                                                "have any indexes in: {1}.".format(content, lindexes))
            return nindexes
        raise errors.NoArgsPassed

    def lindex(self, *, content: str=None, nindex: int=None):
        if content is not None or nindex is not None:
            for line in self.lines:
                if content is not None:
                    if content.lower() == line.content.lower():
                        return line.lindex
                if nindex is not None:
                    if line.nindex == nindex:
                        return line.lindex
            raise errors.NotesNotFoundError("No line was found to equal the content: {0} or "
                                            "have the nindex: {1}".format(content, nindex))
        raise errors.NoArgsPassed

    def lindexes(self, *, content: str=None, nindex: int=None):

        lindexes = []
        if content is not None or nindex is not None:
            for line in self.lines:
                if content is not None:
                    if content.lower() in line.content.lower():
                        lindexes.append(line.lindex)
                        continue
                if nindex is not None:
                    if line.nindex == nindex:
                        lindexes.append(line.lindex)
                        continue
            if not lindexes:
                raise errors.NotesNotFoundError("No line was found with the content: {0} or "
                                                "have the nindex: [1}".format(content, nindex))
            return lindexes
        raise errors.NoArgsPassed

    def line(self, *, content: str=None, nindex: int=None, lindex: int=None):
        if nindex is not None:
            try:
                if isinstance(self.notes[nindex], Line):
                    return self.notes[nindex]
                else:
                    raise errors.NotALine
            except IndexError:
                raise errors.NotesIndexError("The note index: {0} was out of bounds of the notes.".format(nindex))
        if lindex is not None:
            try:
                return self.lines[lindex]
            except IndexError:
                raise errors.NotesIndexError("The line index: {0} was out of bounds of the lines.".format(lindex))
        if content is not None:
            for line in self.lines:
                if line.content.lower() == content.lower():
                    return line
            raise errors.NotesNotFoundError("No line was found to equal content: {0}".format(content))
        raise errors.NoArgsPassed

    def lines(self, *, content: str=None, nindexes: list=None, lindexes: list=None):
        lines = []
        if content is not None or nindexes is not None or lindexes is not None:
            for line in self.lines:
                if content is not None:
                    if line.content.lower() == content.lower():
                        lines.append(line)
                        continue
                if nindexes is not None:
                    if line.nindex in set(nindexes):
                        lines.append(line)
                        continue
                if lindexes is not None:
                    if line.lindex in set(lindexes):
                        lines.append(line)
                        continue
            if not lines:
                raise errors.NotesNotFoundError(
                    "No line was found to contain content: {0} or have any indexes in: {1}".format(content, nindexes))
            return lines
        raise errors.NoArgsPassed


import os
os.chdir(os.getcwd() + "\\testing_notes")

noteutil = LineNoteUtil("test1.txt", comment="#")
print(noteutil)

# class Pair(Line):
#     def __init__(self, content, nindex, lindex, pindex, term, definition):
#         super().__init__(content, nindex, lindex)
#         self.pindex = pindex
#         self.term = term
#         self.definition = definition
#
#
# class PairedNoteUtil(LineNoteUtil):
#     """
#     Splits all lines in notes_list into key, value pairs known as terms and definitions.
#
#     Terms and definitions are separated by delimeters, which occur only once in each line but can be any character.
#     Creates a dictionary out of all of the terms and definitions by splitting by the delimeter.
#
#     Attributes
#     ----------
#         delimeter : str
#             The character that separates terms from definitions.
#         notes_paired : IndexedDict of {str: str}
#             IndexedDict created from splitting each element in notes_list with the delimeter.
#         error_message : str
#             Any errors that occurred while creating the paired notes.
#     Special Methods
#     ---------------
#         __str__()
#             Prints all variables separated by new lines.
#     """
#
#     def __init__(self, file_name: str, comments: list, delimeter: str, skip_warnings=False):
#         """
#         Initialize all variables with the file given.
#
#         Parameters
#         ----------
#         file_name : str
#             Name of the file to be converted into PairedNoteUtil.
#         comments : list of str
#             The prefixes of lines that will be ignored, checked both before and after strip.
#         delimeter : str
#             The character that separates the key from the value, or the term from the definition.
#         """
#
#         super().__init__(file_name, comments)
#         self.error_message = ""
#         self.delimeter = delimeter
#
#         self.notes_split = self.notes_list.copy()
#         self.notes_paired = IndexedDict()
#         self._split_terms()
#         self._make_notes_paired()
#
#         if not skip_warnings:
#             print(self.error_message)
#
#     def __str__(self):
#         """
#         Converts all variables into strings.
#
#         Returns
#         -------
#         str
#             All variables with labels separated by new lines.
#         """
#
#         message = super().__str__() + "\n"
#         message += "PairedNoteUtil:\n"
#         message += "Delimeter: " + self.delimeter + "\n"
#
#         message += "Notes split: " + str(self.notes_split) + "\n"
#         message += "Notes paired: " + str(self.notes_paired) + "\n"
#         return message
#
#     def _split_terms(self):
#         """
#         Separates all terms in notes_list by splitting using the delimeter.
#
#         This makes notes_list into a List[List[str]]
#
#         Returns
#         -------
#         None
#         """
#
#         self.notes_split = self.notes_list.copy()
#         for i in range(len(self.notes_split)):
#             try:
#                 self.notes_split[i] = self.notes_split[i].split(self.delimeter)
#             except AttributeError:  # List has already been split
#                 pass
#
#             self.notes_split[i][0] = self.notes_split[i][0].strip()
#             if len(self.notes_split[i]) == 2:
#                 self.notes_split[i][1] = self.notes_split[i][1].strip()
#
#     def _make_notes_paired(self, notes_split: list=None):
#         """
#         Creates a IndexedDict based off the notes_list created in NoteUtil.
#
#         If we want to create a new dictionary from a new file, we must first read_file()
#             before calling this or recreate a PairedNoteUtil.
#
#         Parameters
#         ----------
#         notes_split : list of list [str, str]
#             A list of terms and definitions - (as a list).
#
#         Returns
#         -------
#         None
#         """
#
#         self.notes_paired = IndexedDict()
#
#         if notes_split is None:
#             notes_split = self.notes_split
#         for i in range(len(notes_split)):
#             try:
#                 if len(notes_split[i]) > 2:
#                     raise errors.ExtraDelimeterError
#                 elif len(notes_split[i]) == 1:
#                     raise errors.MissingDelimeterError
#
#                 term, definition = notes_split[i]
#
#                 if definition == "":
#                     raise errors.NoDefinitionError
#
#                 if term in self.notes_paired:
#                     raise errors.DuplicateTermError
#
#                 self.notes_paired[term] = definition
#
#             except errors.ExtraDelimeterError:
#                 self.error_message += "WARNING: Extra delimeter at around index " + str(i+1) + ". "
#                 self.error_message += "Pair was skipped: " + str(notes_split[i]) + "\n"
#             except errors.MissingDelimeterError:
#                 self.error_message += "WARNING: Missing delimeter at around index " + str(i+1) + ". "
#                 self.error_message += "Pair was skipped: " + str(notes_split[i]) + "\n"
#             except errors.NoDefinitionError:
#                 self.error_message += "WARNING: Missed pairing at around index " + str(i+1) + ". "
#                 self.error_message += "Pair was skipped: " + str(notes_split[i]) + "\n"
#             except errors.DuplicateTermError:
#                 self.error_message += "WARNING: Duplicate term at around index " + str(i+1) + ". "
#                 self.error_message += "Pair was skipped: " + str(notes_split[i]) + "\n"
#
#     def format(self):
#         """
#         Formats the notes in the way the noteutil read it.
#
#         It prints each term separated by a delimeter, then a space, and then the definition.
#
#         Returns
#         -------
#         str
#             What was read from the note file.
#         """
#
#         formatted = ""
#         for term, definition in self.notes_paired.items():
#             formatted += "{0}{1} {2}\n".format(term, self.delimeter, definition)
#         return formatted
#
#     def term(self, *, notes_dict: IndexedDict=None,
#              index: int=None, term: str=None, definition: str=None, func=str.lower):
#         """
#         Returns a list of terms that matches exactly with the given definition.
#
#         Parameters
#         ----------
#         notes_dict : IndexedDict
#             Any IndexedDict that contains terms and definitions.
#         index : int, optional if definition is provided.
#             Index of the term.
#         term : str
#             A name of the term that may not match exactly (cases).
#         definition : str, optional if index is provided.
#             Name that matches a definition in notes_dict.
#         func : function
#             Function to apply to the notes_dict term and definition. Default is lower case.
#             Will also apply to term and definition if they are not None.
#
#         Returns
#         -------
#         str
#             First term that corresponded with the term name or definition name.
#
#         Raises
#         ------
#         NotesNotFoundError
#             If the provided term or definition is not found within the notes_dict's keys and values.
#         """
#
#         if notes_dict is None:
#             notes_dict = self.notes_paired
#         try:
#             if index is not None:
#                 return notes_dict.key_with(index=index)
#             if func:
#                 return notes_dict.key_with(name=func(term) if term is not None else term,
#                                            val=func(definition) if definition is not None else definition,
#                                            func=func)
#             return notes_dict.key_with(name=term, val=definition)
#         except KeyError:
#             raise errors.NotesNotFoundError("No term was found with the provided term or definition.")
#
#     def definition(self, *, notes_dict: IndexedDict=None,
#                    index: int=None, term: str=None, definition: str=None, func=str.lower):
#         """
#         Returns a list of definitions that have part of the term name as its key or part of the definition name in it.
#
#         Parameters
#         ----------
#         notes_dict : IndexedDict
#             Any IndexedDict that contains terms and definitions.
#         index : int, optional if term is provided.
#             Index of the definition.
#         term : str, optional if index is provided.
#             Name of the term that may be in a definition's key.
#         definition : str
#             The name of the definition that may not match exactly (cases).
#         func : function
#             Function to apply to the notes_dict term and definition. Default is lower case.
#             Will also apply to term and definition if they are not None.
#
#         Returns
#         -------
#         str
#             A definition that had a key that corresponded with term or the definition. See IndexedDict.
#
#         Raises
#         ------
#         NotesNotFoundError
#             If the provided term or definition is not found within the notes_dict's keys or values.
#         """
#
#         if notes_dict is None:
#             notes_dict = self.notes_paired
#         try:
#             if index is not None:
#                 return notes_dict.val_with(index=index)
#             if func:
#                 return notes_dict.val_with(key=func(term) if term is not None else term,
#                                            name=func(term) if definition is not None else definition,
#                                            func=func)
#             return notes_dict.val_with(key=term)
#         except ValueError:
#             raise errors.NotesNotFoundError("No definition was found with the provided term or definition.")
#
#     def pair_index(self, *, notes_dict: IndexedDict=None,
#                    term: str=None, definition: str=None, func=str.lower):
#         """
#         Returns the index of a term or definition if it matches exactly.
#
#         Parameters
#         ----------
#         notes_dict : IndexedDict
#             Any IndexedDict that contains terms and definitions.
#         term : str, optional if definition is provided.
#             Key of the element that is being searched for.
#         definition : str, optional if term is provided.
#             Value of the element that is being searched for.
#         func : function
#             Function to apply to the notes_dict term and definition. Default is lower case.
#             Will also apply to term and definition if they are not None.
#
#         Returns
#         -------
#         int
#             Index of the term or definition in the notes_dict.
#
#         Raises
#         ------
#         NotesIndexError
#             If the index is out of range (and thus no terms or definitions are found).
#         """
#
#         if notes_dict is None:
#             notes_dict = self.notes_paired
#         try:
#             if func:
#                 return notes_dict.index_with(key=func(term) if term is not None else term,
#                                              val=func(definition) if definition is not None else definition,
#                                              func=func)
#             return notes_dict.index_with(key=term, val=definition)
#         except IndexError:
#             raise errors.NotesIndexError("No index was found for the provided term or definition.")
#
#     def terms(self, *, notes_dict: IndexedDict=None,
#               indexes: list=None, term: str=None, definition: str=None, func=str.lower):
#         """
#         Returns a list of terms that have part of the term name in it or part of the definition in its own definition.
#
#         "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.
#
#         Parameters
#         ----------
#         notes_dict : IndexedDict
#             Any IndexedDict that contains terms and definitions.
#         indexes : list of int, optional if term or definition is provided.
#             Indexes of terms to be added.
#         term : str, optional if indexes or definition is provided.
#             Name that may appear in multiple other terms' names.
#         definition : str, optional if indexes or term is provided.
#             Name that may appear in multiple other definitions.
#         func : function
#             Function to apply to the notes_dict term and definition. Default is lower case.
#             Will also apply to term and definition if they are not None.
#
#         Returns
#         -------
#         list of str
#             All of the terms that corresponded with the term name or definition name.
#
#         Raises
#         ------
#         NotesNotFoundError
#             If no term had the name in its name or had the definition in its value.
#         """
#
#         if notes_dict is None:
#             notes_dict = self.notes_paired
#         try:
#             if func:
#                 return notes_dict.keys_with(indexes=indexes,
#                                             name=func(term) if term is not None else term,
#                                             val=func(definition) if definition is not None else definition,
#                                             func=func)
#             return notes_dict.keys_with(indexes=indexes, name=term, val=definition)
#         except KeyError:
#             raise errors.NotesNotFoundError("No terms has the provided term or definition in them.")
#
#     def definitions(self, *, notes_dict: IndexedDict=None,
#                     indexes: list=None, term: str=None, definition: str=None, func=str.lower):
#         """
#         Returns a list of definitions that have part of the term name as its key or part of the definition name in it.
#
#         "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.
#
#         Parameters
#         ----------
#         notes_dict : IndexedDict
#             Any IndexedDict that contains terms and definitions.
#         indexes : list of int
#             Indexes of terms to be added.
#         term : str, optional if definition is provided.
#             Name of the term that may be in a definition's key.
#         definition : str, optional if term is provided.
#             Part of a definition that appears in the desired definition.
#         func : function
#             Function to apply to the notes_dict term and definition. Default is lower case.
#             Will also apply to term and definition if they are not None.
#
#         Returns
#         -------
#         list of str
#             All definitions that had a key that corresponded with term or part of the definition. See IndexedDict.
#
#         Raises
#         ------
#         NotesNotFoundError
#             If no definition had the definition in its name or had the term in its key.
#         """
#
#         if notes_dict is None:
#             notes_dict = self.notes_paired
#         try:
#             if func:
#                 return notes_dict.vals_with(indexes=indexes,
#                                             key=func(term) if term is not None else term,
#                                             name=func(term) if definition is not None else definition,
#                                             func=func)
#             return notes_dict.vals_with(indexes=indexes, key=term, name=definition)
#         except ValueError:
#             raise errors.NotesNotFoundError("No definitions had the provided term or definition in them.")
#
#     def pair_indexes(self, *, notes_dict: IndexedDict=None,
#                      term: str=None, definition: str=None, func=str.lower):
#         """
#         Returns the index of a term or definition if it is part of a key or definition in the paired notes.
#
#         "in" operator is used to determine if the term name is in another term. If "in" doesn't work, use ==.
#
#         Parameters
#         ----------
#         notes_dict : IndexedDict
#             Any IndexedDict that contains terms and definitions.
#         term : str, optional if definition is provided.
#             Key of the element that is being searched for.
#         definition : str, optional if term is provided.
#             Value of the element that is being searched for.
#         func : function
#             Function to apply to the notes_dict term and definition. Default is lower case.
#             Will also apply to term and definition if they are not None.
#
#         Returns
#         -------
#         int
#             Index of the term or definition in the notes_dict.
#
#         Raises
#         ------
#         NotesIndexError
#             If all indexes were out of range of the IndexedDict and no items were found.
#         """
#
#         if notes_dict is None:
#             notes_dict = self.notes_paired
#         try:
#             if func:
#                 return notes_dict.indexes_with(key=func(term) if term is not None else term,
#                                                val=func(definition) if definition is not None else definition,
#                                                func=func)
#             return notes_dict.indexes_with(key=term, val=definition)
#         except IndexError:
#             raise errors.NotesIndexError("No indexes were found for the provided terms or definitions.")
#
#     def pair(self, index: int, *, notes_dict: IndexedDict=None):
#         """
#         Returns the term and definition of the notes_dict at the provided index.
#
#         Parameters
#         ----------
#         index : int
#             Index of the term and definition in the dictionary.
#         notes_dict : IndexedDict
#             Any IndexedDict that contains terms and definitions.
#
#         Returns
#         -------
#         str
#             term of the notes_dict at the provided index.
#         str
#             definition of the notes_dict at the provided index.
#
#         Raises
#         ------
#         NotesIndexError
#             If the provided index is out of range of the IndexedDict.
#         """
#
#         if notes_dict is None:
#             notes_dict = self.notes_paired
#         try:
#             return notes_dict.item_at(index)
#         except IndexError:
#             raise errors.NotesIndexError("The provided index was out of range.")
#
#     def pairs(self, indexes: list, *, notes_dict: IndexedDict=None):
#         """
#         Returns a list of (key, value) tuples that represent term and definition pairs.
#
#         Parameters
#         ----------
#         indexes : list of int
#             Indexes of the pairs.
#         notes_dict : IndexedDict
#             Any IndexedDict that contains terms and definitions.
#
#         Returns
#         -------
#         list of tuple(str, str)
#             The list of term and definition pairs.
#
#         Raises
#         ------
#         NotesIndexError
#             If one of the indexes are out of range of the IndexedDict.
#         """
#
#         if notes_dict is None:
#             notes_dict = self.notes_paired
#         try:
#             return notes_dict.items_at(indexes)
#         except IndexError:
#             raise errors.NotesIndexError("At least one of the provided indexes were out of range.")
#
#
# class CategorizedNoteUtil(PairedNoteUtil):
#     """
#     Uses prefixes to separate notes into categories, of which are either positional or generic.
#
#     Definitions may contain additional information, known as extensions, which are separated by new lines.
#         Extensions must be surrounded by given characters.
#
#     Generic terms are added to a category based on a generic prefix.
#     The position of generic terms do not matter and they will never be nested within another generic term.
#
#     Positional terms are added to a category based on their relative position in notes.
#     In order to nest positional terms,
#         the term must have a prefix of a previous positional prefix with its own additional prefix.
#
#     Attributes
#     ----------
#     error_message : str
#         Any errors that occur while making categorized notes.
#     extensions : list of tuple of either (str, str) or (str, str, str) or (str, str, str, str).
#         Each extension is a group of (name, surrounding character(s), place holder)
#         When an extension is found in a definition, it will be added to the end of the string, separated by a \n
#         Extensions can then optionally be removed from the main definition.
#         Case (str, str):
#             First str is name, second str is characters on both sides that surround the extension. No place holder.
#         Case (str, str, str):
#             First str is name, second str is starting bound, third str is ending bound. No place holder.
#         Case (str, str, str, str):
#             First str is name, second str is starting bound, third str is ending bound, fourth str is place holder.
#     generics : list of tuple of (str, str).
#         Each generic is a group of (name, prefix).
#         The name is independent of the terms themselves.
#         The position of generics do not matter, only that it starts with the prefix.
#     positionals : list of tuple of (str, str).
#         Each positional is a group of (name, prefix).
#         The name is independent of the term name itself.
#         Any terms with specifically that prefix will be added to the value of the name.
#
#     generic_dict : IndexedDict
#         A dictionary with keys of generic names and values of IndexedDicts of note pairs.
#         Each generic's name in generics serves as a key and the values are the note pairs as an IndexedDict.
#     extension_dict : IndexedDict
#         A dictionary with keys of each extension name and values of IndexedDicts.
#         Each dictionary will have terms that have the extension in their definition.
#     positional_dict : IndexedDict
#         A dictionary with keys of each positional name and values of IndexedDicts.
#         The positional dict ignores any nesting of prefixes.
#         The note pairs in positional dict are pairs that are exclusive only to that name and prefix.
#         An "Uncategorized" category contains all note pairs that do not have a category above them in the file.
#         "Uncategorized" is double nested to maintain continuity with the rest of positional_dict.
#     nested_dict : IndexedDict
#         A dictionary with keys of each positional name and values of a list of positional names that are nested in it.
#         Another positional is considered nested if the other positional's prefix starts with the positional's prefix.
#         Example : A positional key with prefix '&' will have a positional with prefix '&&' in its values
#             because '&&' starts with '&'.
#     notes_categorized : IndexedDict
#         A dictionary with keys of each positional name but values of IndexedDicts of note pairs from several categories.
#         Think of it as curriculum Units and Chapters.
#             All Units have Chapters, thus the Units will have all of the note pairs of the Chapters.
#             In this case, Unit may have a prefix of, for example, "~", and Chapter "~~".
#         For the notes to be nested, one inner one must start with the prefix of the outer one.
#         Otherwise, notes will not be added to the outer positional key.
#
#     Special Methods
#     ---------------
#         __str__()
#             Prints all of the variables separated by new lines.
#     """
#     def __init__(self, file_name: str, comments: list, delimeter: str, skip_warnings: bool=False,
#                  *, generics: list=None, positionals: list=None, extensions: list=None,
#                  ignore_generics: bool=False, filter_extensions: bool=True,
#                  remove_categories: bool=True):
#         """
#         Sets up all variables and creates notes.
#
#         Parameters
#         ----------
#         file_name : str
#             Name of the file to retrieve notes from.
#         comments : list of str
#             All prefixes to ignore while reading notes.
#         delimeter : str
#             Character that separates terms from definitions.
#         skip_warnings : bool
#             Whether to not print out the error message.
#         generics : list of tuple(str, str)
#             List of generics that are in the tuple (name, prefix)
#         positionals : list of tuple(str, str)
#             List of positionals that are in the tuple (name, prefix).
#         extensions : list of tuple(str, str)
#             List of extensions that are tuples.
#         ignore_generics : bool
#             Whether to exclude generic terms from the positional and categorized notes.
#         filter_extensions : bool
#             Whether to remove extensions from the main definition.
#         remove_categories : bool
#             Whether to remove lines with the category prefix from the notes.
#         """
#
#         super().__init__(file_name, comments, delimeter, skip_warnings=True)
#         self.error_message = ""
#
#         self.positional_list = positionals
#         self.generic_list = generics
#         self.extension_list = extensions
#
#         self.notes_extended = copy.deepcopy(self.notes_split)
#         self.generic_dict = IndexedDict()
#         self.extension_dict = IndexedDict()
#         self.positional_dict = IndexedDict()
#         self.nested_dict = IndexedDict()
#         self.notes_categorized = IndexedDict()
#
#         if extensions is not None:
#             self._add_extensions(filter_extensions)
#             for nb in extensions:
#                 self.extension_dict[nb[0]] = IndexedDict()
#             self._make_extension_dict(ignore_generics)
#
#         if generics is not None:
#             for name, prefix in generics:
#                 self.generic_dict[name] = IndexedDict()
#             self._make_generic_dict()
#
#         if positionals is not None:
#             for name, prefix in positionals:
#                 self.positional_dict[name] = IndexedDict()
#             self.positional_dict["Uncategorized"] = IndexedDict()
#             self.positional_dict["Uncategorized"]["Uncategorized"] = IndexedDict()
#             self._make_positional_dict(ignore_generics)
#             self._make_notes_categorized(ignore_generics)
#
#         self._clean_categories(remove_categories)
#         self._make_notes_paired(notes_split=self.notes_extended)
#
#         if not skip_warnings:
#             print(self.error_message)
#
#     def __str__(self):
#         """
#         Turns all variables into strings.
#
#         Returns
#         -------
#         str
#             All variables separated by new lines.
#         """
#
#         message = super().__str__() + "\n"
#         message += "CategorizedNoteUtil: \n\n"
#         message += "Positionals: " + str(self.positional_list) + "\n"
#         message += "Generics: " + str(self.generic_list) + "\n"
#         message += "Extensions: " + str(self.extension_list) + "\n"
#
#         message += "Notes extended: " + str(self.notes_extended) + "\n"
#         message += "Generic dict: " + str(self.generic_dict) + "\n"
#         message += "Extension dict: " + str(self.extension_dict) + "\n"
#         message += "Positional dict: " + str(self.positional_dict) + "\n"
#         message += "Nested dict: " + str(self.nested_dict) + "\n"
#         message += "Notes categorized: " + str(self.notes_categorized) + "\n"
#
#         return message
#
#     def _add_extensions(self, filter_extensions: bool=True):
#         """
#         Adds extensions (as provided with the extensions parameter in __init__, to each definition.
#
#         The notes_extended list is what contains definitions with extensions, and is separate from notes_split.
#
#         Parameters
#         ----------
#         filter_extensions : bool
#             Whether to remove extensions from the main definition of the term.
#
#         Returns
#         -------
#         None
#         """
#
#         if self.extension_list is not None:
#             for i in range(len(self.notes_extended)):
#                 if len(self.notes_extended[i]) != 2:
#                     continue
#
#                 orig_len = len(self.notes_extended[i][1])
#                 for nb in self.extension_list:
#                     start_len = 0
#                     name, bound1, bound2, place_holder = None, None, None, ""
#                     if len(nb) == 2:
#                         name, bound1 = nb
#                         bound2 = bound1
#                     elif len(nb) == 3:
#                         name, bound1, bound2 = nb
#                     elif len(nb) == 4:
#                         name, bound1, bound2, place_holder = nb
#
#                     while True:     # There could be multiple extensions of a single name.
#                         try:
#                             try:
#                                 b1 = self.notes_extended[i][1].index(bound1, start_len, orig_len)
#                             except ValueError:
#                                 # No extensions left for this term, move to next extension
#                                 break
#
#                             try:
#                                 b2 = self.notes_extended[i][1].index(bound2, b1 + 1, orig_len)
#                             except ValueError:
#                                 # Only one bound is an error
#                                 raise errors.MissingBoundError
#
#                             self.notes_extended[i][1] += "\n" + name + self.delimeter + " " + \
#                                                          self.notes_extended[i][1][b1 + len(bound1): b2]
#                             if filter_extensions:
#                                 self.notes_extended[i][1] = self.notes_extended[i][1][:b1] + place_holder + \
#                                                             self.notes_extended[i][1][b2 + len(bound2):]
#                                 orig_len -= (b2 - b1) + len(bound1) - len(place_holder)
#                                 start_len -= b2 + len(bound2) - len(place_holder)
#                             start_len += b2 + len(bound2)
#                             self.notes_extended[i][1] = self.notes_extended[i][1].strip()
#
#                             if "\n" not in self.notes_extended[i][1]:
#                                 self.notes_extended[i][1] = "\n" + self.notes_extended[i][1]
#                                 raise errors.NoDefinitionError
#
#                         except errors.MissingBoundError:
#                             self.error_message += "WARNING: Missed bound at around line " + str(i+1) + ".\n"
#                             self.error_message += "Extension was ignored: " + str(self.notes_extended[i]) + "\n"
#                             print(start_len, orig_len)
#                             break
#                         except errors.NoDefinitionError:
#                             self.error_message += "WARNING: No definition at around line " + str(i+1) + ".\n"
#                             self.error_message += "Pair was still added: " + str(self.notes_extended[i]) + "\n"
#
#     def _make_generic_dict(self):
#         """
#         Creates a dict of keys as the name of generics and values as all terms and definitions with that generic.
#
#         Returns
#         -------
#         None
#         """
#         for i in range(len(self.notes_extended)):
#
#             if len(self.notes_extended[i]) != 2:
#                 continue
#
#             if self.generic_list is not None:
#                 for n, p in self.generic_list:
#                     if self.notes_extended[i][0].startswith(p):
#                         self.notes_extended[i][0] = self.notes_extended[i][0][len(p):].strip()
#                         self.generic_dict[n][self.notes_extended[i][0]] = self.notes_extended[i][1]
#
#     def _make_extension_dict(self, ignore_generics: bool=False):
#         """
#         Creates a dict of keys as the name of extensions and values as all terms and definitions with that extension.
#
#         Parameters
#         ----------
#         ignore_generics : bool
#             Whether to ignore generics while creating this dictionary.
#
#         Returns
#         -------
#         None
#         """
#
#         for i in range(len(self.notes_extended)):
#             if len(self.notes_extended[i]) != 2:
#                 continue
#
#             is_generic = False
#             prefix = None
#             if self.generic_list is not None:
#                 for n, p in self.generic_list:
#                     if self.notes_extended[i][0].startswith(p):
#                         is_generic = True
#                         prefix = p
#                         break
#                 if ignore_generics and is_generic:
#                     continue
#
#             split_extensions = self.notes_extended[i][1].split("\n")
#             for ex in split_extensions:
#                 for nb in self.extension_list:
#                     if ex.startswith(nb[0]):
#                         if is_generic:
#                             self.extension_dict[nb[0]][self.notes_extended[i][0][len(prefix):].strip()] \
#                                 = self.notes_extended[i][1]
#                         else:
#                             self.extension_dict[nb[0]][self.notes_extended[i][0]] = self.notes_extended[i][1]
#
#     def _make_positional_dict(self, ignore_generics: bool=False):
#         """
#         Makes a dict where each term and definition is under the correct category.
#
#         Creates a dict of keys as names of positionals and values as another dict of keys as names of the notes
#         positional with the value of an IndexedDict with terms and definitions in that positional.
#
#         Parameters
#         ----------
#         ignore_generics : bool
#             Whether to ignore generic terms while creating this dict.
#
#         Returns
#         -------
#         None
#         """
#
#         name, prefix, curr = None, None, None
#         for i in range(len(self.notes_extended)):
#
#             if self.generic_list is not None:
#                 is_generic = False
#                 for n, p in self.generic_list:
#                     if self.notes_extended[i][0].startswith(p):
#                         is_generic = True
#                         break
#                 if is_generic and ignore_generics:
#                     continue
#
#             for n, p in self.positional_list[::-1]:
#                 if self.notes_extended[i][0].startswith(p):
#                     name, prefix, curr = n, p, self.notes_extended[i][0][len(p):].strip()
#                     self.positional_dict[name][curr] = IndexedDict()
#                     break
#             else:
#                 if len(self.notes_extended[i]) != 2:
#                     continue
#                 if name is None or prefix is None:
#                     self.positional_dict["Uncategorized"]["Uncategorized"][
#                         self.notes_extended[i][0]] = self.notes_extended[i][1]
#                 else:
#                     self.positional_dict[name][curr][self.notes_extended[i][0]] = self.notes_extended[i][1]
#
#     def _make_notes_categorized(self, ignore_generics: bool=False):
#         """
#         Creates a dict with keys as positional names and values as all terms and definitions "under" that category.
#
#         Parameters
#         ----------
#         ignore_generics : bool
#             Whether to ignore generic terms while creating this dict.
#
#         Returns
#         -------
#         None
#         """
#
#         for name in self.positional_dict.keys():
#             for category in self.positional_dict[name].keys():
#                 self.notes_categorized[category] = IndexedDict()
#
#         self.notes_categorized["Uncategorized"] = self.positional_dict["Uncategorized"]["Uncategorized"]
#
#         for name, prefix in self.positional_list:
#             curr = None
#             for i in range(len(self.notes_extended)):
#
#                 if ignore_generics:
#                     is_generic = False
#                     for n, p in self.generic_list:
#                         if self.notes_extended[i][0].startswith(p):
#                             is_generic = True
#                             break
#                     if is_generic:
#                         continue
#
#                 if self.notes_extended[i][0].startswith(prefix):
#                     for n, p in self.positional_list[::-1]:
#                         if n == name:
#                             curr = self.notes_extended[i][0][len(prefix):].strip()
#                             self.nested_dict[curr] = []
#                             break
#                         elif self.notes_extended[i][0].startswith(p):
#                             if p.startswith(prefix):
#                                 self.nested_dict[curr].append(self.notes_extended[i][0][len(p):].strip())
#                                 break
#                     continue
#                 else:
#                     for n, p in self.positional_list[::-1]:
#                         if self.notes_extended[i][0].startswith(p):
#                             if p != prefix and not p.startswith(prefix):
#                                 curr = None
#                     if len(self.notes_extended[i]) != 2:
#                         continue
#                     elif curr is None:
#                         continue
#                     else:
#                         self.notes_categorized[curr][self.notes_extended[i][0]] = self.notes_extended[i][1]
#
#     def _clean_categories(self, remove_categories: bool=True):
#         """
#         Removes all prefixes from notes_extended and notes_split terms that start with a category prefix.
#
#         Parameters
#         ----------
#         remove_categories : bool
#             Whether to remove the whole line altogether.
#
#         Returns
#         -------
#         None
#         """
#
#         for i in range(len(self.notes_extended) - 1, -1, -1):
#             if self.positional_list is not None:
#                 for n, p in self.positional_list:
#                     if self.notes_extended[i][0].startswith(p):
#                         if remove_categories:
#                             del self.notes_extended[i]
#                         else:
#                             self.notes_extended[i][0] = self.notes_extended[i][0][len(p):].strip()
#             if self.generic_list is not None:
#                 for n, p in self.generic_list:
#                     if self.notes_extended[i][0].startswith(p):
#                         self.notes_extended[i][0] = self.notes_extended[i][0][len(p):].strip()
#
#         for i in range(len(self.notes_split) - 1, -1, -1):
#             if self.positional_list is not None:
#                 for n, p in self.positional_list:
#                     if self.notes_split[i][0].startswith(p):
#                         if remove_categories:
#                             del self.notes_split[i]
#                         else:
#                             self.notes_split[i][0] = self.notes_split[i][0][len(p):].strip()
#             if self.generic_list is not None:
#                 for n, p in self.generic_list:
#                     if self.notes_split[i][0].startswith(p):
#                         self.notes_split[i][0] = self.notes_split[i][0][len(p):].strip()
#
#     def format(self, width: int=40, tabsize: int=4):
#         """
#         Formats the notes in the way the noteutil read it.
#
#         First it adds all the notes in the positional categories, indicating nested positions with tabs.
#         Then it puts the generic terms at the bottom, after the positional terms.
#
#         Returns
#         -------
#         str
#             What was read from the note file.
#         """
#
#         formatted = ""
#         wrapper = textwrap.TextWrapper(width=width, tabsize=tabsize, replace_whitespace=False, drop_whitespace=True,
#                                        expand_tabs=False)
#
#         if self.positional_list is not None:
#             for term, definition in self.notes_categorized["Uncategorized"].items():
#                 wrapper.initial_indent = ""
#                 wrapper.subsequent_indent = "\t"
#
#                 formatted += wrapper.fill("{0}{1} {2}".format(term, self.delimeter, definition.split("\n")[0])) + "\n"
#
#                 wrapper.initial_indent = "\t"
#                 wrapper.subsequent_indent = "\t\t"
#                 for ext in definition.split("\n")[1:]:
#                     formatted += wrapper.fill(ext) + "\n"
#
#             formatted += "\n"
#
#             def dfs(name: str, tabs: int):
#                 nonlocal formatted
#
#                 wrapper.initial_indent = tabs * "\t"
#                 wrapper.subsequent_indent = (tabs + 1) * "\t"
#                 formatted += wrapper.fill(name) + "\n"
#
#                 tabs += 1
#
#                 for n in self.positional_dict.keys():
#                     try:
#                         idi = self.positional_dict[n].val_with(key=name)
#                         break
#                     except ValueError:
#                         continue
#                 else:
#                     raise errors.NoCategoryError("A category was in the nested dict but not the positional dict.")
#
#                 for t, d in idi.items():
#                     wrapper.initial_indent = tabs * "\t"
#                     wrapper.subsequent_indent = (tabs + 1) * "\t"
#
#                     formatted += wrapper.fill("{0}{1} {2}".format(t, self.delimeter, d.split("\n")[0])) + "\n"
#
#                     tabs += 1
#                     wrapper.initial_indent = tabs * "\t"
#                     wrapper.subsequent_indent = (tabs + 1) * "\t"
#
#                     for e in d.split("\n")[1:]:
#                         formatted += wrapper.fill(e) + "\n"
#
#                     tabs -= 1
#
#                 if self.nested_dict[name]:
#                     for nest in self.nested_dict[name]:
#                         dfs(nest, tabs)
#
#             for cat in self.nested_dict.keys():
#                 for nested in self.nested_dict.values():
#                     if cat in nested:
#                         break
#                 else:
#                     dfs(cat, 0)
#         else:
#             formatted += super().format()
#
#         formatted += "\n"
#
#         if self.generic_dict is not None:
#             for n, idict in self.generic_dict.items():
#                 wrapper.initial_indent = ""
#                 wrapper.subsequent_indent = "\t"
#
#                 formatted += wrapper.fill(n) + "\n"
#
#                 for term, definition in idict.items():
#                     wrapper.initial_indent = "\t"
#                     wrapper.subsequent_indent = "\t\t"
#                     formatted += wrapper.fill("{0}{1} {2}".format(
#                         term, self.delimeter, definition.split("\n")[0])) + "\n"
#                     wrapper.initial_indent = "\t\t"
#                     wrapper.subsequent_indent = "\t\t\t"
#                     for ext in definition.split("\n")[1:]:
#                         formatted += wrapper.fill(ext) + "\n"
#
#         return formatted
#
#     def term(self, *, notes_dict: IndexedDict=None,
#              index: int=None, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """Excludes extensions from definition while searching."""
#
#         return super().term(notes_dict=notes_dict, index=index, term=term, definition=definition, func=func)
#
#     def definition(self, *, notes_dict: IndexedDict=None,
#                    index: int=None, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """Excludes extensions from definition while searching."""
#
#         return super().definition(notes_dict=notes_dict, index=index, term=term, definition=definition, func=func)
#
#     def pair_index(self, *, notes_dict: IndexedDict=None,
#                    term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """Excludes extensions from definition while searching."""
#
#         return super().pair_index(notes_dict=notes_dict, term=term, definition=definition, func=func)
#
#     def terms(self, *, notes_dict: IndexedDict=None,
#               indexes: int=None, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """Excludes extensions from definition while searching."""
#
#         return super().terms(notes_dict=notes_dict, indexes=indexes, term=term, definition=definition, func=func)
#
#     def definitions(self, *, notes_dict: IndexedDict = None,
#                     indexes: int=None, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """Excludes extensions from definition while searching."""
#
#         return super().definitions(notes_dict=notes_dict, indexes=indexes, term=term, definition=definition, func=func)
#
#     def pair_indexes(self, *, notes_dict: IndexedDict=None,
#                      term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """Excludes extensions from definition while searching."""
#
#         return super().pair_indexes(notes_dict=notes_dict, term=term, definition=definition, func=func)
#
#     def extension(self, name: str, *, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """
#         Finds all values of the extension of a definition given the name of the extension.
#
#         Parameters
#         ----------
#         name : str
#             Name of the extension of the wanted value.
#         term : str, optional if definition is provided.
#             Name of the term to find.
#         definition : str, optional if the term is provided.
#             Name of the definition to find.
#         func : function
#             Removes the extensions from the definition if left blank.
#             Otherwise applies this function to the term, definition, and key and value of the parameter and notes dict.
#
#         Returns
#         -------
#         list of str
#             All values of the wanted extension.
#
#         Raises
#         ------
#         NoExtensionError
#             If the term has no extension or the name of the extension given was incorrect.
#         """
#
#         all_values = []
#         for ex in self.extension_dict.keys():
#             if name.lower() == ex.lower():
#                 exact_definition = self.definition(notes_dict=self.extension_dict[ex],
#                                                    term=term, definition=definition, func=func)
#                 extensions = exact_definition.split("\n")[1:]
#                 for ext in extensions:
#                     if ext.startswith(ex):
#                         all_values.append(ext[ext.index(self.delimeter) + len(self.delimeter) + 1:])
#         if not all_values:
#             raise errors.NoExtensionError(
#                 "The definition found from the provided term or definition did not have this extension.")
#         return all_values
#
#     def category(self, *, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """
#         Finds whether the term is part of a generic or positional category.
#
#         Parameters
#         ----------
#         term : str, optional if definition is provided.
#             Name of the term to find.
#         definition : str, optional if the term is provided.
#             Name of the definition to find.
#         func : function
#             Removes the extensions from the definition if left blank.
#             Otherwise applies this function to the term, definition, and key and value of the parameter and notes dict.
#
#         Returns
#         -------
#         str
#             The name of the category the term is a part of.
#
#         Raises
#         ------
#         NoCategoryError
#             If no category is found.
#         """
#
#         for g in self.generic_dict.keys():
#             if func is not None:
#                 if func(term) == func(g):
#                     return g
#             else:
#                 if term == g:
#                     return g
#
#             try:
#                 self.term(notes_dict=self.generic_dict[g], term=term, definition=definition,
#                           func=func)
#             except errors.NotesNotFoundError:
#                 pass
#             else:
#                 return g
#
#         for n in self.positional_dict.keys():
#             for c in self.positional_dict[n].keys():
#                 if func is not None:
#                     if func(term) == func(c):
#                         return c
#                 else:
#                     if term == c:
#                         return c
#
#                 try:
#                     self.term(notes_dict=self.positional_dict[n][c], term=term, definition=definition, func=func)
#                 except errors.NotesNotFoundError:
#                     pass
#                 else:
#                     return c
#         raise errors.NoCategoryError("No category was found. Term: {0}. Definition: {1}".format(
#             func(term) if func is not None else term, func(definition) if func is not None else definition))
#
#     def extensions(self, *, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """
#         Returns all extensions that a term has.
#
#         Parameters
#         ----------
#         term : str, optional if definition is provided.
#             Name of the term to find.
#         definition : str, optional if the term is provided.
#             Name of the definition to find.
#         func : function
#             Removes the extensions from the definition if left blank.
#             Otherwise applies this function to the term, definition, and key and value of the parameter and notes dict.
#
#         Returns
#         -------
#         dict
#             Keys of the name of the extension with the value as a list of all values of that extension.
#
#         Raises
#         ------
#         NoExtensionError
#             If no extensions are found.
#         """
#
#         all_extensions = {}
#         for ex in self.extension_dict.keys():
#             try:
#                 exact_definition = self.definition(notes_dict=self.extension_dict[ex],
#                                                    term=term, definition=definition, func=func)
#             except errors.NotesNotFoundError:
#                 continue
#
#             extensions = exact_definition.split("\n")[1:]
#             for ext in extensions:
#                 if ext.startswith(ex):
#                     try:
#                         all_extensions[ex].append(ext[ext.index(self.delimeter) + len(self.delimeter) + 1:])
#                     except KeyError:
#                         all_extensions[ex] = [ext[ext.index(self.delimeter) + len(self.delimeter) + 1:]]
#         if not all_extensions:
#             raise errors.NoExtensionError(
#                 "The definition from the provided term or definition did not have any extensions.")
#
#         return all_extensions
#
#     def positionals(self, name: str, func=lambda x: x.lower()):
#         """
#         Returns all positional names that correspond to the provided name.
#
#         Parameters
#         ----------
#         name : str
#             The name of the positional given in the positionals list.
#         func : function
#             A function applied to the names. This makes checks case insensitive by default.
#
#         Returns
#         -------
#         list of str
#             All of the names of the positionals that fall under the provided name.
#         """
#
#         for n in self.positional_dict.keys():
#             if func(n) == func(name):
#                 return list(self.positional_dict[n].keys())
#
#     def categories(self, *, term: str=None, definition: str=None, func=lambda x: x.lower().split("\n")[0]):
#         """
#         Returns all positional categories the term is a part of.
#
#         Parameters
#         ----------
#         term : str, optional if definition is provided.
#             Name of the term to find.
#         definition : str, optional if the term is provided.
#             Name of the definition to find.
#         func : function
#             Removes the extensions from the definition if left blank.
#             Otherwise applies this function to the term, definition, and key and value of the parameter and notes dict.
#
#         Returns
#         -------
#         list of str
#             All names of the categories the term is a part of.
#
#         Raises
#         ------
#         NoCategoryError
#             If no categories are found.
#         """
#
#         all_categories = []
#         for n in self.notes_categorized.keys():
#             try:
#                 self.term(notes_dict=self.notes_categorized[n], term=term, definition=definition, func=func)
#             except errors.NotesNotFoundError:
#                 pass
#             else:
#                 all_categories.append(n)
#         if not all_categories:
#             raise errors.NoCategoryError("The term from the provided term or definition did not have any categories.")
#
#         return all_categories
