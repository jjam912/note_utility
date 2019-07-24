import tkinter as tk
import tkinter.font as tkfont
import noteutil as nu
from editor import Editor
from searcher import Searcher
from quizzer import Quizzer
from reviewer import Reviewer


class ConfiguratorView:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteUtil Configurator")
        self.controller = ConfiguratorController(self)

        self.line_numbers = tk.BooleanVar(value=True)
        self.highlight = tk.BooleanVar(value=True)
        self.menu_bar = None
        self.init_menu_bar()

        self.config_filename = tk.StringVar(value="None")
        self.config_label = None
        self.status_label = None
        self.init_info_labels()

        self.text_editor = None
        self.init_text_editor()

        self.editor_button = None
        self.searcher_button = None
        self.quizzer_button = None
        self.reviewer_button = None
        self.init_actions_frame()

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
        view_menu.add_checkbutton(label="Show line number", variable=self.line_numbers,
                                  command=self.controller.on_line_numbers)
        view_menu.add_checkbutton(label="Highlight current line", variable=self.highlight,
                                  command=self.controller.on_highlight)
        self.menu_bar.add_cascade(menu=view_menu, label="View")

    def init_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        help_menu.add_command(label="What config?", command=self.controller.on_what_config)
        help_menu.add_command(label="About", command=self.controller.on_about)
        self.menu_bar.add_cascade(menu=help_menu, label="Help")

    def init_info_labels(self):
        self.config_label = tk.Label(self.root, text="Your current config file is: " + str(self.config_filename.get()),
                                     padx=10, anchor=tk.W)
        self.status_label = tk.Label(self.root, text="Open a config file or create a new one and then compile it. " +
                                                     "If you already have a config file, use File >> Open Config.",
                                     padx=10, anchor=tk.W)
        self.config_label.pack(side=tk.TOP, padx=30, pady=(10, 0), fill=tk.X)
        self.status_label.pack(side=tk.TOP, padx=30, fill=tk.X)

    def init_text_editor(self):
        self.text_editor = tk.Text(self.root, wrap=tk.NONE, undo=True,
                                   font=tkfont.Font(family="Ubuntu", size=12))
        xscrollbar = tk.Scrollbar(self.text_editor, orient=tk.HORIZONTAL)
        yscrollbar = tk.Scrollbar(self.text_editor, orient=tk.VERTICAL)
        self.text_editor.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        xscrollbar.config(command=self.text_editor.xview)
        yscrollbar.config(command=self.text_editor.yview)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=40, pady=10)
        self.controller.on_new_config()

    def init_actions_frame(self):
        actions_frame = tk.LabelFrame(self.root, text="Choose a method of review:")
        self.editor_button = tk.Button(actions_frame, text="Editor", command=self.controller.on_editor)
        self.searcher_button = tk.Button(actions_frame, text="Searcher", command=self.controller.on_searcher)
        self.quizzer_button = tk.Button(actions_frame, text="Quizzer", command=self.controller.on_quizzer)
        self.reviewer_button = tk.Button(actions_frame, text="Reviewer", command=self.controller.on_reviewer)
        self.editor_button.pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        self.searcher_button.pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        self.quizzer_button.pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        self.reviewer_button.pack(side=tk.LEFT, padx=1, fill=tk.X, expand=True)
        actions_frame.pack(side=tk.TOP, fill=tk.X, padx=40, pady=(0, 10))

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class ConfiguratorController:
    def __init__(self, view):
        self.count = 0
        self.view = view

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
        self.count += 1
        print(self.count)

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
        self.view.clear()
        Editor(self.view.root)

    def on_searcher(self):
        self.view.clear()
        Searcher(self.view.root)

    def on_quizzer(self):
        self.view.clear()
        Quizzer(self.view.root)

    def on_reviewer(self):
        self.view.clear()
        Reviewer(self.view.root)


if __name__ == "__main__":
    gui = tk.Tk()
    app = ConfiguratorView(gui)
    gui.geometry("1600x900+160+90")
    gui.mainloop()
