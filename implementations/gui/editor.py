import os
import tkinter as tk
import tkinter.font as tkfont
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmsgbox
from noteutil.errors import NoteUtilError, QuizError, LeitnerError
import webbrowser


NOTES_DIR = os.path.join(os.getcwd(), "notes")


class EditorView:
    def __init__(self, root, noteutil, quiz, leitner):
        self.root = root
        self.root.title("NoteUtil Editor")

        self.controller = EditorController(self, noteutil, quiz, leitner)

        self.menu_bar = None
        self.init_menu_bar()

        self.line_numbers_text = None
        self.text_editor = None
        self.init_text_editor()

        if noteutil is not None and quiz is not None and leitner is not None:
            with open(noteutil.nu_file, mode="r") as f:
                self.text_editor.insert(tk.END, f.read())

    def init_menu_bar(self):
        self.menu_bar = tk.Menu(self.root, tearoff=False)
        self.init_file_menu()
        self.init_edit_menu()
        self.init_view_menu()
        self.init_tools_menu()
        self.init_help_menu()
        self.root.config(menu=self.menu_bar)

    def init_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="New config", accelerator="Ctrl+N", command=self.controller.on_new_file)
        self.root.bind("<Control-N>", lambda e: self.controller.on_new_file())
        self.root.bind("<Control-n>", lambda e: self.controller.on_new_file())
        file_menu.add_command(label="Open config", accelerator="Ctrl+O", command=self.controller.on_open_file)
        self.root.bind("<Control-O>", lambda e: self.controller.on_open_file())
        self.root.bind("<Control-o>", lambda e: self.controller.on_open_file())
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.controller.on_save)
        self.root.bind("<Control-S>", lambda e: self.controller.on_save())
        self.root.bind("<Control-s>", lambda e: self.controller.on_save())
        file_menu.add_command(label="Save as", accelerator="Ctrl+Shift+S", command=self.controller.on_save_as)
        self.root.bind("<Control-Shift-S>", lambda e: self.controller.on_save_as())
        self.root.bind("<Control-Shift-s>", lambda e: self.controller.on_save_as())
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def init_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=self.controller.on_find)
        self.root.bind("<Control-F>", lambda e: self.controller.on_find())
        self.root.bind("<Control-f>", lambda e: self.controller.on_find())
        edit_menu.add_command(label="Replace", accelerator="Ctrl+R", command=self.controller.on_replace)
        self.root.bind("<Control-R>", lambda e: self.controller.on_replace())
        self.root.bind("<Control-r>", lambda e: self.controller.on_replace())
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def init_view_menu(self):
        view_menu = tk.Menu(self.menu_bar, tearoff=False)
        view_menu.add_checkbutton(label="Show line number", variable=self.controller.line_numbers,
                                  command=self.controller.on_line_numbers)
        view_menu.add_checkbutton(label="Highlight current line", variable=self.controller.highlight,
                                  command=self.controller.on_highlight)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

    def init_tools_menu(self):
        tools_menu = tk.Menu(self.menu_bar, tearoff=False)
        tools_menu.add_command(label="View image link", command=self.controller.on_view_image_link)
        tools_menu.add_command(label="Font selector", command=self.controller.on_font_selector)
        tools_menu.add_command(label="Display LaTeX", command=self.controller.on_display_latex)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

    def init_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        help_menu.add_command(label="About", command=self.controller.on_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def init_text_editor(self):
        text_editor_frame = tk.Frame(self.root)
        self.line_numbers_text = tk.Text(text_editor_frame, width=5, state=tk.DISABLED,
                                         font=tkfont.Font(family="Ubuntu", size=12))
        self.text_editor = tk.Text(text_editor_frame, wrap=tk.WORD, undo=True,
                                   font=tkfont.Font(family="Ubuntu", size=12))
        yscrollbar = tk.Scrollbar(text_editor_frame, orient=tk.VERTICAL, command=self.text_editor.yview)
        self.text_editor.config(yscrollcommand=yscrollbar.set)

        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.line_numbers_text.pack(side=tk.LEFT, fill=tk.Y)
        self.text_editor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        text_editor_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx="1in", pady=("0.25in", 0))

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class EditorController:
    def __init__(self, view, noteutil, quiz, leitner):
        self.count = 0
        self.view = view
        self.noteutil = noteutil
        self.quiz = quiz
        self.leitner = leitner

        self.line_numbers = tk.BooleanVar(value=True)
        self.highlight = tk.BooleanVar(value=True)

    def on_new_file(self):
        self.count += 1
        print(self.count)

    def on_open_file(self):
        self.count += 1
        print(self.count)

    def on_save(self):
        self.count += 1
        print(self.count)

    def on_save_as(self):
        self.count += 1
        print(self.count)

    def on_find(self):
        self.count += 1
        print(self.count)

    def on_replace(self):
        self.count += 1
        print(self.count)

    def on_line_numbers(self):
        self.count += 1
        print(self.count)

    def on_highlight(self):
        self.count += 1
        print(self.count)

    def on_view_image_link(self):
        self.count += 1
        print(self.count)

    def on_font_selector(self):
        self.count += 1
        print(self.count)

    def on_display_latex(self):
        self.count += 1
        print(self.count)

    def on_about(self):
        self.count += 1
        print(self.count)


if __name__ == "__main__":
    gui = tk.Tk()
    app = EditorView(gui, None, None, None)
    gui.geometry("1600x900+160+90")
    gui.mainloop()


