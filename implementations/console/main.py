from noteutil import NoteUtil, Quiz, Leitner
from noteutil.comparisons import CompareOptions
import os
import sys
from typing import List


os.chdir(os.path.join(os.getcwd(), "notes"))
# Construct and add your NoteUtils here::
math = NoteUtil("heading_config.txt")
noteutils = [math]
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

    input_ = input(message + "\n\tType 'exit', 'quit' or 'stop' to stop input.\n")

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
        input_ = text_input(message)
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
        if os.path.isfile(self.quiz.qz_file):
            self.quiz.load()
        self.leitner = Leitner(noteutil)
        if os.path.isfile(self.leitner.lt_file):
            self.leitner.load()

        # Settings
        self.settings = Settings(self)


class Settings:
    def __init__(self, session: Session):
        # TODO: Some of these probably have to be properties
        self.session = session
        self.random = True
        self.current_file = session.noteutil.note_file
        self.current_heading = None
        self.term_first = True
        self.include_extensions = True
        self.advanced_search = True


class Commands:
    def __init__(self, noteutils: List[NoteUtil]):
        self.sessions = {}
        for nu in noteutils:
            self.sessions[nu.note_file] = Session(nu)
        self.current_session = None
        self.commands = {
            "commands": self.display,
            "select":   self.select,
            "search":   self.search,
            "quiz":     self.quiz,
            "leitner":  self.leitner
        }

    @staticmethod
    def display():
        print(
            """Here are the commands:
            
        commands    : Shows this.
        select      : Select a note file to use.
        search      : Search for a Note.
        quiz        : Start a quiz.
        leitner     : Begin a Leitner review.
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

    def search(self):
        noteutil = self.current_session.noteutil
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

        define = yn_input("Would you like to look at a specific Note more in depth? (Y/N)")
        if define is None or define is False:
            return print("Canceled input. (6)")

        nindex = range_input("Choose a Note from the found Note list", range(1, len(note_list) + 1))
        if nindex is None:
            return print("Canceled input. (7)")
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

    def quiz(self):
        pass

    def leitner(self):
        pass


def main():
    print(
        """
Welcome to NoteUtil's command line implementation!
==================================================

Before we begin, you must first set up a few settings:""")

    commands = Commands(noteutils)
    commands.select()
    Commands.display()
    command_loop(commands)


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








