# import random
#
#
# class Quiz:
#     """
#     Organizes questions through generation of lines from notes.
#
#     With just a bare NoteUtil, there's not much to quiz besides just returning the lines.
#
#     Keys are used for to_dict().
#     Keys that are used for converting to a dictionary or setting the current notes:
#         For dictionary:
#             KEY_ALL_INDEXES : str
#                 All of the keys are constructed from KEY_LIST + either CHRONOLOGICAL or RANDOM suffix.
#                 KEY_LINE_INDEX : str
#                 KEY_LINE_INDEXES : str
#                 KEY_CORRECT_INDEX : str
#                 KEY_CORRECT_INDEXES : str
#                 KEY_INCORRECT_INDEX : str
#                 KEY_INCORRECT_INDEXES : str
#                 KEY_LAST_INDEX : str
#                     Last index generated.
#             KEY_RANDOM : str
#             KEY_CORRECT_LIST : str
#             KEY_INCORRECT_LIST : str
#         For current notes:
#             KEY_LINES_NOTES : str
#             KEY_CORRECT_LIST : str
#             KEY_INCORRECT_LIST : str
#
#     Attributes
#     ----------
#         all_indexes : dict of {str: str}
#             line_index : int
#                 Index to the next line to pass chronologically.
#             line_indexes : list of int
#                 Indexes to lines that have not been retrieved randomly yet.
#             correct_line_index : int
#                 Index to the next line in the correct list.
#             correct_line_indexes : list of int
#                 Indexes to random lines in the correct list.
#             incorrect_line_index : int
#                 Index to the next line in the incorrect list.
#             incorrect_line_indexes : list of int
#                 Indexes to random lines in the incorrect list.
#             last_index : int
#                 Index to the previous line that was retrieved.
#         current_notes : str
#             A key to the current notes being used (KEY_NOTES_LIST, KEY_CORRECT_LIST, or KEY_INCORRECT_LIST)
#         random : bool
#             Whether to return random lines or chronological ones.
#         all_lists : dict of {str: list}
#             notes_list : list of str
#                 The notes list from noteutil.
#             correct_list : list of str
#                 Subset of notes that contain questions the user answered correctly.
#             incorrect_list : list of str
#                 Subset of notes that contain questions the user answered incorrectly.
#     """
#
#     CHRONOLOGICAL_SUFFIX = "_chronological_index"
#     RANDOM_SUFFIX = "_random_indexes"
#     LIST_SUFFIX = "_list"
#
#     KEY_ALL_INDEXES = "all_indexes"
#     KEY_ALL_LISTS = "all_lists"
#
#     KEY_NOTES = "notes"
#
#     KEY_CORRECT = "correct"
#
#     KEY_INCORRECT = "incorrect"
#
#     KEY_CURRENT_NOTES = "current_notes"
#
#     KEY_LAST_INDEX = "last_index"
#     KEY_RANDOM = "random"
#
#     def __init__(self, noteutil):
#         """
#         Initialize all variables that relate to quizzing and notes.
#
#         Parameters
#         ----------
#         noteutil : NoteUtil
#             The note utility that was made from a file of notes.
#         """
#
#         self.noteutil = noteutil
#
#         self.all_indexes = {self.KEY_NOTES + self.CHRONOLOGICAL_SUFFIX: 0,
#                             self.KEY_NOTES + self.RANDOM_SUFFIX: [x for x in range(len(self.noteutil.notes_list))],
#                             self.KEY_CORRECT + self.CHRONOLOGICAL_SUFFIX: 0,
#                             self.KEY_CORRECT + self.RANDOM_SUFFIX: [],
#                             self.KEY_INCORRECT + self.CHRONOLOGICAL_SUFFIX: 0,
#                             self.KEY_INCORRECT + self.RANDOM_SUFFIX: [],
#                             self.KEY_LAST_INDEX: 0}
#
#         random.shuffle(self.all_indexes[self.KEY_NOTES + self.RANDOM_SUFFIX])
#
#         self.all_lists = {self.KEY_NOTES + self.LIST_SUFFIX: self.noteutil.notes_list,
#                           self.KEY_CORRECT + self.LIST_SUFFIX: [],
#                           self.KEY_INCORRECT + self.LIST_SUFFIX: []}
#
#         self.current_notes = self.KEY_NOTES
#         self.random = False
#
#     def __str__(self):
#         """
#         Converts all variables into strings and labels them.
#
#         Returns
#         -------
#         str
#             All variables as strings and separated by new lines.
#         """
#
#         message = "Quiz: \n\n"
#
#         message += "All indexes: \n"
#         for key in self.all_indexes.keys():
#             message += key + ": " + str(self.all_indexes[key]) + "\n"
#
#         message += "All lists: \n"
#         for key in self.all_lists.keys():
#             message += key + ": " + str(self.all_lists[key]) + "\n"
#
#         message += "Current notes: " + str(self.current_notes) + "\n"
#
#         message += "Last index: " + str(self.all_indexes[self.KEY_LAST_INDEX]) + "\n"
#         message += "Random: " + str(self.random) + "\n"
#
#         return message + "\n"
#
#     def to_dict(self):
#         """
#         Converts all variables into a dictionary using key constants.
#
#         Does not convert the noteutil.
#
#         Returns
#         -------
#         dict
#             Dictionary of all variables {KEY_CONSTANT: variable}.
#         """
#
#         quiz = dict()
#         quiz[self.KEY_ALL_INDEXES] = self.all_indexes
#
#         ignore_keys = [self.KEY_NOTES + self.LIST_SUFFIX]
#         filtered_dict = dict()
#         for k in self.all_lists:
#             if k not in ignore_keys:
#                 filtered_dict[k] = self.all_lists[k]
#         quiz[self.KEY_ALL_LISTS] = filtered_dict
#
#         quiz[self.KEY_CURRENT_NOTES] = self.current_notes
#         quiz[self.KEY_RANDOM] = self.random
#         return quiz
#
#     def parse_dict(self, var_dict: dict):
#         """
#         Sets class variables by reading a dictionary.
#
#         Reads using the key constants the dictionary should have been created with.
#
#         Parameters
#         ----------
#         var_dict : dict
#             Should be a dictionary created from to_dict().
#             Contains all of the keys and values of a saved Quiz state.
#
#         Returns
#         -------
#         None
#         """
#
#         self.all_indexes.update(var_dict[Quiz.KEY_ALL_INDEXES])
#         self.all_lists.update(var_dict[Quiz.KEY_ALL_LISTS])
#         self.current_notes = var_dict[Quiz.KEY_CURRENT_NOTES]
#         self.random = var_dict[Quiz.KEY_RANDOM]
#
#     def line(self, notes_key: str=None):
#         """
#         Retrieves a line of notes, moving chronologically or randomly.
#
#         Resets to the first (top) line when all lines have been retrieved.
#         Resets the random indexes when all indexes have been generated randomly.
#
#         Parameters
#         ----------
#         notes_key : list, optional - default is current_notes.
#             Key for a list of notes, such as KEY_NOTES_LIST, or KEY_CORRECT_LIST.
#
#         Returns
#         -------
#         str
#             The next line in the notes list or a random line that hasn't been requested before.
#         bool
#             Whether the chronological index or random index has cycled.
#         """
#
#         repeat = False
#         if notes_key is None:
#             notes_key = self.current_notes
#         notes_list = self.all_lists[notes_key + self.LIST_SUFFIX]
#         rand_list = self.all_indexes[notes_key + self.RANDOM_SUFFIX]
#         chrono_index = self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX]
#
#         if self.random:
#             rand_index = rand_list.pop()
#             line = notes_list[rand_index]
#             self.all_indexes[self.KEY_LAST_INDEX] = self.noteutil.line_index(name=line)
#
#             if not rand_list:
#                 self.all_indexes[notes_key + self.RANDOM_SUFFIX] = [x for x in range(len(notes_list))]
#                 random.shuffle(self.all_indexes[notes_key + self.RANDOM_SUFFIX])
#                 repeat = True
#
#         else:
#             line = notes_list[chrono_index]
#             self.all_indexes[self.KEY_LAST_INDEX] = self.noteutil.line_index(name=line)
#
#             self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] += 1
#
#             if self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] == len(notes_list):
#                 self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] = 0
#                 repeat = True
#
#         return line, repeat
#
#     def add_line(self, *, notes_key: str=None,
#                  last: bool=False, index: int=None, name: str=None, func=lambda x: x.lower()):
#         """
#         Adds a line of notes to the correct list.
#
#         Parameters
#         ----------
#         notes_key: str, optional - default is current_notes.
#             Key to one of the notes lists.
#         last : bool, optional if one of the other two is provided.
#             Add the line that corresponds to the last index used.
#         index : int, optional if one of the other two is provided.
#             Add the line that corresponds to the provided index in notes_list.
#         name : str, optional if one of the other two is provided.
#             Part of or the entire line of notes, must be unique to that notes line. Add the line found.
#         func : function, Optional
#             Function to apply to the name and line, default is case insensitive.
#
#         Returns
#         -------
#         None
#
#         Raises
#         ------
#         ForbiddenEdit
#             If the notes_paired was attempted to be edited.
#         DuplicateError
#             If the line is already in the selected list.
#         NotesNotFoundError
#             If the no lines were found from the name.
#         MultipleFoundError
#             If more than 1 line was found from the name.
#         """
#
#         if notes_key is None:
#             notes_key = self.current_notes
#
#         if notes_key == self.KEY_NOTES:
#             raise errors.ForbiddenEdit
#
#         notes_list = self.all_lists[notes_key + self.LIST_SUFFIX]
#         rand_list = self.all_indexes[notes_key + self.RANDOM_SUFFIX]
#
#         if last:
#             last_index = self.all_indexes[self.KEY_LAST_INDEX]
#
#             if self.noteutil.line(index=last_index) in notes_list:
#                 raise errors.DuplicateError
#             else:
#                 notes_list.append(self.noteutil.line(index=last_index))
#
#             rand_list.insert(random.randint(0, len(notes_list)), len(notes_list) - 1)
#             return
#
#         if index is not None:
#             if self.noteutil.line(index=index) in notes_list:
#                 raise errors.DuplicateError
#             else:
#                 notes_list.append(self.noteutil.line(index=index))
#
#             rand_list.insert(random.randint(0, len(notes_list)), len(notes_list) - 1)
#             return
#
#         if name is not None:
#             try:
#                 line = self.noteutil.line(name=name, func=func)
#
#                 if line in notes_list:
#                     raise errors.DuplicateError
#                 notes_list.append(line)
#                 rand_list.insert(random.randint(0, len(notes_list)), len(notes_list) - 1)
#                 return
#
#             except errors.NotesNotFoundError:  # Try again with the lines method.
#                 pass
#
#             lines = self.noteutil.lines(name=name, func=func)
#             if len(lines) > 1:
#                 raise errors.MultipleFoundError("More than one line found.")
#
#             line = lines[0]
#
#             if line in notes_list:
#                 raise errors.DuplicateError
#             else:
#                 notes_list.append(line)
#                 rand_list.insert(random.randint(0, len(notes_list)), len(notes_list) - 1)
#
#     def remove_line(self, *, notes_key: str=None,
#                     last: bool=False, index: int=None, name: str=None, func=lambda x: x.lower()):
#         """
#         Removes a line of notes from the correct list.
#
#         Parameters
#         ----------
#         notes_key : str
#             Key to one of the note lists.
#         last : bool, optional if one of the other two is provided.
#             Add the line that corresponds to the last index used.
#         index : int, optional if one of the other two is provided.
#             Add the line that corresponds to the provided index in notes_list.
#         name : str, optional if one of the other two is provided.
#             Part of or the entire line of notes, must be unique to that notes line. Add the line found.
#         func : function, Optional
#             Function to apply to the name and line, default is case insensitive.
#
#         Returns
#         -------
#         None
#
#         Raises
#         ------
#         ForbiddenEdit
#             If the notes_paired was attempted to be edited.
#         NotesNotFoundError
#             If the no lines were found from the name.
#             If the line was not in the dictionary to begin with.
#         MultipleFoundError
#             If more than one line was found from the name.
#         """
#
#         if notes_key is None:
#             notes_key = self.current_notes
#
#         if notes_key == self.KEY_NOTES:
#             raise errors.ForbiddenEdit
#
#         notes_list = self.all_lists[notes_key + self.LIST_SUFFIX]
#         rand_list = self.all_indexes[notes_key + self.RANDOM_SUFFIX]
#         chrono_index = self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX]
#
#         if last:
#             last_index = self.all_indexes[self.KEY_LAST_INDEX]
#             line = self.noteutil.line(index=last_index)
#             line_index = notes_list.index(line)
#
#             if line in notes_list:
#
#                 if line_index <= chrono_index:
#                     self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#                 for i in range(len(rand_list) - 1, -1, -1):
#                     if rand_list[i] > line_index:
#                         rand_list[i] -= 1
#                     elif rand_list[i] == line_index:
#                         del rand_list[i]
#
#                 del notes_list[line_index]
#             else:
#                 raise errors.NotesNotFoundError
#             return
#
#         if index is not None:
#             line = self.noteutil.line(index=index)
#             line_index = notes_list.index(line)
#
#             if line in notes_list:
#                 if line_index <= chrono_index:
#                     self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#                 for i in range(len(rand_list) - 1, -1, -1):
#                     if rand_list[i] > line_index:
#                         rand_list -= 1
#                     elif rand_list[i] == line_index:
#                         del rand_list[i]
#
#                 del notes_list[line_index]
#             else:
#                 raise errors.NotesNotFoundError
#             return
#
#         if name is not None:
#
#             try:
#                 line = self.noteutil.line(name=name, func=func)
#                 line_index = notes_list.index(line)
#
#                 if line not in notes_list:
#                     raise errors.NotesNotFoundError
#
#                 if line_index <= chrono_index:
#                     self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#
#                 for i in range(len(rand_list) - 1, -1, -1):
#                     if rand_list[i] > line_index:
#                         rand_list[i] -= 1
#                     elif rand_list[i] == line_index:
#                         del rand_list[i]
#
#                 del notes_list[line_index]
#
#             except errors.NotesNotFoundError:  # Try again with the lines method.
#                 pass
#
#             lines = self.noteutil.lines(name=name, func=func)
#
#             if len(lines) > 1:
#                 raise errors.MultipleFoundError
#
#             line = lines[0]
#             line_index = notes_list.index(line)
#
#             if line not in notes_list:
#                 raise errors.NotesNotFoundError
#
#             if line_index <= chrono_index:
#                 self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#
#             for i in range(len(rand_list) - 1, -1, -1):
#                 if rand_list[i] > line_index:
#                     rand_list[i] -= 1
#                 elif rand_list[i] == line_index:
#                     del rand_list[i]
#
#             del notes_list[line_index]
#
#     def lookup_lines(self, *, indexes: list=None, name: str=None, func=lambda x: x.lower()):
#         """
#         Searches through all lines of notes and adds them to a list.
#
#         Parameters
#         ----------
#         indexes : list of int
#             Specific indexes in the noteutil notes_list to add.
#         name : str
#             A string that occurs in lines of notes. Any line that has this name in it will be added.
#         func : function, Optional
#             Function to apply to the name and line, default is case insensitive.
#
#         Returns
#         -------
#         list of str
#             The list of lines that includes either the line of the index or all lines that matched with the name.
#         """
#
#         lines = []
#         if indexes is not None:
#             for index in indexes:
#                 lines.append(self.noteutil.line(index=index))
#         if name is not None:
#             for line in self.noteutil.lines(name=name, func=func):
#                 if line not in lines:
#                     lines.append(line)
#         return lines
#
#     def toggle_random(self):
#         """
#         Toggles class instance variable between random and not random.
#
#         Returns
#         -------
#         None
#         """
#
#         self.random = not self.random
#
#     def reset(self, chronological: bool=None, *, notes_key: str=None):
#         """
#         Resets the indexes of a certain notes list.
#
#         Parameters
#         ----------
#         chronological : bool, Optional
#             If this is not provided (left as None), it will reset both the random and chronological progress.
#             Otherwise, if it is True, it will reset chronological progress of the notes list.
#             If it is False, it will reset the random progress of the notes list.
#         notes_key : str, Optional
#             If this is not provided, it will default to whatever the current notes are.
#             Otherwise, it will use the key provided to find a corresponding notes list.
#
#         Returns
#         -------
#         None
#         """
#
#         if notes_key is None:
#             notes_key = self.current_notes
#
#         if chronological is None:
#             self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] = 0
#             self.all_indexes[notes_key + self.RANDOM_SUFFIX] = [
#                 x for x in range(len(self.all_lists[notes_key + self.LIST_SUFFIX]))]
#             random.shuffle(self.all_indexes[notes_key + self.RANDOM_SUFFIX])
#         else:
#             if chronological:
#                 self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] = 0
#             else:
#                 self.all_indexes[notes_key + self.RANDOM_SUFFIX] = [
#                     x for x in range(len(self.all_lists[notes_key + self.LIST_SUFFIX]))]
#                 random.shuffle(self.all_indexes[notes_key + self.RANDOM_SUFFIX])
#
#     def reset_all(self):
#         """
#         Resets all indexes except last_index to default. Empties the correct and incorrect lists.
#
#         Does not reset notes (use read_notes() for that).
#
#         Returns
#         -------
#         None
#         """
#
#         self.all_lists[self.KEY_CORRECT + self.LIST_SUFFIX] = []
#         self.all_lists[self.KEY_INCORRECT + self.LIST_SUFFIX] = []
#         for key in self.all_indexes.keys():
#             if key.endswith(self.CHRONOLOGICAL_SUFFIX):
#                 self.all_indexes[key] = 0
#             elif key.endswith(self.RANDOM_SUFFIX):
#                 try:
#                     self.all_indexes[key] = [
#                         x for x in range(len(self.all_lists[key[:-1 * len(self.RANDOM_SUFFIX)] + self.LIST_SUFFIX]))]
#                     random.shuffle(self.all_indexes[key])
#                 except KeyError:
#                     pass
#
#     def reset_chronological(self):
#         """
#         Resets only the chronological index (line_index) back to 0.
#
#         Returns
#         -------
#         None
#         """
#
#         for key in self.all_indexes.keys():
#             if key.endswith(self.CHRONOLOGICAL_SUFFIX):
#                 self.all_indexes[key] = 0
#
#     def reset_random(self):
#         """
#         Resets the list of indexes that have not been randomly retrieved from yet.
#
#         Returns
#         -------
#         None
#         """
#
#         for key in self.all_indexes:
#             if key.endswith(self.RANDOM_SUFFIX):
#                 try:
#                     self.all_indexes[key] = [
#                         x for x in range(len(self.all_lists[key[:-1 * len(self.RANDOM_SUFFIX)] + self.LIST_SUFFIX]))]
#                     random.shuffle(self.all_indexes[key])
#                 except KeyError:
#                     pass
#
#     def reset_correct(self):
#         """
#         Resets the list of correct lines.
#
#         Returns
#         -------
#         None
#         """
#
#         self.all_lists[self.KEY_CORRECT + self.LIST_SUFFIX] = []
#         self.all_indexes[self.KEY_CORRECT + self.CHRONOLOGICAL_SUFFIX] = 0
#         self.all_indexes[self.KEY_CORRECT + self.RANDOM_SUFFIX] = []
#
#     def reset_incorrect(self):
#         """
#         Resets the list of incorrect lines.
#
#         Returns
#         -------
#         None
#         """
#
#         self.all_lists[self.KEY_INCORRECT + self.LIST_SUFFIX] = []
#         self.all_indexes[self.KEY_INCORRECT + self.CHRONOLOGICAL_SUFFIX] = 0
#         self.all_indexes[self.KEY_INCORRECT + self.RANDOM_SUFFIX] = []
#
#
# class PairedQuiz(Quiz):
#     """
#     A quiz of paired notes with terms and definitions. Can ask for the term given the definition and vice versa.
#
#     Keys are used for to_dict().
#     Keys that are used for converting to a dictionary.
#         In all_indexes:
#             All keys are constructed from KEY_DICT + RANDOM or CHRONOLOGICAL suffix.
#             KEY_DICT_INDEX : str
#             KEY_DICT_INDEXES : str
#             KEY_CORRECT_PAIR_INDEX : str
#             KEY_CORRECT_PAIR_INDEXES : str
#             KEY_INCORRECT_PAIR_INDEXES : str
#             KEY_INCORRECT_PAIR_INDEXES : str
#
#         Dict keys:
#             KEY_NOTES_PAIRED : str
#             KEY_CORRECT_DICT : str
#             KEY_INCORRECT_DICT : str
#         KEY_TERM_FIRST : str
#
#     Attributes
#     ----------
#         delimeter : str
#             The character that separates terms from definitions.
#         all_indexes {str : int or list of int}:     # Additions to the previous all_indexes
#             dict_index : int
#                 Chronological index of the next pair of term and definitions.
#             dict_indexes : list of int
#                 Keep tracks of what pairs (terms and definitions) have been used.
#                 Used to make sure terms are not repeating.
#             correct_pair_index : int
#                 Chronological index of the next pair in the correct dict.
#             correct_pair_indexes : list of int
#                 Random indexes of the next pair in the correct dict.
#             incorrect_pair_index : int
#                 Chronological index of the next pair in the incorrect dict.
#             incorrect_pair_indexes : list of int
#                 Random indexes of the next pair in the incorrect dict.
#         all_dicts : dict {str: IndexedDict}
#             notes_dict : IndexedDict {str : str}
#                 All terms and definitions in a dictionary
#             correct_dict : IndexedDict {str: str}
#                 Subset of notes_dict that contains the user's correct terms and definitions.
#             incorrect_dict : IndexedDict {str: str}
#                 Subset of notes_dict that contains the user's incorrect terms and definitions.
#         term_first : bool
#             Whether to return the term first in the qa method.
#     """
#
#     DICT_SUFFIX = "_dict"
#
#     KEY_ALL_DICTS = "all_dicts"
#
#     KEY_TERM_FIRST = "term_first"
#
#     def __init__(self, noteutil):
#         """
#         Sets up empty variables for the Paired notes and quiz.
#
#         Parameters
#         ----------
#         noteutil : PairedNoteUtil
#             A PairedNoteUtil that has been initialized with notes.
#         """
#
#         super().__init__(noteutil)
#         self.current_notes = self.KEY_NOTES
#
#         self.all_indexes.update(
#             {self.KEY_NOTES + self.CHRONOLOGICAL_SUFFIX: 0,
#              self.KEY_NOTES + self.RANDOM_SUFFIX: [x for x in range(len(self.noteutil.notes_paired))],
#              self.KEY_CORRECT + self.CHRONOLOGICAL_SUFFIX: 0,
#              self.KEY_CORRECT + self.RANDOM_SUFFIX: [],
#              self.KEY_INCORRECT + self.CHRONOLOGICAL_SUFFIX: 0,
#              self.KEY_INCORRECT + self.RANDOM_SUFFIX: []})
#
#         random.shuffle(self.all_indexes[self.KEY_NOTES + self.RANDOM_SUFFIX])
#         self.delimeter = noteutil.delimeter
#         self.all_dicts = IndexedDict({self.KEY_NOTES + self.DICT_SUFFIX: self.noteutil.notes_paired,
#                                       self.KEY_CORRECT + self.DICT_SUFFIX: IndexedDict(),
#                                       self.KEY_INCORRECT + self.DICT_SUFFIX: IndexedDict()})
#
#         self.term_first = True
#
#     def __str__(self):
#         """
#         Converts all variables into strings.
#
#         Returns
#         -------
#         str
#             All variables with labels separated by newlines.
#         """
#
#         message = super().__str__() + "\n"
#         message += "PairedQuiz:\n"
#
#         message += "All dictionaries: \n"
#         for key in self.all_dicts.keys():
#             message += key + ": " + str(self.all_dicts[key]) + "\n"
#         message += "Delimeter: " + self.delimeter + "\n"
#         message += "Term first: " + str(self.term_first) + "\n"
#
#         return message
#
#     def to_dict(self):
#         """
#         Converts all changeable variables into a dictionary using key constants.
#
#         Will not convert any 'notes' because those can be remade from the notes files.
#
#         Returns
#         -------
#         dict
#             Dictionary of all variables {KEY_CONSTANT: variable}.
#         """
#
#         quiz = super().to_dict()
#
#         ignore_keys = [self.KEY_NOTES + self.DICT_SUFFIX]
#         filtered_dict = dict()
#         for k in self.all_dicts:
#             if k not in ignore_keys:
#                 filtered_dict[k] = self.all_dicts[k]
#         quiz[self.KEY_ALL_DICTS] = filtered_dict
#
#         quiz[self.KEY_TERM_FIRST] = self.term_first
#
#         return quiz
#
#     def parse_dict(self, var_dict: dict):
#         """
#         Sets all of this class' changeable variables by reading a dictionary.
#
#         Reads using the key constants the dictionary should have been created with.
#
#         Parameters
#         ----------
#         var_dict : dict
#             A dictionary created from PairedNoteUtil.to_dict() that has all of the key constants.
#
#         Returns
#         -------
#         None
#         """
#
#         super().parse_dict(var_dict)
#         self.all_dicts.update(var_dict[PairedQuiz.KEY_ALL_DICTS])
#         for k in self.all_dicts.keys():
#             self.all_dicts[k] = IndexedDict(self.all_dicts[k])
#         self.term_first = var_dict[PairedQuiz.KEY_TERM_FIRST]
#
#     def pair(self, notes_key: str=None):
#         """
#         Retrieves a pair (term and definition), moving chronologically or randomly.
#
#         Resets to the first (top) pair when all pairs have been retrieved.
#         Resets the dict indexes when all of them are used for random generation.
#
#         Parameters
#         ----------
#         notes_key : str
#             A key to a notes dict to take a pair from.
#
#         Returns
#         -------
#         str
#             The term of a pair that is either next chronologically or randomly chosen.
#         str
#             The definition of a pair that is either next chronologically or randomly chosen.
#         bool
#             Whether the chronological index or random index has repeated.
#         """
#
#         repeat = False
#         if notes_key is None:
#             notes_key = self.current_notes
#         notes_dict = self.all_dicts[notes_key + self.DICT_SUFFIX]
#         rand_list = self.all_indexes[notes_key + self.RANDOM_SUFFIX]
#         chrono_index = self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX]
#
#         if self.random:
#
#             if not rand_list:
#                 rand_list = self.all_indexes[notes_key + self.RANDOM_SUFFIX] = [x for x in range(len(notes_dict))]
#                 random.shuffle(self.all_indexes[notes_key + self.RANDOM_SUFFIX])
#
#             try:
#                 rand_index = rand_list.pop()
#             except IndexError:
#                 raise errors.NotesIndexError("The notes_dict provided is empty")
#
#             pair = self.noteutil.pair(notes_dict=notes_dict, index=rand_index)
#             self.all_indexes[self.KEY_LAST_INDEX] = self.noteutil.pair_index(term=pair[0])
#
#             if not rand_list:
#                 repeat = True
#
#         else:
#             if self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] >= len(notes_dict):
#                 chrono_index = self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] = 0
#
#             pair = self.noteutil.pair(notes_dict=notes_dict, index=chrono_index)
#             self.all_indexes[self.KEY_LAST_INDEX] = self.noteutil.pair_index(term=pair[0])
#
#             self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] += 1
#
#             if self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] == len(notes_dict):
#                 repeat = True
#
#         return pair[0], pair[1], repeat
#
#     def qa(self, notes_key: str=None):
#         """
#         Retrieves a pair and then formats the term and definition into a question-answer style.
#
#         The order of the term and definition are determined term_first.
#
#         Parameters
#         ----------
#         notes_key : str, optional - default is current_notes.
#             Key to a notes dict.
#
#         Returns
#         -------
#         str
#             Question asking either to define the term or guess the term.
#         str
#             Answer saying either the definition or what the term was.
#         bool
#             Whether the terms have cycled.
#         """
#
#         if notes_key is None:
#             notes_key = self.current_notes
#         term, definition, repeat = self.pair(notes_key)
#
#         if self.term_first:
#             question = "Define{0} {1}".format(self.delimeter, term)
#             answer = "The definition was{0} {1}".format(self.delimeter, definition)
#         else:
#             question = "Guess the term{0} {1}".format(self.delimeter, definition)
#             answer = "The term was{0} {1}".format(self.delimeter, term)
#         return question, answer, repeat
#
#     def add_pair(self, *, notes_key: str=None,
#                  last: bool=False, index: int=None, term: str=None, definition: str=None, func=lambda x: x.lower()):
#         """
#         Assigns a definition to a term in a notes dict.
#
#         Parameters
#         ----------
#         notes_key : str, optional - default is current_notes.
#             Key to a notes dict to add to.
#         last : bool, optional if one of the other three is provided.
#             Add the pair that corresponds to the last index used.
#         index : int, optional if one of the other three is provided.
#             Add the pair that corresponds to the provided index in notes paired.
#         term : str, optional if one of the other three is provided.
#             Part of or the entire term, must be unique to noteutil.notes_paired.
#         definition : str, optional if one of the other three is provided.
#             Part of or the entire definition, must be unique to noteutil.notes_paired.
#         func : function, Optional
#             Function to apply to the term and definition of parameter and dictionary, default is case insensitive.
#
#         Returns
#         -------
#         None
#
#         Raises
#         ------
#         ForbiddenEdit
#             If the notes_paired was attempted to be edited.
#         DuplicateError
#             If the term is already in the selected list.
#         NotesNotFoundError
#             If the no terms were found from the name.
#         MultipleFoundError
#             If more than 1 term was found from the name.
#         """
#
#         if notes_key is None:
#             notes_key = self.current_notes
#
#         if notes_key == self.KEY_NOTES:
#             raise errors.ForbiddenEdit
#
#         notes_dict = self.all_dicts[notes_key + self.DICT_SUFFIX]
#         rand_list = self.all_indexes[notes_key + self.RANDOM_SUFFIX]
#
#         if last:
#             last_index = self.all_indexes[self.KEY_LAST_INDEX]
#             exact_term, exact_definition = self.noteutil.pair(index=last_index)
#
#             if exact_term in notes_dict:
#                 raise errors.DuplicateError
#             else:
#                 notes_dict[exact_term] = exact_definition
#
#             rand_list.insert(random.randint(0, len(notes_dict)), len(notes_dict) - 1)
#             return
#
#         if index is not None:
#             exact_term, exact_definition = self.noteutil.pair(index=index)
#             if exact_term in notes_dict:
#                 raise errors.DuplicateError
#             else:
#                 notes_dict[exact_term] = exact_definition
#
#             rand_list.insert(random.randint(0, len(notes_dict)), len(notes_dict) - 1)
#             return
#
#         if term is not None:
#             try:
#                 exact_term = self.noteutil.term(term=term, func=func)
#                 if exact_term in notes_dict:
#                     raise errors.DuplicateError
#
#                 notes_dict[exact_term] = self.noteutil.definition(term=exact_term)
#                 rand_list.insert(random.randint(0, len(notes_dict)), len(notes_dict) - 1)
#                 return
#
#             except errors.NotesNotFoundError:
#                 pass    # Try again with terms
#
#             try:
#                 terms = self.noteutil.terms(term=term, func=func)
#                 if len(terms) == 1:     # Only throw error if there is no definition parameter (we can search that too)
#                     exact_term = terms[0]
#
#                     if exact_term in notes_dict:
#                         raise errors.DuplicateError
#                     else:
#                         notes_dict[exact_term] = self.noteutil.definition(term=exact_term)
#                         rand_list.insert(random.randint(0, len(notes_dict)), len(notes_dict) - 1)
#                         return
#                 else:
#                     raise errors.MultipleFoundError
#             except (errors.NotesNotFoundError, errors.MultipleFoundError):
#                 if definition is None:
#                     raise
#
#         if definition is not None:
#             try:
#                 exact_term = self.noteutil.term(definition=definition, func=func)
#                 if exact_term in notes_dict:
#                     raise errors.DuplicateError
#                 else:
#                     notes_dict[exact_term] = self.noteutil.definition(term=exact_term)
#                     rand_list.insert(random.randint(0, len(notes_dict)), len(notes_dict) - 1)
#                     return
#             except errors.NotesNotFoundError:
#                 pass
#
#             terms = self.noteutil.terms(definition=definition, func=func)
#             if len(terms) == 1:
#                 exact_term = terms[0]
#
#                 if exact_term in notes_dict:
#                     raise errors.DuplicateError
#                 else:
#                     notes_dict[exact_term] = self.noteutil.definition(term=exact_term)
#                     rand_list.insert(random.randint(0, len(notes_dict)), len(notes_dict) - 1)
#                     return
#             else:
#                 raise errors.MultipleFoundError
#
#     def remove_pair(self, *, notes_key: str=None,
#                     last: bool=False, index: int=None, term: str=None, definition: str=None, func=lambda x: x.lower()):
#         """
#         Adds a line of notes to the incorrect list.
#
#         Parameters
#         ----------
#         notes_key : str
#             Key to a notes dict to remove the pair from.
#         last : bool, optional if one of the other three is provided.
#             Remove the pair that corresponds to the last index used.
#         index : int, optional if one of the other three is provided.
#             Remove the pair that corresponds to the provided index.
#         term : str, optional if one of the other is provided.
#             The name of the term to remove.
#             If a term is not found, and a definition was provided, this will continue to the definition section.
#         definition : str, optional if one of the other is provided.
#             The definition of the term to remove.
#         func : function, Optional
#             Function to apply to the term and definition of parameter and dictionary, default is case insensitive.
#
#         Returns
#         -------
#         None
#
#         Raises
#         ------
#         ForbiddenEdit
#             If the notes_paired was attempted to be edited.
#         NotesNotFoundError
#             If the no lines were found from the name.
#             If the term was not in the dictionary to begin with.
#         MultipleFoundError
#             If more than 1 line was found from the name.
#         """
#
#         if notes_key is None:
#             notes_key = self.current_notes
#
#         if notes_key == self.KEY_NOTES:
#             raise errors.ForbiddenEdit
#
#         notes_dict = self.all_dicts[notes_key + self.DICT_SUFFIX]
#         rand_list = self.all_indexes[notes_key + self.RANDOM_SUFFIX]
#         chrono_index = self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX]
#
#         if last:
#             last_index = self.all_indexes[self.KEY_LAST_INDEX]
#             exact_term, exact_definition = self.noteutil.pair(index=last_index)
#
#             pair_index = self.noteutil.pair_index(notes_dict=notes_dict, term=exact_term)
#
#             if exact_term in notes_dict:
#
#                 if pair_index <= chrono_index:
#                     self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#                 for i in range(len(rand_list) - 1, -1, -1):
#                     if rand_list[i] > pair_index:
#                         rand_list[i] -= 1
#                     elif rand_list[i] == pair_index:
#                         del rand_list[i]
#
#                 del notes_dict[exact_term]
#             else:
#                 raise errors.NotesNotFoundError
#             return
#
#         if index is not None:
#             exact_term, exact_definition = self.noteutil.pair(index=index)
#             pair_index = self.noteutil.pair_index(notes_dict=notes_dict, term=exact_term)
#
#             if exact_term in notes_dict:
#                 if pair_index <= chrono_index:
#                     self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#                 for i in range(len(rand_list) - 1, -1, -1):
#                     if rand_list[i] > pair_index:
#                         rand_list[i] -= 1
#                     elif rand_list[i] == pair_index:
#                         del rand_list[i]
#
#                 del notes_dict[exact_term]
#             else:
#                 raise errors.NotesNotFoundError
#             return
#         if term is not None:
#
#             try:
#                 exact_term = self.noteutil.term(term=term, func=func)
#                 pair_index = self.noteutil.pair_index(notes_dict=notes_dict, term=exact_term)
#
#                 if exact_term not in notes_dict:
#                     raise errors.NotesNotFoundError
#
#                 if pair_index <= chrono_index:
#                     self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#
#                 for i in range(len(rand_list) - 1, -1, -1):
#                     if rand_list[i] > pair_index:
#                         rand_list[i] -= 1
#                     elif rand_list[i] == pair_index:
#                         del rand_list[i]
#
#                 del notes_dict[exact_term]
#                 return
#
#             except errors.NotesNotFoundError:  # Try again with the terms method.
#                 pass
#
#             try:
#                 terms = self.noteutil.terms(term=term, func=func)
#
#                 if len(terms) == 1:
#                     exact_term = terms[0]
#                     pair_index = self.noteutil.pair_index(term=exact_term)
#
#                     if exact_term not in notes_dict:
#                         raise errors.NotesNotFoundError
#
#                     if pair_index <= chrono_index:
#                         self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#                     del notes_dict[exact_term]
#                     return
#
#                 else:
#                     raise errors.MultipleFoundError
#             except (errors.MultipleFoundError, errors.NotesNotFoundError):
#                 if definition is None:
#                     raise
#
#         if definition is not None:
#
#             try:
#                 exact_term = self.noteutil.term(definition=definition, func=func)
#                 pair_index = self.noteutil.pair_index(notes_dict=notes_dict, term=exact_term)
#
#                 if exact_term not in notes_dict:
#                     raise errors.NotesNotFoundError
#
#                 if pair_index <= chrono_index:
#                     self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#
#                 for i in range(len(rand_list) - 1, -1, -1):
#                     if rand_list[i] > pair_index:
#                         rand_list[i] -= 1
#                     elif rand_list[i] == pair_index:
#                         del rand_list[i]
#
#                 del notes_dict[exact_term]
#                 return
#
#             except errors.NotesNotFoundError:  # Try again with the terms method.
#                 pass
#
#             terms = self.noteutil.terms(definition=definition, func=func)
#
#             if len(terms) == 1:
#                 exact_term = terms[0]
#                 pair_index = self.noteutil.pair_index(term=exact_term)
#
#                 if exact_term not in notes_dict:
#                     raise errors.NotesNotFoundError
#
#                 if pair_index <= chrono_index:
#                     self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] -= 1
#                 del notes_dict[exact_term]
#
#     def define_term(self, *, index: int=None, term: str=None, func=lambda x: x.lower()):
#         """
#         Defines a term at a specific index or with a certain name.
#
#         Checks the index first if both index and name are provided.
#
#         Parameters
#         ----------
#         index : int, optional if name is provided.
#             Index of a term in notes_paired.
#         term : str, optional if index is provided.
#             Name of key in notes_paired to be defined.
#         func : function, Optional
#             Function to apply to the term of parameter and dictionary, default is case insensitive.
#
#         Returns
#         -------
#         str
#             Definition of the term.
#
#         Raises
#         ------
#         NotesNotFoundError
#             If no values were associated with the index or term.
#         """
#
#         if index is not None:
#             return self.noteutil.definition(index=index)
#         if term is not None:
#             return self.noteutil.definition(term=term, func=func)
#
#     def define_terms(self, *, indexes: list=None, terms: list=None, func=lambda x: x.lower()):
#         """
#         Defines a list of terms from given indexes or term names.
#
#         Evaluates the indexes list first, and then the names list.
#
#         Parameters
#         ----------
#         indexes : list of int, optional if names is provided.
#             All indexes of terms to be defined.
#         terms : list of str, optional if indexes is provided.
#             All names of terms to be defined.
#         func : function, Optional
#             Function to apply to the term of parameter and dictionary, default is case insensitive.
#
#         Returns
#         -------
#         list of str
#             All definitions that corresponded to the indexes and names without repeating.
#
#         Raises
#         ------
#         NotesNotFoundError
#             If any of the values were not associated with the index or term.
#         """
#
#         definitions = []
#         if indexes is not None:
#             for index in indexes:
#                 definitions.append(self.define_term(index=index))
#         if terms is not None:
#             for term in terms:
#                 definition = self.define_term(term=term, func=func)
#                 if definition not in definitions:
#                     definitions.append(definition)
#         return definitions
#
#     def lookup_terms(self, *, indexes: list=None, name: str=None, definition: str=None, func=lambda x: x.lower()):
#         """
#         Gathers a list of terms from the given indexes, name, and/or definition.
#
#         Evaluates the indexes first, then name, and then definition.
#
#         Parameters
#         ----------
#         indexes : list of int
#             All indexes that correspond to a term.
#         name : str
#             A name that may appear in the terms' names.
#         definition : str
#             A definition that may correspond to terms.
#         func : function, Optional
#             Function to apply to the term and definition of parameter and dictionary, default is case insensitive.
#
#         Returns
#         -------
#         list of str
#             All terms that corresponded with the provided indexes, name, and/or definition.
#         """
#
#         terms = []
#         if indexes is not None:
#             for index in indexes:
#                 terms.append(self.noteutil.term(index=index))
#         if name is not None:
#             for term in self.noteutil.terms(term=name, definition=definition, func=func):
#                 if term not in terms:
#                     terms.append(term)
#         return terms
#
#     def toggle_term_first(self):
#         """
#         Toggles between returning the term first and the definition first.
#
#         Returns
#         -------
#
#         """
#
#         self.term_first = not self.term_first
#
#     def reset(self, chronological: bool=None, *, notes_key: str=None):
#         """
#         Resets the indexes of a certain notes dict.
#
#         Parameters
#         ----------
#         chronological : bool, Optional
#             If this is not provided (left as None), it will reset both the random and chronological progress.
#             Otherwise, if it is True, it will reset chronological progress of the notes dict.
#             If it is False, it will reset the random progress of the notes dict.
#         notes_key : str, Optional
#             If this is not provided, it will default to whatever the current notes are.
#             Otherwise, it will use the key provided to find a corresponding notes dict.
#
#         Returns
#         -------
#         None
#         """
#
#         if notes_key is None:
#             notes_key = self.current_notes
#
#         if chronological is None:
#             self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] = 0
#             self.all_indexes[notes_key + self.RANDOM_SUFFIX] = [
#                 x for x in range(len(self.all_dicts[notes_key + self.DICT_SUFFIX]))]
#             random.shuffle(self.all_indexes[notes_key + self.RANDOM_SUFFIX])
#         else:
#             if chronological:
#                 self.all_indexes[notes_key + self.CHRONOLOGICAL_SUFFIX] = 0
#             else:
#                 self.all_indexes[notes_key + self.RANDOM_SUFFIX] = [
#                     x for x in range(len(self.all_dicts[notes_key + self.DICT_SUFFIX]))]
#                 random.shuffle(self.all_indexes[notes_key + self.RANDOM_SUFFIX])
#
#     def reset_all(self):
#         """
#         Resets all indexes except last_index to default.
#
#         Does not reset notes (use make_notes() for that).
#
#         Returns
#         -------
#         None
#         """
#
#         super().reset_all()
#
#         self.all_dicts[self.KEY_CORRECT + self.DICT_SUFFIX] = IndexedDict()
#         self.all_dicts[self.KEY_INCORRECT + self.DICT_SUFFIX] = IndexedDict()
#
#         for key in self.all_indexes.keys():
#             if key.endswith(self.CHRONOLOGICAL_SUFFIX):
#                 self.all_indexes[key] = 0
#             elif key.endswith(self.RANDOM_SUFFIX):
#                 try:
#                     self.all_indexes[key] = [
#                         x for x in range(len(self.all_dicts[key[:-1 * len(self.RANDOM_SUFFIX)] + self.DICT_SUFFIX]))]
#                     random.shuffle(self.all_indexes[key])
#                 except KeyError:
#                     pass
#
#     def reset_random(self):
#         """
#         Resets the list of indexes that have not been randomly retrieved from yet.
#
#         Returns
#         -------
#         None
#         """
#
#         super().reset_random()
#         for key in self.all_indexes:
#             if key.endswith(self.RANDOM_SUFFIX):
#                 try:
#                     self.all_indexes[key] = [
#                         x for x in range(len(self.all_dicts[key[:-1 * len(self.RANDOM_SUFFIX)] + self.DICT_SUFFIX]))]
#                     random.shuffle(self.all_indexes[key])
#                 except KeyError:
#                     pass
#
#     def reset_correct(self):
#         """
#         Resets the list of correct lines.
#
#         Returns
#         -------
#         None
#         """
#
#         super().reset_correct()
#         self.all_dicts[self.KEY_CORRECT + self.DICT_SUFFIX] = IndexedDict()
#         self.all_indexes[self.KEY_CORRECT + self.CHRONOLOGICAL_SUFFIX] = 0
#         self.all_indexes[self.KEY_CORRECT + self.RANDOM_SUFFIX] = []
#
#     def reset_incorrect(self):
#         """
#         Resets the list of incorrect lines.
#
#         Returns
#         -------
#         None
#         """
#
#         super().reset_incorrect()
#         self.all_dicts[self.KEY_INCORRECT + self.DICT_SUFFIX] = IndexedDict()
#         self.all_indexes[self.KEY_INCORRECT + self.CHRONOLOGICAL_SUFFIX] = 0
#         self.all_indexes[self.KEY_INCORRECT + self.RANDOM_SUFFIX] = []
#
#
# class CategorizedQuiz(PairedQuiz):
#     """
#     A quiz with extended terms and definitions. It has been separated by "categories" for better organization.
#
#     All keys used will have the following and can be found in all_dicts:
#         n - name of the extension/category
#         DICT_SUFFIX - a suffix to indicate that it is a dict
#
#     A key is constructed from n + DICT_SUFFIX
#     """
#
#     def __init__(self, noteutil):
#         """
#         Creates all of the dictionary maps and indexes.
#
#         Parameters
#         ----------
#         noteutil : CategorizedNoteUtil
#             The CategorizedNoteUtil used to make the notes.
#         """
#
#         super().__init__(noteutil)
#
#         extensions = self.noteutil.extension_dict
#         generics = self.noteutil.generic_dict
#         categorized = self.noteutil.notes_categorized
#
#         if extensions:
#             for n, d in extensions.items():
#                 self.all_dicts[n + self.DICT_SUFFIX] = d
#                 self.all_indexes[n + self.CHRONOLOGICAL_SUFFIX] = 0
#                 self.all_indexes[n + self.RANDOM_SUFFIX] = [x for x in range(len(d))]
#                 random.shuffle(self.all_indexes[n + self.RANDOM_SUFFIX])
#
#         if generics:
#             for n, d in generics.items():
#                 self.all_dicts[n + self.DICT_SUFFIX] = d
#                 self.all_indexes[n + self.CHRONOLOGICAL_SUFFIX] = 0
#                 self.all_indexes[n + self.RANDOM_SUFFIX] = [x for x in range(len(d))]
#                 random.shuffle(self.all_indexes[n + self.RANDOM_SUFFIX])
#
#         if categorized:
#             for n, d in categorized.items():
#                 self.all_dicts[n + self.DICT_SUFFIX] = d
#                 self.all_indexes[n + self.CHRONOLOGICAL_SUFFIX] = 0
#                 self.all_indexes[n + self.RANDOM_SUFFIX] = [x for x in range(len(d))]
#                 random.shuffle(self.all_indexes[n + self.RANDOM_SUFFIX])
