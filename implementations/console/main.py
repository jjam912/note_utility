from noteutil import NoteUtil, Quiz, Leitner
from noteutil.notes import Note
from noteutil.comparisons import CompareOptions
from noteutil.errors import NoteError, TimeTooShort, LastBox
import os
from typing import List
from itertools import filterfalse


os.chdir(os.path.join(os.getcwd(), "notes"))
# Construct and add your NoteUtils here::
math = NoteUtil("heading_config.txt")
euro = NoteUtil("euro_config.txt")
calc = NoteUtil("calc_config.txt")
noteutils = [math, euro, calc]
#

CANCEL = ["exit", "quit", "stop"]


def text_input(message: str):
    """Takes input for any string as long as it is not one of the CANCEL words.

    Parameters
    ----------
    message : str
        The prompt to be accompanied with the input.

    Returns
    -------
    str or None
    """

    input_ = input(message + "\n\tType 'exit', 'quit' or 'stop' to leave the current action.\n")

    if input_.lower() in CANCEL:
        return None
    return input_


def range_input(message: str, range_: range):
    """Takes only an input that is an integer in a certain range.

    Parameters
    ----------
    message : str
        The prompt to be accompanied with the input.
    range_ : range
        A Python range that the integer input must be in.

    Returns
    -------
    int or None
    """

    while True:
        input_ = text_input(message)
        if input_ is None:
            return None

        try:
            input_ = int(input_)
            if input_ in range_:
                return input_
            else:
                print("Try again, number was not in the range.")
        except ValueError:
            print("Try again, input was not a number.")


def yn_input(message: str):
    while True:
        input_ = text_input(message + " (Y/N)")
        if input_ is None:
            return None

        if input_.lower() == "y":
            return True
        if input_.lower() == "n":
            return False
        print("Try again, input was not 'y' or 'n'.")


class Notebook:
    def __init__(self, noteutil: NoteUtil):
        self.noteutil = noteutil
        self.quiz = Quiz(noteutil)
        self.quiz.load()
        self.leitner = Leitner(noteutil)
        self.leitner.load()

        # Settings
        self.noteutil_settings = NoteUtilSettings(self)
        self.study_settings = StudySettings(self)


class NoteUtilSettings:
    def __init__(self, notebook: Notebook):
        self.notebook = notebook
        self.file = notebook.noteutil.note_file
        self.simple_search = True
        self.ask_define = True


class StudySettings:
    def __init__(self, notebook: Notebook):
        self.notebook = notebook
        self.qz_file = notebook.quiz.qz_file
        self.lt_file = notebook.leitner.lt_file
        self.term_format1 = "\nDefine the term: {0}"
        self.definition_format2 = "The definition is: {1}\n" \
                                  "Note Index: {3}"

        self.definition_format1 = "\nGuess the term: {1}"
        self.term_format2 = "The term is: {0}\n" \
                            "Note Index: {3}"

        self.random = True
        self.term_first = True
        self.include_extensions = True
        self.extension_format = {}
        self.extension_first = {}
        for ext_name in notebook.noteutil.extension_names:
            self.extension_format[ext_name] = "\n{0}: {1}"
            self.extension_first[ext_name] = False

    @property
    def heading(self):
        heading = self.notebook.quiz.division
        if heading is None:
            return "none"
        elif isinstance(heading, str):
            return heading
        elif isinstance(heading, Note):
            return heading.heading_name
        return "Error"
    

class Commands:
    def __init__(self, noteutils: List[NoteUtil]):
        self.notebooks = {}
        for nu in noteutils:
            self.notebooks[nu.note_file] = Notebook(nu)
        self.current_notebook = None
        self.commands = {
            "commands":     self.display,
            "select":       self.select,

            "noteutil":                     self.noteutil,
            "noteutil settings":            self.noteutil_settings,
            "noteutil settings search":     self.noteutil_settings_search,
            "noteutil settings define":     self.noteutil_settings_define,
            "noteutil headings":            self.noteutil_headings,
            "noteutil categories":          self.noteutil_categories,
            "noteutil extensions":          self.noteutil_extensions,
            "noteutil search":              self.noteutil_search,
            "noteutil edit":                self.noteutil_edit,

            "study":                         self.study,
            "study settings":                self.study_settings,
            "study settings format":         self.study_settings_format,
            "study settings order":          self.study_settings_order,
            "study settings random":         self.study_settings_random,
            "study settings extensions":     self.study_settings_extensions,

            "quiz":                         self.quiz,
            "quiz division":                self.quiz_division,
            "quiz generate":                self.quiz_generate,
            "quiz correct":                 self.quiz_correct,
            "quiz incorrect":               self.quiz_incorrect,
            "quiz unmarked":                self.quiz_unmarked,
            "quiz clear":                   self.quiz_clear,
            "quiz save":                    self.quiz_save,
            "quiz load":                    self.quiz_load,

            "leitner":                      self.leitner,
            "leitner settings":             self.leitner_settings,
            "leitner boxes":                self.leitner_boxes,
            "leitner notes":                self.leitner_notes,
            "leitner generate":             self.leitner_generate,
            "leitner reset":                self.leitner_reset,
            "leitner save":                 self.leitner_save,
            "leitner load":                 self.leitner_load
        }

    @staticmethod
    def display():
        print(
            """Here are the commands:
            
        commands    : Shows this.
        select      : Select a note file to use.
        noteutil    : Shows commands for NoteUtil.
        study       : Shows commands for Study Settings
        quiz        : Shows commands for Quiz.
        leitner     : Shows commands for Leitner.
        """)

    def select(self):
        print("Please choose one of the following note files:")
        for i, note_file in enumerate(self.notebooks.keys()):
            print("\t{0}. {1}".format(i + 1, note_file))
        i_nu = range_input("Select the number corresponding to the note file you want to use.",
                           range(1, len(self.notebooks) + 1))
        if i_nu is None:
            return print("Canceled input. (1)")

        note_file = list(self.notebooks.keys())[i_nu - 1]
        self.current_notebook = self.notebooks[note_file]

    def noteutil(self):
        print(
            """Here are the NoteUtil commands:

        noteutil    : Shows this.
        
        NoteUtil Settings
            noteutil settings   : Displays your NoteUtil settings.
            noteutil settings search    : Toggles between simple and advanced search.
            noteutil settings define    : Toggles between asking to define in depth and not
        NoteUtil
            noteutil headings       : Shows heading order and names.
            noteutil categories     : Shows category names and prefixes.
            noteutil extensions     : Shows extension names and bounds.
            noteutil search         : Search for a Note.
            noteutil edit           : Edit the content of a Note.
        """)

    def noteutil_settings(self):
        settings = self.current_notebook.noteutil_settings
        print("Noteutil Settings:")
        print("\tSimple Search: " + str(settings.simple_search))
        print("\tAsk Define: " + str(settings.ask_define))

    def noteutil_settings_search(self):
        settings = self.current_notebook.noteutil_settings
        settings.simple_search = not settings.simple_search
        print("Simple Search set to: " + str(settings.simple_search))

    def noteutil_settings_define(self):
        settings = self.current_notebook.noteutil_settings
        settings.ask_define = not settings.ask_define
        print("Ask Define set to: " + str(settings.ask_define))

    def noteutil_headings(self):
        noteutil = self.current_notebook.noteutil

        heading_description = ""
        heading_description += "Heading Levels:" + "\n"

        level = 1
        for gname, anames in noteutil.level_order.items():  # General name, Actual names
            heading_description += "\tLevel " + str(level) + ". " + gname + ":" + "\n"
            for aname in anames:
                heading_description += "\t\t" + aname.heading_name + "\n"
            level += 1

        heading_description += "Heading Order:" + "\n"
        for note in noteutil.heading_order:
            for _ in range(note.level):
                heading_description += "\t"
            heading_description += note.heading_name + "\n"
        print(heading_description)

    def noteutil_categories(self):
        noteutil = self.current_notebook.noteutil
        print("Categories:")

        for name, prefix in zip(noteutil.category_names, noteutil.category_prefixes):
            print("\t" + name + ": " + prefix)

    def noteutil_extensions(self):
        noteutil = self.current_notebook.noteutil

        print("Extensions:")
        for name, bounds in zip(noteutil.extension_names, noteutil.extension_bounds):
            print("\t" + name)
            print("\t\tLeft bound:  " + bounds[0])
            print("\t\tRight bound: " + bounds[1])

    def noteutil_search(self):
        noteutil = self.current_notebook.noteutil
        settings = self.current_notebook.noteutil_settings

        if settings.simple_search:
            query = text_input("Enter the part of the Note you are searching for.")
            if query is None:
                return print("Canceled input. (1)")

            note_list = noteutil.get_list(content=query, compare=CompareOptions.SIN)
            if not note_list:
                return print("No Notes found. (1)")

        else:
            search_type = range_input("How do you want to search?"
                                      "\n\t1. Content"
                                      "\n\t2. Note index"
                                      "\n\t3. Term"
                                      "\n\t4. Definition"
                                      "\n\t5. Heading level"
                                      "\n\t6. Heading name"
                                      "\n\t7. Extension name", range(8))
            search_conversion = {1: "content", 2: "nindex", 3: "term", 4: "definition",
                                 5: "level", 6: "heading_name", 7: "extension_names"}

            if search_type is None:
                return print("Canceled input. (1)")
            if search_type in [0]:
                kwargs = text_input("You've found the hidden eval search option!\n"
                                    "Complete the code: noteutil.get_list(<...>)")
                if kwargs is None:
                    return print("Canceled input. (0)")
                note_list = eval("noteutil.get_list(" + kwargs + ")")
            elif search_type in [1, 3, 4, 6]:
                compare_type = range_input("How do you want to compare?"
                                           "\n\t1. Equals"
                                           "\n\t2. Similarity"
                                           "\n\t3. In"
                                           "\n\t4. Similar & In", range(1, 5))
                compare_conversion = {1: CompareOptions.EQUALS, 2: CompareOptions.SIMILAR,
                                      3: CompareOptions.IN, 4: CompareOptions.SIN}
                if compare_type is None:
                    return print("Canceled input. (2)")

                query = text_input("Enter the part of the Note you are searching for.")
                if query is None:
                    return print("Canceled input. (3)")

                note_list = noteutil.get_list(**{search_conversion[search_type]: query,
                                                 "compare": compare_conversion[compare_type]})
                if not note_list:
                    return print("No Notes found. (2)")

            elif search_type in [2, 5]:
                if search_type == 2:
                    specific = yn_input("Would you like a specific index (Y) or a range of Notes (N)?")
                    if specific is None:
                        return print("Canceled input. (4)")
                    if specific:
                        query = range_input("Enter the note index of the Note.", range(len(noteutil.notes)))
                        if query is None:
                            return print("Canceled input. (5)")

                        note_list = noteutil.get_list(**{search_conversion[search_type]: query})
                    else:
                        begin = range_input("Enter the note index of the beginning Note.", range(len(noteutil.notes)))
                        if begin is None:
                            return print("Canceled input. (5)")

                        end = range_input("Enter the note index of the ending Note. "
                                          "It must be greater than the beginning Note",
                                          range(begin + 1, len(noteutil.notes) + 1))
                        if end is None:
                            return print("Canceled input. (6)")

                        note_list = []
                        for nindex in range(begin, end):
                            note_list.append(noteutil.notes[nindex])

                    if not note_list:
                        return print("No Notes found. (3)")
                else:
                    query = range_input("Enter the level of the Heading.", range(1, noteutil.levels + 1))
                    note_list = noteutil.get_list(**{search_conversion[search_type]: query})
                    if not note_list:
                        return print("No Notes found. (4)")

            elif search_type in [7]:
                query = text_input("Enter the Extension name and make sure it matches exactly.")
                if query is None:
                    return print("Canceled input. (7)")

                note_list = noteutil.get_list(**{search_conversion[search_type]: query, "compare": CompareOptions.IN})
                if not note_list:
                    return print("No Notes found. (5)")
            else:
                return print("Error: Search type not in range.")

        for i, note in enumerate(note_list):
            print("\t{0}. {1}".format(i + 1, note.content))

        if settings.ask_define:
            define = yn_input("Would you like to look at a specific Note more in depth?")
            if define is None or define is False:
                return print("Canceled input. (8)")

            if len(note_list) > 1:
                nindex = range_input("Choose the number of a Note from the Note list", range(1, len(note_list) + 1))
                if nindex is None:
                    return print("Canceled input. (9)")
            else:
                nindex = 1
            note = note_list[nindex - 1]
            print("Content: {0}\n"
                  "RContent: {1}\n"
                  "Note Index: {2}\n"
                  "Term: {3}\n"
                  "Definition: {4}\n"
                  "Heading level: {5}\n"
                  "Heading name: {6}\n"
                  "Note Range: {7}\n"
                  "Extensions: {8}".format(note.content, note.rcontent, note.nindex, note.term, note.definition,
                                           note.level, note.heading_name,
                                           "range(" + str(note.begin_nindex) + ", " + str(note.end_nindex) + ")",
                                           "\n\t".join(list(map(lambda e: e.name + ":" + e.content, note.extensions)))))

    def noteutil_edit(self):
        noteutil = self.current_notebook.noteutil

        nindex = range_input("Enter the note index of the Note.", range(len(noteutil.notes)))
        if nindex is None:
            return print("Canceled input. (1)")
        note = noteutil.notes[nindex]
        print("The current content of this note is:")
        print("\t" + note.content)
        confirm = yn_input("Are you sure you want to edit this Note?"
                           "\n\tEditing a Note's content can have several side effects, including:"
                           "\n\t1. Changes to Heading name."
                           "\n\t2. Changes to Extensions."
                           "\n\t3. Changes to whether the Note is a pair."
                           "\n\t4. Changes to term, definition, and separator.")
        if confirm is None or confirm is False:
            return print("Canceled input. (2)")

        confirm = False
        while not confirm:
            content = text_input("Enter the new content of the Note.")
            if content is None:
                return print("Canceled input. (3)")
            confirm = yn_input("The content of your Note is:"
                               "\n\t{0}"
                               "\nIs this your intended content?".format(content))
            if confirm is None:
                return print("Canceled input. (4)")

        try:
            noteutil.edit(note, content)
        except NoteError as e:
            confirm = yn_input("There was a warning associated with the content you assigned:"
                               "\n\t{0}"
                               "\nDo you want to override this warning?".format(e.args))
            if confirm is None or confirm is False:
                return print("Canceled input. (5)")

        noteutil.edit(note, content, True)
        confirm = yn_input("Would you like to save these changes in your .nu file?")
        if confirm is None or confirm is False:
            return print("Canceled input. (6)")
        noteutil.reformat()

    def study(self):
        print(
            """Here are the Quiz commands:

        study    : Shows this.
        
        Study Settings
            study settings               : Displays your Quiz settings.
            study settings format        : Sets up how term and definition should be formatted.
            study settings order         : Toggles between term and definition being said first.
            study settings random        : Toggles between chronological and random Note generation.
            study settings heading       : Selects the heading that the Quiz should generate Notes from.
            study settings extensions    : Sets up how extensions should be handled.

        """)

    def study_settings(self):
        settings = self.current_notebook.study_settings
        print("Quiz Settings:")
        print("\tHeading: " + settings.heading)
        print("\tTerm Format 1: " + repr(settings.term_format1))
        print("\tDefinition Format 2: " + repr(settings.definition_format2))
        print("\tDefinition Format 1: " + repr(settings.definition_format1))
        print("\tTerm Format 2: " + repr(settings.term_format2))
        print("\tRandom: " + str(settings.random))
        print("\tTerm First: " + str(settings.term_first))
        print("\tInclude Extensions: " + str(settings.include_extensions))
        print("\tExtension Format: " + repr(settings.extension_format))
        print("\tExtension Term First: " + repr(settings.extension_first))

    def study_settings_format(self):
        print("""
        The difference between formats 1 and 2 depends on whether Term First is True.
            1 means that the prompt for either the term or the definition is first. 
            2 means that the answer for either the term or the definition is second.
        When Term First is True, Term Format 1 and Definition Format 2 are used.
            This is because the term is asked first and then the definition is revealed second.
        When Term First is False, Definition Format 1 and Term Format 2 are used.
            This is because the definition is asked first and then the term is revealed second.
            
        """)

        settings = self.current_notebook.study_settings
        edit_tf1 = yn_input("Do you want to edit Term Format 1?\n"
                            "The current format is: " + repr(settings.term_format1))
        if edit_tf1 is None:
            return print("Canceled input. (1)")
        if edit_tf1:
            new_format = text_input(r"Use {0} for term, {1} for definition, {2} for separator, {3} for note index, "
                                    r"\n for newline, and \t for tab")
            if new_format is None:
                print("Canceled input. (2)")
            else:
                new_format = new_format.replace("\\n", "\n")
                new_format = new_format.replace("\\t", "\t")
                settings.term_format1 = new_format

        edit_df2 = yn_input("Do you want to edit Definition Format 2?\n"
                            "The current format is " + repr(settings.definition_format2))
        if edit_df2 is None:
            return print("Canceled input. (3)")
        if edit_df2:
            new_format = text_input(r"Use {0} for term, {1} for definition, {2} for separator, {3} for note index, "
                                    r"\n for newline, and \t for tab")
            if new_format is None:
                print("Canceled input. (4)")
            else:
                new_format = new_format.replace("\\n", "\n")
                new_format = new_format.replace("\\t", "\t")
                settings.definition_format2 = new_format

        edit_df1 = yn_input("Do you want to edit Definition Format 1?\n"
                            "The current format is " + repr(settings.definition_format1))
        if edit_df1 is None:
            return print("Canceled input. (5)")
        if edit_df1:
            new_format = text_input(r"Use {0} for term, {1} for definition, {2} for separator, {3} for note index, "
                                    r"\n for newline, and \t for tab")
            if new_format is None:
                print("Canceled input. (6)")
            else:
                new_format = new_format.replace("\\n", "\n")
                new_format = new_format.replace("\\t", "\t")
                settings.definition_format1 = new_format

        edit_tf2 = yn_input("Do you want to edit Term Format 2?\n"
                            "The current format is " + repr(settings.term_format2))
        if edit_tf2 is None or not edit_tf2:
            return print("Canceled input. (7)")

        if edit_tf2:
            new_format = text_input(r"Use {0} for term, {1} for definition, {2} for separator, {3} for note index, "
                                    r"\n for newline, and \t for tab")
            if new_format is None:
                print("Canceled input. (8)")
            else:
                new_format = new_format.replace("\\n", "\n")
                new_format = new_format.replace("\\t", "\t")
                settings.term_format2 = new_format

    def study_settings_order(self):
        settings = self.current_notebook.study_settings
        settings.term_first = not settings.term_first
        print("Term First set to: " + str(settings.term_first))

    def study_settings_random(self):
        settings = self.current_notebook.study_settings
        settings.random = not settings.random
        print("Random set to: " + str(settings.random))

    def study_settings_extensions(self):
        settings = self.current_notebook.study_settings
        noteutil = self.current_notebook.noteutil

        include_extensions = yn_input("Would you like to include extensions?")
        if include_extensions is None:
            return print("Canceled input. (0)")
        settings.include_extensions = include_extensions

        for ext_name in noteutil.extension_names:
            edit_ext = yn_input("Do you want to edit the Extension \"{0}\"?".format(ext_name))
            if edit_ext is None:
                return print("Canceled input. (1)")
            if edit_ext:
                edit_format = yn_input("Do you want to edit the Extension format for this extension?\n"
                                       "The current format is: " + repr(settings.extension_format[ext_name]))
                if edit_format is None:
                    return print("Canceled input. (2)")
                if edit_format:
                    new_format = text_input(r"Use {0} for name, {1} for content, \n for newline, and \t for tab")
                    if new_format is None:
                        return print("Canceled input. (3)")
                    else:
                        new_format = new_format.replace("\\n", "\n")
                        new_format = new_format.replace("\\t", "\t")
                        settings.extension_format[ext_name] = new_format

                term_first = yn_input("Should this term appear with the term (Y) or with the definition (N)?")
                if term_first is None:
                    return print("Canceled input. (4)")
                settings.extension_first[ext_name] = term_first
    
    def quiz(self):
        print("""
        quiz    : Shows this.
        
        Quizzing:
            quiz division       : Choose the division to quiz yourself with.
            quiz generate       : Generates and begins a quiz.
            quiz correct        : Displays all correct pairs.
            quiz incorrect      : Displays all incorrect pairs.
            quiz unmarked       : Displays all unmarked pairs.
            quiz clear          : Empties the correct and incorrect list.
            quiz save           : Saves the correct and incorrect terms to the .qz file.
            quiz load           : Loads the correct and incorrect terms from the .qz file.
            """)

    def quiz_division(self):
        settings = self.current_notebook.study_settings
        divisions = list(map(lambda n: n.heading_name, self.current_notebook.noteutil.heading_order))
        divisions.extend(self.current_notebook.noteutil.category_names)
        divisions.insert(0, "unmarked")
        divisions.insert(0, "correct")
        divisions.insert(0, "incorrect")
        divisions.insert(0, "none")

        for i, division in enumerate(divisions):
            print("\t{0}. {1}".format(i + 1, division))
        division_choice = range_input("Select the number of the division you want.", range(1, len(divisions) + 1))
        if division_choice is None:
            return print("Canceled input. (0)")
        self.current_notebook.quiz.select_pairs(divisions[division_choice - 1])
        print("Quiz division set to: " + settings.heading)

    def quiz_generate(self):
        quiz = self.current_notebook.quiz
        settings = self.current_notebook.study_settings

        filter_notes = yn_input("Do you want to filter the current division you are using more?")
        if filter_notes is None:
            return print("Canceled input. (0)")
        if filter_notes:

            remove_correct = yn_input("Would you like to remove terms marked correct?")
            if remove_correct is None:
                return print("Canceled input. (1)")
            if remove_correct:
                quiz.pairs = list(filterfalse(lambda p: p in quiz.correct, quiz.pairs))

            remove_incorrect = yn_input("Would you like to remove terms marked incorrect?")
            if remove_incorrect is None:
                return print("Canceled input. (2)")
            if remove_incorrect:
                quiz.pairs = list(filterfalse(lambda p: p in quiz.incorrect, quiz.pairs))

            remove_unmarked = yn_input("Would you like to remove terms that are unmarked?")
            if remove_unmarked is None:
                return print("Canceled input. (3)")
            if remove_unmarked:
                quiz.pairs = list(filter(lambda p: p in quiz.correct or p in quiz.incorrect, quiz.pairs))

        session = list(quiz.generate(randomize=settings.random))
        quiz.select_pairs(settings.heading)
        for note in session:
            term, definition, separator, nindex = note.term, note.definition, note.separator, note.nindex
            if settings.term_first:
                question = settings.term_format1.format(term, definition, separator, nindex)
                if settings.include_extensions:
                    for extension in note.extensions:
                        if settings.extension_first[extension.name]:
                            question += settings.extension_format[extension.name].format(
                                extension.name, extension.content)
                input(question)
                answer = settings.definition_format2.format(term, definition, separator, nindex)
                if settings.include_extensions:
                    for extension in note.extensions:
                        if not settings.extension_first[extension.name]:
                            answer += settings.extension_format[extension.name].format(
                                extension.name, extension.content)
                print(answer)
            else:
                question = settings.definition_format1.format(term, definition, separator, nindex)
                if settings.include_extensions:
                    for extension in note.extensions:
                        if settings.extension_first[extension.name]:
                            question += settings.extension_format[extension.name].format(
                                extension.name, extension.content)
                input(question)
                answer = settings.term_format2.format(term, definition, separator, nindex)
                if settings.include_extensions:
                    for extension in note.extensions:
                        if not settings.extension_first[extension.name]:
                            answer += settings.extension_format[extension.name].format(
                                extension.name, extension.content)
                print(answer)

            def quiz_options():
                while True:
                    option = text_input("Enter 'c' for correct, 'i' for incorrect, or enter to continue")
                    if option is None:
                        print("Canceled input. (1)")
                        return False
                    option = option.strip().lower()
                    if option in ["c", "i", ""]:
                        if option == "c":
                            quiz.append(note, correct=True)
                            print("Added {0} to correct list.".format(note.term))
                        elif option == "i":
                            quiz.append(note, correct=False)
                            print("Added {0} to incorrect list.".format(note.term))
                        return True
                    else:
                        print("Input was not 'c' or 'i'. Try again.")

            proceed = quiz_options()
            if proceed is False:
                return
        print("All pairs have been cycled.")
        save = yn_input("Save progress?")
        if save is None:
            return print("Canceled input. (2)")
        if save:
            quiz.save()

    def quiz_correct(self):
        quiz = self.current_notebook.quiz
        print("Correct Terms:")
        for note in quiz.correct:
            print("\t" + note.term)

    def quiz_incorrect(self):
        quiz = self.current_notebook.quiz
        print("Incorrect Terms:")
        for note in quiz.incorrect:
            print("\t" + note.term)

    def quiz_unmarked(self):
        quiz = self.current_notebook.quiz
        noteutil = self.current_notebook.noteutil
        unmarked = list(filterfalse(lambda p: p in quiz.incorrect or p in quiz.correct, noteutil.pairs))
        print("Unmarked Terms:")
        for note in unmarked:
            print("\t" + note.term)

    def quiz_clear(self):
        quiz = self.current_notebook.quiz
        quiz.clear()
        print("Correct and Incorrect lists cleared.")

    def quiz_save(self):
        quiz = self.current_notebook.quiz
        quiz.save()
        print("Quiz terms saved successfully.")

    def quiz_load(self):
        quiz = self.current_notebook.quiz
        quiz.load()
        print("Quiz terms loaded successfully.")

    def leitner(self):
        print("""
        leitner:    Shows this
        
        Leitner System:
            leitner settings        : Modify Leitner's boxes settings. 
            leitner boxes           : Display the boxes and their time periods.
            leitner notes           : Display the boxes and the Notes they have inside of them.
            leitner generate        : Generate and begin a Leitner session.
            leitner reset           : Reset all of the Notes to Box 1
            leitner save            : Save the location of all Notes into the .lt file.
            leitner load            : Load the state of a Leitner system from the .lt file.
        """)

    def leitner_settings(self):
        leitner = self.current_notebook.leitner
        self.leitner_boxes()
        add_box = yn_input("Would you like to add another box to the end?")
        if add_box is None:
            return print("Canceled input. (0)")
        if add_box:
            time = range_input("Enter a time period for the box (how long between each review.)\n"
                               "It must be greater than the current longest time period (max 9999999).",
                               range(leitner.times[len(leitner.times)] + 1, 10000000))
            if time is None:
                return print("Canceled input. (1)")
            try:
                leitner.append_box(time)
                return print("Added Box {0} with time period {1}.".format(len(leitner.boxes), time))
            except TimeTooShort:
                return print("The time you gave was shorter than the current longest time period.")

        pop_box = yn_input("Would you like to remove the last box?")
        if pop_box is None:
            return print("Canceled input. (2)")
        if pop_box:
            try:
                leitner.pop_box()
                print("Removed Box {0}.".format(len(leitner.boxes) + 1))
            except LastBox:
                return print("The Leitner system only has one box left (the minimum).")

    def leitner_boxes(self):
        leitner = self.current_notebook.leitner
        boxes_description = ""
        for number, time in leitner.times.items():
            boxes_description += "Box {0} with time period {1}".format(number, time) + "\n"
        print(boxes_description)

    def leitner_notes(self):
        leitner = self.current_notebook.leitner
        boxes_description = ""
        for number, note_list in leitner.boxes.items():
            boxes_description += "Box {0} with time period {1}:\n".format(number, leitner.times[number])
            for note in note_list:
                boxes_description += "\t" + note.content + "\n"
        print(boxes_description)

    def leitner_generate(self):
        leitner = self.current_notebook.leitner
        settings = self.current_notebook.study_settings

        for note in leitner.generate(randomize=settings.random):
            term, definition, separator, nindex = note.term, note.definition, note.separator, note.nindex
            if settings.term_first:
                question = settings.term_format1.format(term, definition, separator, nindex)
                if settings.include_extensions:
                    for extension in note.extensions:
                        if settings.extension_first[extension.name]:
                            question += settings.extension_format[extension.name].format(
                                extension.name, extension.content)
                input(question)
                answer = settings.definition_format2.format(term, definition, separator, nindex)
                if settings.include_extensions:
                    for extension in note.extensions:
                        if not settings.extension_first[extension.name]:
                            answer += settings.extension_format[extension.name].format(
                                extension.name, extension.content)
                print(answer)
            else:
                question = settings.definition_format1.format(term, definition, separator, nindex)
                if settings.include_extensions:
                    for extension in note.extensions:
                        if settings.extension_first[extension.name]:
                            question += settings.extension_format[extension.name].format(
                                extension.name, extension.content)
                input(question)
                answer = settings.term_format2.format(term, definition, separator, nindex)
                if settings.include_extensions:
                    for extension in note.extensions:
                        if not settings.extension_first[extension.name]:
                            answer += settings.extension_format[extension.name].format(
                                extension.name, extension.content)
                print(answer)

            def quiz_options():
                while True:
                    option = text_input("Enter 'c' for correct, 'i' for incorrect, or enter to continue")
                    if option is None:
                        print("Canceled input. (1)")
                        return False
                    option = option.strip().lower()
                    if option in ["c", "i", ""]:
                        if option == "c":
                            leitner.correct(note)
                            print("Moved {0} to Box {1}.".format(note.term, note.box))
                        elif option == "i":
                            leitner.incorrect(note)
                            print("Moved {0} to Box 1.".format(note.term))
                        return True
                    else:
                        print("Input was not 'c' or 'i'. Try again.")

            proceed = quiz_options()
            if proceed is False:
                return
        print("All pairs have been cycled.")
        save = yn_input("Save progress?")
        if save is None:
            return print("Canceled input. (2)")
        if save:
            leitner.save()

    def leitner_reset(self):
        leitner = self.current_notebook.leitner
        leitner.reset()
        print("Leitner reset successfully.")

    def leitner_save(self):
        leitner = self.current_notebook.leitner
        leitner.save()
        print("Leitner terms saved successfully.")

    def leitner_load(self):
        leitner = self.current_notebook.leitner
        leitner.load()
        print("Leitner terms loaded successfully.")


def main():
    print(
        """
Welcome to NoteUtil's command line implementation!
==================================================

Before we begin, you must first set up a few settings:""")

    try:
        commands = Commands(noteutils)
        commands.current_notebook = commands.notebooks[noteutils[0].note_file]
        commands.select()
        Commands.display()
        command_loop(commands)
    except KeyboardInterrupt:
        pass
    finally:
        print("Bye!")


def command_loop(commands: Commands):
    while True:
        command = text_input("Enter a command.")
        if command is None:
            return print("Canceled input. (0)")
        if command.lower().strip() in commands.commands:
            commands.commands[command]()
        else:
            print("Command not found.")


main()








