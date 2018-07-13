import random
from note_utility.noteutil import IndexedDict


class Quiz:
    """
    Organizes questions through generation of lines from notes.

    With just a bare NoteUtil, there's not much to quiz besides just returning the lines.

    Keys are used for to_dict().
    Keys that are used for converting to a dictionary:
        KEY_LINE_INDEX : str
        KEY_LINE_INDEXES : str
        KEY_LAST_INDEX : str
        KEY_RANDOM : str
        KEY_LINES_CORRECT : str
        KEY_LINES_INCORRECT : str

    Attributes
    ----------
        line_index : int
            Index to the next line to pass chronologically.
        line_indexes : list of int
            Indexes to lines that have not been retrieved randomly yet.
        last_index : int
            Index to the previous line that was retrieved.
        random : bool
            Whether to return random lines or chronological ones.
        lines_correct : list of str
            Subset of notes that contain questions the user answered correctly.
        lines_incorrect : list of str
            Subset of notes that contain questions the user answered incorrectly.
    """

    KEY_LINE_INDEX = "line_index"
    KEY_LINE_INDEXES = "line_indexes"
    KEY_LAST_INDEX = "last_index"
    KEY_RANDOM = "random"
    KEY_LINES_CORRECT = "lines_correct"
    KEY_LINES_INCORRECT = "lines_incorrect"

    def __init__(self, noteutil):
        """
        Initialize all variables that relate to quizzing and notes.

        Parameters
        ----------
        noteutil : NoteUtil
            The note utility that was made from a file of notes.
        """

        # Relating to noteutil
        self.noteutil = noteutil
        self.line_index = 0
        self.line_indexes = random.shuffle([x for x in range(len(self.noteutil.notes_list))])
        self.last_index = 0

        # Relating to quiz
        self.random = False

        self.lines_correct = []
        self.lines_incorrect = []

    def __str__(self):
        """
        Converts all variables into strings and labels them.

        Returns
        -------
        str
            All variables as strings and separated by new lines.
        """

        message = "Quiz: \n"

        message += "Line index: " + str(self.line_index) + "\n"
        message += "Line indexes: " + str(self.line_indexes) + "\n"
        message += "Last index: " + str(self.last_index) + "\n"
        message += "Random: " + str(self.random) + "\n"
        message += "Lines correct: " + str(self.lines_correct) + "\n"
        message += "Lines incorrect: " + str(self.lines_incorrect) + "\n"

        return message

    def to_dict(self):
        """
        Converts all variables into a dictionary using key constants.

        Does not convert the noteutil.

        Returns
        -------
        dict
            Dictionary of all variables {KEY_CONSTANT: variable}.
        """

        quiz = dict()
        quiz[self.KEY_LINE_INDEX] = self.line_index
        quiz[self.KEY_LINE_INDEXES] = self.line_indexes
        quiz[self.KEY_LAST_INDEX] = self.last_index
        quiz[self.KEY_RANDOM] = self.random
        quiz[self.KEY_LINES_CORRECT] = self.lines_correct
        quiz[self.KEY_LINES_INCORRECT] = self.lines_incorrect

        return quiz

    @staticmethod
    def parse_dict(quiz, var_dict: dict):
        """
        Sets class variables by reading a dictionary.

        Reads using the key constants the dictionary should have been created with.

        Parameters
        ----------
        quiz : Quiz
            Any instance of a Quiz (since we will modify its variables).
        var_dict : dict
            Should be a dictionary created from to_dict().
            Contains all of the keys and values of a saved Quiz state.

        Returns
        -------
        None
        """

        quiz.line_index = var_dict[Quiz.KEY_LINE_INDEX]
        quiz.line_indexes = var_dict[Quiz.KEY_LINE_INDEXES]
        quiz.last_index = var_dict[Quiz.KEY_LAST_INDEX]
        quiz.random = var_dict[Quiz.KEY_RANDOM]
        quiz.lines_correct = var_dict[Quiz.KEY_LINES_CORRECT]
        quiz.lines_incorrect = var_dict[Quiz.KEY_LINES_INCORRECT]

    def get_line(self):
        """
        Retrieves a line of notes, moving chronologically or randomly.

        Resets to the first (top) line when all lines have been retrieved.
        Resets the random indexes when all indexes have been generated randomly.

        Parameters
        ----------
        rand : bool
            Whether to return a line from a random index or from chronological order.

        Returns
        -------
        str
            The next line in the notes list or a random line that hasn't been requested before.
        bool
            Whether the chronological index or random index has cycled.
        """

        repeat = False
        if self.random:
            rand_index = self.line_indexes.pop()
            if not self.line_indexes:
                self.line_indexes = random.shuffle([x for x in range(len(self.noteutil.notes_list))])
                repeat = True
            line = self.noteutil.notes_list[rand_index]
            self.last_index = rand_index

        else:
            line = self.noteutil.notes_list[self.line_index]
            self.line_index += 1
            if self.line_index == len(self.noteutil.notes_list):
                self.line_index = 0
                repeat = True
            self.last_index = self.line_index - 1

        return line, repeat

    def add_line_correct(self, *, last: bool=False, index: int=None, name: str=None, case_sensitive=False):
        """
        Adds a line of notes to the correct list.

        Parameters
        ----------
        last : bool, optional if one of the other two is provided.
            Add the line that corresponds to the last index used.
        index : int, optional if one of the other two is provided.
            Add the line that corresponds to the provided index.
        name : str, optional if one of the other two is provided.
            Part of or the entire line of notes, must be unique to that notes line. Add the line found.
        case_sensitive : bool, optional
            Whether case matters while searching with the name.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the provided name appears in multiple lines or no lines.
        """

        if last:
            self.lines_correct.append(self.noteutil.notes_list[self.last_index])
            return
        if index is not None:
            self.lines_correct.append(self.noteutil.line(index))
            return
        if name is not None:
            lines = self.noteutil.lines(name, case_sensitive)
            if len(lines) > 1 or len(lines) == 0:
                raise ValueError
            self.lines_correct.append(lines[0])

    def add_line_incorrect(self, *, last: bool=False, index: int=None, name: str=None, case_sensitive=False):
        """
        Adds a line of notes to the incorrect list.

        Parameters
        ----------
        last : bool, optional if one of the other two is provided.
            Add the line that corresponds to the last index used.
        index : int, optional if one of the other two is provided.
            Add the line that corresponds to the provided index.
        name : str, optional if one of the other two is provided.
            Part of or the entire line of notes, must be unique to that notes line. Add the line found.
        case_sensitive : bool, optional
            Whether case matters while searching with the name.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the provided name appears in multiple lines or no lines.
        """

        if last:
            self.lines_incorrect.append(self.noteutil.notes_list[self.last_index])
            return
        if index is not None:
            self.lines_incorrect.append(self.noteutil.line(index))
            return
        if name is not None:
            lines = self.noteutil.lines(name, case_sensitive)
            if len(lines) > 1:
                raise ValueError
            self.lines_incorrect.append(lines[0])

    def remove_line_correct(self, *, last: bool=False, index: int=None, name: str=None, case_sensitive=False):
        """
        Removes a line of notes from the correct list.

        Parameters
        ----------
        last : bool, optional if one of the other two is provided.
            Add the line that corresponds to the last index used.
        index : int, optional if one of the other two is provided.
            Add the line that corresponds to the provided index.
        name : str, optional if one of the other two is provided.
            Part of or the entire line of notes, must be unique to that notes line. Add the line found.
        case_sensitive : bool
            Whether case matters while searching with the name.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the line does not exist in the correct list.
            If the provided name appears in multiple lines or no lines.
        """

        if last:
            del self.lines_correct[self.lines_correct.index(self.noteutil.line(self.last_index))]
            return
        if index is not None:
            del self.lines_correct[self.lines_correct.index(self.noteutil.line(index))]
            return
        if name is not None:
            lines = self.noteutil.lines(name, case_sensitive)
            if len(lines) > 1:
                raise ValueError
            del self.lines_correct[self.lines_correct.index(lines[0])]

    def remove_line_incorrect(self, *, last: bool=False, index: int=None, name: str=None, case_sensitive=False):
        """
        Removes a line of notes from the incorrect list.

        Parameters
        ----------
        last : bool, optional if one of the other two is provided.
            Add the line that corresponds to the last index used.
        index : int, optional if one of the other two is provided.
            Add the line that corresponds to the provided index.
        name : str, optional if one of the other two is provided.
            Part of or the entire line of notes, must be unique to that notes line. Add the line found.
        case_sensitive : bool
            Whether case matters while searching with the name.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the line does not exist in the correct list.
            If the provided name appears in multiple lines or no lines.
        """

        if last:
            del self.lines_incorrect[self.lines_incorrect.index(self.noteutil.line(self.last_index))]
            return
        if index is not None:
            del self.lines_incorrect[self.lines_incorrect.index(self.noteutil.line(index))]
            return
        if name is not None:
            lines = self.noteutil.lines(name, case_sensitive)
            if len(lines) > 1:
                raise ValueError
            del self.lines_incorrect[self.lines_incorrect.index(lines[0])]

    def lookup_lines(self, *, indexes: list=None, name: str=None, case_sensitive=False):
        """
        Searches through all lines of notes and adds them to a list.

        Parameters
        ----------
        indexes : list of int
            Specific indexes in the noteutil notes_list to add.
        name : str
            A string that occurs in lines of notes. Any line that has this name in it will be added.
        case_sensitive : bool
            Whether case matters while searching with the name.

        Returns
        -------
        list of str
            The list of lines that includes either the line of the index or all lines that matched with the name.
        """
        lines = []
        if indexes is not None:
            for index in indexes:
                lines.append(self.noteutil.line(index))
        if name is not None:
            lines.extend(self.noteutil.lines(name, case_sensitive))
        return lines

    def toggle_random(self):
        """
        Toggles class instance variable between random and not random.

        Returns
        -------
        None
        """
        self.random = not self.random

    def reset_all(self):
        """
        Resets all indexes except last_index to default. Empties the correct and incorrect lists.

        Does not reset notes (use make_notes() for that).

        Returns
        -------
        None
        """

        self.line_index = 0
        self.line_indexes = random.shuffle([x for x in range(len(self.noteutil.notes_list))])
        self.lines_correct = []
        self.lines_incorrect = []

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

        self.line_indexes = random.shuffle([x for x in range(len(self.noteutil.notes_list))])

    def reset_correct(self):
        """
        Resets the list of correct lines.

        Returns
        -------
        None
        """

        self.lines_correct = []

    def reset_incorrect(self):
        """
        Resets the list of incorrect lines.

        Returns
        -------
        None
        """

        self.lines_incorrect = []


class PairedQuiz(Quiz):
    """


    Keys are used for to_dict().
    Keys that are used for converting to a dictionary.
        KEY_DICT_INDEX : str
        KEY_DICT_INDEXES : str

    Attributes
    ----------
        delimeter : str
            The character that separates terms from definitions.
        pair_index : int
            Chronological index of the next pair of term and definitions.
        pair_indexes : list of int
            Keep tracks of what pairs (terms and definitions) have been used.
            Used to make sure terms are not repeating.
    """

    KEY_DICT_INDEX = "dict_index"
    KEY_DICT_INDEXES = "dict_indexes"
    KEY_TERM_FIRST = "term_first"

    def __init__(self, noteutil):
        super().__init__(noteutil)
        self.pair_index = 0
        self.pair_indexes = random.shuffle([x for x in range(len(self.noteutil.notes_paired))])
        self.delimeter = noteutil.delimeter

        self.term_first = True
        self.pairs_correct = IndexedDict()
        self.pairs_incorrect = IndexedDict()

    def __str__(self):
        """
        Converts all variables into strings.

        Returns
        -------
        str
            All variables with labels separated by newlines.
        """

        message = super().__str__() + "\n"
        message += "PairedQuiz:\n"

        message += "Delimeter: " + self.delimeter + "\n"
        message += "Pair index: " + str(self.pair_index) + "\n"
        message += "Pair indexes: " + str(self.pair_indexes) + "\n"

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
    def parse_dict(quiz, var_dict: dict):
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

        super().parse_dict(quiz, var_dict)
        quiz.pair_index = var_dict[PairedQuiz.KEY_DICT_INDEX]
        quiz.pair_indexes = var_dict[PairedQuiz.KEY_DICT_INDEXES]

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
        """

        repeat = False
        if rand:
            rand_index = self.pair_indexes.pop()
            if not self.pair_indexes:
                self.pair_indexes = random.shuffle([x for x in range(len(self.noteutil.notes_paired))])
                repeat = True
            self.last_index = rand_index
            pair = self.noteutil.pair(rand_index)
        else:
            pair = self.noteutil.pair(self.pair_index)
            self.last_index = self.pair_index
            self.pair_index += 1
            if self.pair_index == len(self.noteutil.notes_paired):
                self.pair_index = 0
                repeat = True
        return pair[0], pair[1], repeat

    def add_term_correct(self, *, last: bool = False, index: int = None, name: str=None, case_sensitive=False):
        """
        Adds a line of notes to the correct list.

        Parameters
        ----------
        last : bool, optional if one of the other two is provided.
            Add the pair that corresponds to the last index used.
        index : int, optional if one of the other two is provided.
            Add the pair that corresponds to the provided index.
        name : str, optional if one of the other two is provided.
            Part of or the entire term, must be unique to noteutil.notes_paired. Add the term with this name.
        case_sensitive : bool, optional
            Whether case matters while searching with the name.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the provided name appears in multiple lines or no lines.
        """

        if last:
            term, definition = self.noteutil.pair(self.last_index)
            self.pairs_correct[term] = definition
            return
        if index is not None:
            term, definition = self.noteutil.pair(index)
            self.pairs_correct[term] = definition
            return
        if name is not None:
            try:
                term = self.noteutil.term(name=name, case_sensitive=case_sensitive)
                self.pairs_correct[term] = self.noteutil.definition(term=term)
            except KeyError:
                terms = self.noteutil.terms(name=name, case_sensitive=case_sensitive)
                if len(terms) == 0:
                    raise KeyError("Name not found in correct terms")
                if len(terms) > 1:
                    raise KeyError("More than one term found for the name")
                self.pairs_correct[terms[0]] = self.noteutil.definition(terms[0])

    def add_line_incorrect(self, *, last: bool = False, index: int = None, name: str = None, case_sensitive=False):
        """
        Adds a line of notes to the incorrect list.

        Parameters
        ----------
        last : bool, optional if one of the other two is provided.
            Add the pair that corresponds to the last index used.
        index : int, optional if one of the other two is provided.
            Add the pair that corresponds to the provided index.
        name : str, optional if one of the other two is provided.
            Part of or the entire term, must be unique to noteutil.notes_paired. Add the term with this name.
        case_sensitive : bool, optional
            Whether case matters while searching with the name.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the provided name appears in multiple lines or no lines.
        """

        if last:
            term, definition = self.noteutil.pair(self.last_index)
            self.pairs_incorrect[term] = definition
            return
        if index is not None:
            term, definition = self.noteutil.pair(index)
            self.pairs_incorrect[term] = definition
            return
        if name is not None:
            try:
                term = self.noteutil.term(name=name, case_sensitive=case_sensitive)
                self.pairs_incorrect[term] = self.noteutil.definition(term=term)
            except KeyError:
                terms = self.noteutil.terms(name=name, case_sensitive=case_sensitive)
                if len(terms) == 0:
                    raise KeyError("Name not found in incorrect terms")
                if len(terms) > 1:
                    raise KeyError("More than one term found for the name")
                self.pairs_incorrect[terms[0]] = self.noteutil.definition(terms[0])

    def remove_line_correct(self, *, last: bool = False, index: int = None, name: str = None, case_sensitive=False):
        """
        Adds a line of notes to the incorrect list.

        Parameters
        ----------
        last : bool, optional if one of the other two is provided.
            Remove the pair that corresponds to the last index used.
        index : int, optional if one of the other two is provided.
            Remove the pair that corresponds to the provided index.
        name : str, optional if one of the other two is provided.
            Part of or the entire term, must be unique to noteutil.notes_paired. Remove the term with this name.
        case_sensitive : bool, optional
            Whether case matters while searching with the name.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the provided name appears in multiple lines or no lines.
        """

        if last:
            term, definition = self.noteutil.pair(self.last_index)
            self.pairs_correct.pop(term)
            return
        if index is not None:
            term, definition = self.noteutil.pair(index)
            self.pairs_correct.pop(term)
            return
        if name is not None:
            try:
                term = self.noteutil.term(name=name, case_sensitive=case_sensitive)
                self.pairs_correct.pop(term)
            except KeyError:
                terms = self.noteutil.terms(name=name, case_sensitive=case_sensitive)
                if len(terms) == 0:
                    raise KeyError("Name not found in correct terms")
                if len(terms) > 1:
                    raise KeyError("More than one term found for the name")
                self.pairs_correct.pop(terms[0])

    def remove_line_incorrect(self, *, last: bool = False, index: int = None, name: str = None, case_sensitive=False):
        """
        Adds a line of notes to the incorrect list.

        Parameters
        ----------
        last : bool, optional if one of the other two is provided.
            Remove the pair that corresponds to the last index used.
        index : int, optional if one of the other two is provided.
            Remove the pair that corresponds to the provided index.
        name : str, optional if one of the other two is provided.
            Part of or the entire term, must be unique to noteutil.notes_paired. Remove the term with this name.
        case_sensitive : bool, optional
            Whether case matters while searching with the name.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the provided name appears in multiple lines or no lines.
        """

        if last:
            term, definition = self.noteutil.pair(self.last_index)
            self.pairs_incorrect.pop(term)
            return
        if index is not None:
            term, definition = self.noteutil.pair(index)
            self.pairs_incorrect.pop(term)
            return
        if name is not None:
            try:
                term = self.noteutil.term(name=name, case_sensitive=case_sensitive)
                self.pairs_incorrect.pop(term)
            except KeyError:
                terms = self.noteutil.terms(name=name, case_sensitive=case_sensitive)
                if len(terms) == 0:
                    raise KeyError("Name not found in incorrect terms")
                if len(terms) > 1:
                    raise KeyError("More than one term found for the name")
                self.pairs_incorrect.pop(terms[0])

    def define_term(self, *, index: int=None, name: str=None):
        """
        Defines a term at a specific index or with a certain name.

        Checks the index first if both index and name are provided.

        Parameters
        ----------
        index : int, optional if name is provided.
            Index of a term in notes_paired.
        name : str, optional if index is provided.
            Name of key in notes_paired to be defined.

        Returns
        -------
        str
            Definition of the term.

        Raises
        ------
        ValueError
            If no values were associated with the index or term.

        """

        if index is not None:
            return self.noteutil.definition(index=index)
        if name is not None:
            return self.noteutil.definition(term=name)

    def define_terms(self, *, indexes: list=None, names: list=None):
        """
        Defines a list of terms from given indexes or term names.

        Evaluates the indexes list first, and then the names list.

        Parameters
        ----------
        indexes : list of int, optional if names is provided.
            All indexes of terms to be defined.
        names : list of str, optional if indexes is provided.
            All names of terms to be defined.

        Returns
        -------
        list of str
            All definitions that corresponded to the indexes and names without repeating.
        """

        definitions = []
        if indexes is not None:
            for index in indexes:
                definitions.append(self.noteutil.definition(index=index))
        if names is not None:
            for term in names:
                definition = self.noteutil.definition(term=term)
                if definition not in definitions:
                    definitions.append(definition)
        return definitions

    def lookup_terms(self, *, indexes: list=None, name=None, definition=None):
        """
        Gathers a list of terms from the given indexes, name, and/or definition.

        Evaluates the indexes first, then name, and then definition.

        Parameters
        ----------
        indexes : list of int
            All indexes that correspond to a term.
        name : str
            A name that may appear in the terms' names.
        definition : str
            A definition that may correspond to terms.

        Returns
        -------
        list of str
            All terms that corresponded with the provided indexes, name, and/or definition.
        """

        terms = []
        if indexes is not None:
            for index in indexes:
                terms.append(self.noteutil.term(index=index))
        if name is not None:
            for term in self.noteutil.terms(term=name):
                if term not in terms:
                    terms.append(term)
        if definition is not None:
            for term in self.noteutil.terms(definition=definition):
                if term not in terms:
                    terms.append(term)
        return terms

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
        self.pair_indexes = random.shuffle([x for x in range(len(self.noteutil.notes_paired))])
        self.pairs_correct = IndexedDict()
        self.pairs_incorrect = IndexedDict()

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
        self.pair_indexes = random.shuffle([x for x in range(len(self.noteutil.notes_paired))])

    def reset_correct(self):
        """
        Resets the list of correct lines.

        Returns
        -------
        None
        """
        super().reset_correct()
        self.pairs_correct = IndexedDict()

    def reset_incorrect(self):
        """
        Resets the list of incorrect lines.

        Returns
        -------
        None
        """
        super().reset_incorrect()
        self.pairs_incorrect = IndexedDict()


class CategorizedQuiz(PairedQuiz):
    pass



