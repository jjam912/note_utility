import os
import tkinter as tk
import tkinter.font as tkfont
import noteutil as nu
from disabled_text import DisabledText
from editor import EditorView
from searcher import SearcherView
from quizzer import QuizzerView
from reviewer import ReviewerView


class ConfiguratorView:
    def __init__(self, root, noteutil=None, quiz=None, leitner=None):
        self.root = root
        self.root.title("NoteUtil Configurator")
        self.controller = ConfiguratorController(self, noteutil, quiz, leitner)

        self.menu_bar = None
        self.init_menu_bar()

        self.config_label = None
        self.status_label = None
        self.init_info_labels()

        self.line_numbers_text = None
        self.text_editor = None
        self.init_text_editor()

        self.editor_button = None
        self.searcher_button = None
        self.quizzer_button = None
        self.reviewer_button = None
        self.init_actions_frame()

        if not os.path.exists(os.path.join(os.getcwd(), "notes")):
            os.mkdir(os.path.join(os.getcwd(), "notes"))

    def init_menu_bar(self):
        self.menu_bar = tk.Menu(self.root, tearoff=False)
        self.init_file_menu()
        self.init_edit_menu()
        self.init_view_menu()
        self.init_help_menu()
        self.root.config(menu=self.menu_bar)

    def init_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="New config", command=self.controller.on_new_config)
        file_menu.add_command(label="Open config", command=self.controller.on_open_config)
        file_menu.add_command(label="Save", command=self.controller.on_save)
        file_menu.add_command(label="Save as", command=self.controller.on_save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Compile", command=self.controller.on_compile)
        self.menu_bar.add_cascade(menu=file_menu, label="File")

    def init_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        edit_menu.add_command(label="Find", command=self.controller.on_find)
        edit_menu.add_command(label="Replace", command=self.controller.on_replace)
        self.menu_bar.add_cascade(menu=edit_menu, label="Edit")

    def init_view_menu(self):
        view_menu = tk.Menu(self.menu_bar, tearoff=False)
        view_menu.add_checkbutton(label="Show line number", variable=self.controller.line_numbers,
                                  command=self.controller.on_line_numbers)
        view_menu.add_checkbutton(label="Highlight current line", variable=self.controller.highlight,
                                  command=self.controller.on_highlight)
        self.menu_bar.add_cascade(menu=view_menu, label="View")

    def init_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        help_menu.add_command(label="What config?", command=self.controller.on_what_config)
        help_menu.add_command(label="About", command=self.controller.on_about)
        self.menu_bar.add_cascade(menu=help_menu, label="Help")

    def init_info_labels(self):
        self.config_label = tk.Label(self.root, text="Your current config file is: " +
                                                     str(self.controller.config_filename.get()), padx=10, anchor=tk.W)
        self.status_label = tk.Label(self.root, text="Open a config file or create a new one and then compile it. " +
                                                     "If you already have a config file, use File >> Open Config.",
                                     padx=10, anchor=tk.W)
        self.config_label.pack(side=tk.TOP, padx=30, pady=(10, 0), fill=tk.X)
        self.status_label.pack(side=tk.TOP, padx=30, fill=tk.X)

    def init_text_editor(self):
        text_editor_frame = tk.Frame(self.root)
        self.line_numbers_text = DisabledText(text_editor_frame, width=4, font=tkfont.Font(family="Ubuntu", size=12))
        self.text_editor = tk.Text(text_editor_frame, wrap=tk.NONE, undo=True,
                                   font=tkfont.Font(family="Ubuntu", size=12))
        xscrollbar = tk.Scrollbar(text_editor_frame, orient=tk.HORIZONTAL, command=self.text_editor.xview)
        yscrollbar = tk.Scrollbar(text_editor_frame, orient=tk.VERTICAL, command=self.text_editor.yview)
        self.text_editor.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.line_numbers_text.pack(side=tk.LEFT, fill=tk.Y)
        self.text_editor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.controller.on_new_config()
        text_editor_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=40, pady=10)

    def init_actions_frame(self):
        actions_frame = tk.LabelFrame(self.root, text="Choose a method of review:")
        self.editor_button = tk.Button(actions_frame, text="Editor", bd=5, command=self.controller.on_editor)
        self.searcher_button = tk.Button(actions_frame, text="Searcher", state=tk.DISABLED, bd=5,
                                         command=self.controller.on_searcher)
        self.quizzer_button = tk.Button(actions_frame, text="Quizzer", state=tk.DISABLED, bd=5,
                                        command=self.controller.on_quizzer)
        self.reviewer_button = tk.Button(actions_frame, text="Reviewer", state=tk.DISABLED, bd=5,
                                         command=self.controller.on_reviewer)
        self.editor_button.pack(side=tk.LEFT, padx=5, pady=(5, 10), fill=tk.X, expand=True)
        self.searcher_button.pack(side=tk.LEFT, padx=5, pady=(5, 10), fill=tk.X, expand=True)
        self.quizzer_button.pack(side=tk.LEFT, padx=5, pady=(5, 10), fill=tk.X, expand=True)
        self.reviewer_button.pack(side=tk.LEFT, padx=5, pady=(5, 10), fill=tk.X, expand=True)
        actions_frame.pack(side=tk.TOP, fill=tk.X, padx=40, pady=(0, 10))

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class ConfiguratorController:
    def __init__(self, view, noteutil, quiz, leitner):
        self.count = 0
        self.view = view
        self.noteutil = noteutil
        self.quiz = quiz
        self.leitner = leitner

        self.config_filename = tk.StringVar(value="None")
        self.line_numbers = tk.BooleanVar(value=True)
        self.highlight = tk.BooleanVar(value=True)

    def on_new_config(self):
        self.view.text_editor.delete(1.0, tk.END)
        with open("CONFIG_TEMPLATE.txt", mode="r") as f:
            self.view.text_editor.insert(tk.END, f.read())

    def on_open_config(self):
        self.count += 1
        print(self.count)

    def on_save(self):
        self.count += 1
        print(self.count)

    def on_save_as(self):
        self.count += 1
        print(self.count)

    def on_compile(self):
        self.view.searcher_button.config(state=tk.NORMAL)
        self.view.quizzer_button.config(state=tk.NORMAL)
        self.view.reviewer_button.config(state=tk.NORMAL)

    def on_find(self):
        self.count += 1
        print(self.count)

    def on_replace(self):
        self.count += 1
        print(self.count)

    def on_select_all(self):
        self.count += 1
        print(self.count)

    def on_line_numbers(self):
        self.count += 1
        print(self.count)

    def on_highlight(self):
        self.count += 1
        print(self.count)

    def on_what_config(self):
        self.count += 1
        print(self.count)

    def on_about(self):
        self.count += 1
        print(self.count)

    def on_editor(self):
        toplevel = tk.Tk()
        toplevel.geometry("1600x900+160+90")
        EditorView(toplevel, self.noteutil, self.quiz, self.leitner)
        toplevel.mainloop()

    def on_searcher(self):
        self.view.clear()
        SearcherView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_quizzer(self):
        self.view.clear()
        QuizzerView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_reviewer(self):
        self.view.clear()
        ReviewerView(self.view.root, self.noteutil, self.quiz, self.leitner)


if __name__ == "__main__":
    gui = tk.Tk()
    app = ConfiguratorView(gui)
    gui.geometry("1600x900+160+90")
    gui.mainloop()
