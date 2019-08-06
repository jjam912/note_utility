"""GUI for configuring NoteUtil and editing the config file."""
import os
import tkinter as tk
import tkinter.font as tkfont
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmsgbox
import noteutil as nu
from noteutil.errors import NoteUtilError, QuizError, LeitnerError
import json
import webbrowser


NOTES_DIR = os.path.join(os.getcwd(), "notes")
SETTINGS_DIR = os.path.join(os.getcwd(), "settings.json")


class ConfiguratorView:
    def __init__(self, root, noteutil=None, quiz=None, leitner=None):
        self.root = root
        self.root.title("NoteUtil Configurator - Untitled")
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

        self.controller.read_settings()
        if noteutil is not None and quiz is not None and leitner is not None:
            with open(noteutil.config_file, mode="r") as f:
                self.controller.on_open_config(f)

        self.root.protocol("WM_DELETE_WINDOW", self.controller.on_close)

    def init_menu_bar(self):
        self.menu_bar = tk.Menu(self.root, tearoff=False)
        self.init_file_menu()
        self.init_edit_menu()
        self.init_view_menu()
        self.init_help_menu()
        self.root.config(menu=self.menu_bar)

    def init_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="New config", accelerator="Ctrl+N", command=self.controller.on_new_config)
        self.root.bind("<Control-N>", lambda e: self.controller.on_new_config())
        self.root.bind("<Control-n>", lambda e: self.controller.on_new_config())
        file_menu.add_command(label="Open config", accelerator="Ctrl+O", command=self.controller.on_open_config)
        self.root.bind("<Control-O>", lambda e: self.controller.on_open_config())
        self.root.bind("<Control-o>", lambda e: self.controller.on_open_config())
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.controller.on_save)
        self.root.bind("<Control-S>", lambda e: self.controller.on_save())
        self.root.bind("<Control-s>", lambda e: self.controller.on_save())
        file_menu.add_command(label="Save as", accelerator="Ctrl+Shift+S", command=self.controller.on_save_as)
        self.root.bind("<Control-Shift-S>", lambda e: self.controller.on_save_as())
        self.root.bind("<Control-Shift-s>", lambda e: self.controller.on_save_as())
        file_menu.add_separator()
        file_menu.add_command(label="Compile", accelerator="Ctrl+G", command=self.controller.on_compile)
        self.root.bind("<Control-G>", lambda e: self.controller.on_compile())
        self.root.bind("<Control-g>", lambda e: self.controller.on_compile())
        self.menu_bar.add_cascade(menu=file_menu, label="File")

    def init_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=self.controller.on_find)
        self.root.bind("<Control-F>", lambda e: self.controller.on_find())
        self.root.bind("<Control-f>", lambda e: self.controller.on_find())
        edit_menu.add_command(label="Replace", accelerator="Ctrl+R", command=self.controller.on_replace)
        self.root.bind("<Control-R>", lambda e: self.controller.on_replace())
        self.root.bind("<Control-r>", lambda e: self.controller.on_replace())
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
        self.config_label = tk.Label(self.root, text="Your current config file is: None", padx=10, anchor=tk.W)
        self.status_label = tk.Label(self.root, text="Open a config file or create a new one and then compile it. " +
                                                     "If you already have a config file, use File >> Open Config.",
                                     padx=10, anchor=tk.W)
        self.config_label.pack(side=tk.TOP, padx=30, pady=(10, 0), fill=tk.X)
        self.status_label.pack(side=tk.TOP, padx=30, fill=tk.X)

    def init_text_editor(self):
        text_editor_frame = tk.Frame(self.root)
        self.line_numbers_text = tk.Text(text_editor_frame, width=5, font=tkfont.Font(family="Ubuntu", size=12),
                                         state=tk.DISABLED)
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

    def unbind_all(self):
        self.root.unbind("<Control-N>")
        self.root.unbind("<Control-N>")
        self.root.unbind("<Control-O>")
        self.root.unbind("<Control-o>")
        self.root.unbind("<Control-S>")
        self.root.unbind("<Control-s>")
        self.root.unbind("<Control-Shift-S>")
        self.root.unbind("<Control-Shift-s>")
        self.root.unbind("<Control-G>")
        self.root.unbind("<Control-g>")
        self.root.unbind("<Control-F>")
        self.root.unbind("<Control-f>")
        self.root.unbind("<Control-R>")
        self.root.unbind("<Control-r>")

    def clear(self):
        self.unbind_all()
        for widget in self.root.winfo_children():
            widget.destroy()


class ConfiguratorController:
    def __init__(self, view, noteutil, quiz, leitner):
        self.count = 0
        self.view = view
        self.noteutil = noteutil
        self.quiz = quiz
        self.leitner = leitner

        if not os.path.exists(NOTES_DIR):
            os.mkdir(NOTES_DIR)
        if not os.path.exists(SETTINGS_DIR):
            with open(SETTINGS_DIR, mode="w") as f:
                f.write("{}")

        self.config_file_path = None
        self.config_file_name = None
        self.line_numbers = tk.BooleanVar(value=True)
        self.highlight = tk.BooleanVar(value=True)

        self.settings = {}

    def read_settings(self):
        with open(SETTINGS_DIR, mode="r") as f:
            try:
                program_settings = json.loads(f.read())
            except json.JSONDecodeError:
                program_settings = {}
            self.settings = program_settings.get("configurator", {})
        if self.settings:
            self.config_file_path = self.settings.get("config_file_path", None)
            self.config_file_name = self.settings.get("config_file_name", None)
            self.line_numbers.set(self.settings.get("line_numbers", True))
            self.highlight.set(self.settings.get("highlight", True))
            if self.config_file_path is not None:
                with open(self.config_file_path, mode="r") as f:
                    self.on_open_config(f)

    def save_settings(self):
        self.settings["config_file_path"] = self.config_file_path
        self.settings["config_file_name"] = self.config_file_name
        self.settings["line_numbers"] = self.line_numbers.get()
        self.settings["highlight"] = self.highlight.get()

        with open(SETTINGS_DIR, mode="r") as f:
            try:
                program_settings = json.loads(f.read())
            except json.JSONDecodeError:
                program_settings = {}
        program_settings["configurator"] = self.settings

        with open(SETTINGS_DIR, mode="w") as f:
            f.write(json.dumps(program_settings))

    def on_new_config(self):
        self.view.text_editor.delete(1.0, tk.END)
        with open("CONFIG_TEMPLATE.txt", mode="r") as f:
            self.view.text_editor.insert(tk.END, f.read())
            self.file_update()
        return "break"

    def on_open_config(self, file=None):
        if file is None:
            file = tkfiledialog.askopenfile(defaultextension=".txt", initialdir=NOTES_DIR, title="Open config",
                                            filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if file:
            self.view.text_editor.delete(1.0, tk.END)
            self.view.text_editor.insert(tk.END, file.read())
            self.file_update(file)
            self.on_compile()
        return "break"

    def file_update(self, file=None):
        if file:
            self.config_file_name = os.path.basename(file.name)
            self.config_file_path = file.name
            self.view.config_label.config(text="Your current config file is: " + self.config_file_name)
            self.view.status_label.config(text="Compile your file using File >> Compile")
            self.view.root.title("NoteUtil Configurator - " + self.config_file_name)
        else:
            self.config_file_name = None
            self.config_file_path = None
            self.view.config_label.config(text="Your current config file is: None")
            self.view.status_label.config(text="Open a config file or create a new one and then compile it. " +
                                               "If you already have a config file, use File >> Open Config.",)
            self.view.root.title("NoteUtil Configurator - Untitled")
        return "break"

    def on_save(self):
        if self.config_file_path is None:
            return self.on_save_as()
        with open(self.config_file_path, mode="w") as f:
            f.write(self.view.text_editor.get(1.0, tk.END).strip())

    def on_save_as(self):
        file_name = self.config_file_name if self.config_file_name is not None else ""
        file = tk.filedialog.asksaveasfile(defaultextension=".txt",
                                           initialdir=NOTES_DIR, initialfile=file_name, title="Save as",
                                           filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if file:
            self.file_update(file)
            with open(self.config_file_path, mode="w") as f:
                f.write(self.view.text_editor.get(1.0, tk.END).strip())
        return "break"

    def on_compile(self):
        if self.config_file_path is None:
            self.on_save_as()
        else:
            self.on_save()

        try:
            self.noteutil = nu.NoteUtil(self.config_file_path)
            self.quiz = nu.Quiz(self.noteutil)
            self.leitner = nu.Leitner(self.noteutil)
        except (NoteUtilError, QuizError, LeitnerError) as e:
            tkmsgbox.showerror(title="An error occurred compiling your notes", message=e.args[0])
            self.view.status_label.config(text=e.args[0])
            return "break"

        tkmsgbox.showinfo(title="Success!", message="Your file compiled successfully.")
        self.view.status_label.config(text="Your file compiled successfully.")
        self.view.searcher_button.config(state=tk.NORMAL)
        self.view.quizzer_button.config(state=tk.NORMAL)
        self.view.reviewer_button.config(state=tk.NORMAL)
        return "break"

    def on_find(self):
        self.count += 1
        print(self.count)
        return "break"

    def on_replace(self):
        self.count += 1
        print(self.count)
        return "break"

    def on_line_numbers(self):
        self.count += 1
        print(self.count)

    def on_highlight(self):
        self.count += 1
        print(self.count)

    def on_what_config(self):
        webbrowser.open("https://github.com/JJamesWWang/noteutil/blob/master/README.md#Config")

    def on_about(self):
        webbrowser.open("https://github.com/JJamesWWang/noteutil")

    def on_editor(self):
        from editor import EditorView
        toplevel = tk.Toplevel(self.view.root)
        toplevel.geometry("1600x900+160+90")
        EditorView(toplevel, self.noteutil, self.quiz, self.leitner)

    def handle_exit(self):
        self.save_settings()
        option = "ok"
        if self.config_file_path is not None:
            with open(self.config_file_path, mode="r") as f:
                previous_text = f.read()
        else:
            with open("CONFIG_TEMPLATE.txt", mode="r") as f:
                previous_text = f.read()

        if previous_text.strip() != self.view.text_editor.get(1.0, tk.END).strip():
            option = tkmsgbox.askyesnocancel(title="Window closing",
                                             message="Would you like to save before closing?")
        if option == tk.YES:
            self.on_save()
            tkmsgbox.showinfo(title="Success!", message="Saved successfully.")
        if option is not None:
            self.view.clear()
        return option

    def on_searcher(self):
        from searcher import SearcherView
        if self.handle_exit() is not None:
            SearcherView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_quizzer(self):
        from quizzer import QuizzerView
        if self.handle_exit() is not None:
            QuizzerView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_reviewer(self):
        from reviewer import ReviewerView
        if self.handle_exit() is not None:
            ReviewerView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_close(self):
        import sys
        if self.handle_exit() is not None:
            self.view.root.destroy()
            sys.exit()
