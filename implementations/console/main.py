from noteutil import NoteUtil, Quiz, Leitner
from noteutil.notes import Note
from noteutil.comparisons import CompareOptions
from noteutil.errors import NoteError
import os
from typing import List


os.chdir(os.path.join(os.getcwd(), "notes"))
# Construct and add your NoteUtils here::
math = NoteUtil("heading_config.txt")
euro = NoteUtil("euro_config.txt")
noteutils = [math, euro]
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


class Session:
    def __init__(self, noteutil: NoteUtil):
        self.noteutil = noteutil
        self.quiz = Quiz(noteutil)
        self.quiz.load()
        self.leitner = Leitner(noteutil)
        self.leitner.load()

        # Settings
        self.noteutil_settings = NoteUtilSettings(self)
        self.quiz_settings = QuizSettings(self)
        self.leitner_settings = LeitnerSettings(self)


class NoteUtilSettings:
    def __init__(self, session: Session):
        self.session = session
        self.file = session.noteutil.note_file
        self.simple_search = True
        self.ask_define = False


class QuizSettings:
    def __init__(self, session: Session):
        self.session = session
        self.file = session.quiz.qz_file
        self.term_format1 = r"Define the term: {0}"
        self.definition_format2 = r"The definition is: {0}"
        self.definition_format1 = r"Guess the term: {0}"
        self.term_format2 = r"The term is: {0}"

        self.random = True
        self.term_first = True
        self.include_extensions = True
        self.extension_format = r"\n{0}: {1}"

    @property
    def heading(self):
        heading = self.session.quiz.heading
        if heading is None:
            return "None (All)"
        elif isinstance(heading, str):
            return heading.title()
        elif isinstance(heading, Note):
            return heading.heading_name
        return "Error"


class LeitnerSettings:
    def __init__(self, session: Session):
        self.session = session
        self.file = session.leitner.lt_file


class Commands:
    def __init__(self, noteutils: List[NoteUtil]):
        self.sessions = {}
        for nu in noteutils:
            self.sessions[nu.note_file] = Session(nu)
        self.current_session = None
        self.commands = {
            "commands":     self.display,
            "select":       self.select,

            "noteutil":                     self.noteutil,
            "noteutil settings":            self.noteutil_settings,
            "noteutil settings search":     self.noteutil_settings_search,
            "noteutil settings define":     self.noteutil_settings_define,
            "noteutil headings":            self.noteutil_headings,
            "noteutil extensions":          self.noteutil_extensions,
            "noteutil search":              self.noteutil_search,
            "noteutil edit":                self.noteutil_edit,

            "quiz":                         self.quiz,
            "quiz settings":                self.quiz_settings,
            "quiz settings heading":        self.quiz_settings_heading,
            "quiz settings format":         self.quiz_settings_format,
            "quiz settings order":          self.quiz_settings_order,
            "quiz settings random":         self.quiz_settings_random,
            "quiz settings extensions":     self.quiz_settings_extensions,

            "leitner":      self.leitner
        }

    @staticmethod
    def display():
        print(
            """Here are the commands:
            
        commands    : Shows this.
        select      : Select a note file to use.
        noteutil    : Shows commands for NoteUtil.
        quiz        : Shows commands for Quiz.
        leitner     : Shows commands for Leitner.
        """)

    def select(self):
        print("Please choose one of the following note files:")
        for i, note_file in enumerate(self.sessions.keys()):
            print("\t{0}. {1}".format(i + 1, note_file))
        i_nu = range_input("Select the number corresponding to the note file you want to use.",
                           range(1, len(self.sessions) + 1))
        if i_nu is None:
            return print("Canceled input. (1)")

        note_file = list(self.sessions.keys())[i_nu - 1]
        self.current_session = self.sessions[note_file]

    def noteutil(self):
        print(
            """Here are the NoteUtil commands:

        noteutil    : Shows this.
        
        Settings
            noteutil settings   : Displays your NoteUtil settings.
            noteutil settings search    : Toggles between simple and advanced search.
            noteutil settings define    : Toggles between asking to define in depth and not
        NoteUtil
            noteutil headings       : Shows heading order and names.
            noteutil extensions     : Shows extension names
            noteutil search         : Search for a Note.
            noteutil edit           : Edit the content of a Note.
        """)

    def noteutil_settings(self):
        settings = self.current_session.noteutil_settings
        print("Noteutil Settings:")
        print("\tSimple Search: " + str(settings.simple_search))
        print("\tAsk Define: " + str(settings.ask_define))

    def noteutil_settings_search(self):
        settings = self.current_session.noteutil_settings
        settings.simple_search = not settings.simple_search
        print("Simple Search set to: " + str(settings.simple_search))

    def noteutil_settings_define(self):
        settings = self.current_session.noteutil_settings
        settings.ask_define = not settings.ask_define
        print("Ask Define set to: " + str(settings.ask_define))

    def noteutil_headings(self):
        noteutil = self.current_session.noteutil

        heading_description = ""
        heading_description += "Heading Levels:" + "\n"

        level = 1
        for gname, anames in noteutil.heading_level.items():  # General name, Actual names
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

    def noteutil_extensions(self):
        noteutil = self.current_session.noteutil

        print("Extensions:")
        for name, bounds in zip(noteutil.extension_names, noteutil.extension_bounds):
            print("\t" + name)
            print("\t\tLeft bound:  " + bounds[0])
            print("\t\tRight bound: " + bounds[1])

    def noteutil_search(self):
        noteutil = self.current_session.noteutil
        settings = self.current_session.noteutil_settings

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
                    return print("No Notes found. (1)")

            elif search_type in [2, 5]:
                if search_type == 2:
                    query = range_input("Enter the note index of the Note.", range(len(noteutil.notes)))
                else:
                    query = range_input("Enter the level of the Heading.", range(1, noteutil.levels + 1))
                if query is None:
                    return print("Canceled input. (4)")

                note_list = noteutil.get_list(**{search_conversion[search_type]: query})
                if not note_list:
                    return print("No Notes found. (2)")

            elif search_type in [7]:
                query = text_input("Enter the Extension name and make sure it matches exactly.")
                if query is None:
                    return print("Canceled input. (5)")

                note_list = noteutil.get_list(**{search_conversion[search_type]: query, "compare": CompareOptions.IN})
                if not note_list:
                    return print("No Notes found. (3)")
            else:
                return print("Error: Search type not in range.")

        for i, note in enumerate(note_list):
            print("\t{0}. {1}".format(i + 1, note.content))

        if settings.ask_define:
            define = yn_input("Would you like to look at a specific Note more in depth?")
            if define is None or define is False:
                return print("Canceled input. (6)")

            if len(note_list) > 1:
                nindex = range_input("Choose the number of a Note from the found Note list", range(1, len(note_list) + 1))
                if nindex is None:
                    return print("Canceled input. (7)")
            else:
                nindex = 1
            note = note_list[nindex - 1]
            define_type = range_input("Choose an attribute of the Note you want defined."
                                      "\n\t1. Content"
                                      "\n\t2. Note index"
                                      "\n\t3. Term"
                                      "\n\t4. Definition"
                                      "\n\t5. Heading level"
                                      "\n\t6. Heading name"
                                      "\n\t7. Notes"
                                      "\n\t8. Extensions", range(1, 9))
            if define_type is None:
                return print("Canceled input. (8)")
            define_conversion = {1: "content", 2: "nindex", 3: "term", 4: "definition",
                                 5: "level", 6: "heading_name", 7: "notes", 8: "extensions"}
            if define_type in [1, 2, 3, 4, 5, 6]:
                print(getattr(note, define_conversion[define_type]))
            elif define_type in [7]:
                notes = noteutil.notes[note.begin_nindex:note.end_nindex]
                for i, note in enumerate(notes):
                    print("\t{0}. {1}".format(i + 1, note.content))

            elif define_type in [8]:
                extensions = note.extensions
                for i, ext in enumerate(extensions):
                    print("\t{0}. {1}".format(i + 1, ext.content))

    def noteutil_edit(self):
        noteutil = self.current_session.noteutil

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

    def quiz(self):
        print(
            """Here are the Quiz commands:

        quiz    : Shows this.
        
        Settings
            quiz settings               : Displays your Quiz settings.
            quiz settings format        : Sets up how term and definition should be formatted.
            quiz settings order         : Toggles between term and definition being said first.
            quiz settings random        : Toggles between chronological and random Note generation.
            quiz settings heading       : Selects the heading that the Quiz should generate Notes from.
            quiz settings extensions    : Sets up how extensions should be handled.
        Quizzing
            quiz generate       : Generates and begins a quiz.
            quiz correct        : Displays all correct pairs.
            quiz incorrect      : Displays all incorrect pairs.
            quiz clear          : Empties the correct and incorrect list.
            quiz save           : Saves the correct and incorrect terms to the .qz file.
            quiz load           : Loads the correct and incorrect terms from the .qz file.
        """)

    def quiz_settings(self):
        settings = self.current_session.quiz_settings
        print("Quiz Settings:")
        print("\tHeading: " + settings.heading)
        print("\tTerm Format 1: " + settings.term_format1)
        print("\tDefinition Format 2: " + settings.definition_format2)
        print("\tDefinition Format 1: " + settings.definition_format1)
        print("\tTerm Format 2: " + settings.term_format2)
        print("\tRandom: " + str(settings.random))
        print("\tTerm First: " + str(settings.term_first))
        print("\tInclude Extensions: " + str(settings.include_extensions))
        print("\tExtension Format: " + settings.extension_format)

    def quiz_settings_format(self):
        # TODO: After quiz_question
        print("""
        The difference between formats 1 and 2 depends on whether Term First is True.
            1 means that the prompt for either the term or the definition is first. 
            2 means that the answer for either the term or the definition is second.
        When Term First is True, Term Format 1 and Definition Format 2 are used.
            This is because the term is asked first and then the definition is revealed second.
        When Term First is False, Definition Format 1 and Term Format 2 are used.
            This is because the definition is asked first and then the term is revealed second.
        """)

        settings = self.current_session.quiz_settings
        edit_tf1 = yn_input("Do you want to edit Term Format 1?")
        if edit_tf1 is None:
            return print("Canceled input. (1)")
        if edit_tf1:
            pass

        edit_df2 = yn_input("Do you want to edit Definition Format 2?")
        if edit_df2 is None:
            return print("Canceled input. ( )")
        if edit_df2:
            pass

        edit_df1 = yn_input("Do you want to edit Definition Format 1?")
        if edit_df1 is None:
            return print("Canceled input. ( )")
        if edit_df1:
            pass

        edit_tf2 = yn_input("Do you want to edit Term Format 2?")
        if edit_tf2 is None or not edit_tf2:
            return print("Canceled input. ( )")

        if edit_tf2:
            pass

    def quiz_settings_order(self):
        settings = self.current_session.quiz_settings
        settings.term_first = not settings.term_first
        print("Term First set to: " + str(settings.term_first))

    def quiz_settings_random(self):
        settings = self.current_session.quiz_settings
        settings.random = not settings.random
        print("Random set to: " + str(settings.random))

    def quiz_settings_heading(self):
        settings = self.current_session.quiz_settings
        headings = list(map(lambda n: n.heading_name, self.current_session.noteutil.heading_order))
        headings.insert(0, "unmarked")
        headings.insert(0, "correct")
        headings.insert(0, "incorrect")
        headings.insert(0, "none")

        for i, heading in enumerate(headings):
            print("\t{0}. {1}".format(i + 1, heading))
        heading_choice = range_input("Select the number of the heading you want.", range(1, len(headings) + 1))
        if heading_choice is None:
            return print("Canceled input. (0)")
        self.current_session.quiz.select_heading(headings[heading_choice - 1])
        print("Quiz heading set to: " + settings.heading)

    def quiz_settings_extensions(self):
        settings = self.current_session.quiz_settings
        edit_extensions = yn_input("Do you want to edit the Extension Format?")
        if edit_extensions is None:
            return print("Canceled input. (0)")
        if edit_extensions:
            pass

        include_extensions = yn_input("Do you want to include extensions?")
        if include_extensions is None:
            return print("Canceled input. ( )")
        settings.include_extensions = include_extensions
        print("Include Extensions set to: " + str(settings.include_extensions))

    def leitner(self):
        pass


def main():
    print(
        """
Welcome to NoteUtil's command line implementation!
==================================================

Before we begin, you must first set up a few settings:""")

    try:
        commands = Commands(noteutils)
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
        if command.lower() in commands.commands:
            commands.commands[command]()
        else:
            print("Command not found.")


main()








