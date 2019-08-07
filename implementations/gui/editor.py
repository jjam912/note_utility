"""GUI for editing NoteUtil Notes, but can be used for general text editing."""
import os
import tkinter as tk
import tkinter.font as tkfont
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmsgbox
import tkinter.simpledialog as tksimpledialog
import json
import webbrowser


NOTES_DIR = os.path.join(os.getcwd(), "notes")
SETTINGS_DIR = os.path.join(os.getcwd(), "settings.json")


class EditorView:
    def __init__(self, root, noteutil=None, quiz=None, leitner=None):
        self.root = root
        self.root.title("NoteUtil Editor - Untitled")

        self.controller = EditorController(self, noteutil, quiz, leitner)

        self.menu_bar = None
        self.init_menu_bar()

        self.line_numbers_text = None
        self.text_editor = None
        self.yscrollbar = None
        self.init_text_editor()

        self.controller.read_settings()
        self.bind_content_change()
        self.controller.update_highlight()
        self.root.protocol("WM_DELETE_WINDOW", self.controller.on_close)

    def init_menu_bar(self):
        self.menu_bar = tk.Menu(self.root, tearoff=False)
        self.init_file_menu()
        self.init_edit_menu()
        self.init_tools_menu()
        self.init_help_menu()
        self.root.config(menu=self.menu_bar)

    def init_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label="New file", accelerator="Ctrl+N", command=self.controller.on_new_file)
        self.root.bind("<Control-N>", lambda e: self.controller.on_new_file())
        self.root.bind("<Control-n>", lambda e: self.controller.on_new_file())
        file_menu.add_command(label="Open file", accelerator="Ctrl+O", command=self.controller.on_open_file)
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
        edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=self.controller.on_find)
        self.root.bind("<Control-F>", lambda e: self.controller.on_find())
        self.root.bind("<Control-f>", lambda e: self.controller.on_find())
        edit_menu.add_command(label="Replace", accelerator="Ctrl+R", command=self.controller.on_replace)
        self.root.bind("<Control-R>", lambda e: self.controller.on_replace())
        self.root.bind("<Control-r>", lambda e: self.controller.on_replace())
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

    def init_tools_menu(self):
        tools_menu = tk.Menu(self.menu_bar, tearoff=False)
        tools_menu.add_command(label="View image link", command=self.init_image_link_view)
        tools_menu.add_command(label="Font selector", command=self.init_font_chooser_view)
        tools_menu.add_command(label="Display LaTeX", command=self.init_display_latex_view)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

    def init_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        help_menu.add_command(label="About", command=self.controller.on_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def init_text_editor(self):
        text_editor_frame = tk.Frame(self.root)
        self.line_numbers_text = tk.Text(text_editor_frame, width=5, state=tk.DISABLED,
                                         font=tkfont.Font(family="Ubuntu", size=12))
        self.text_editor = tk.Text(text_editor_frame, wrap=tk.NONE, undo=True,
                                   font=tkfont.Font(family="Ubuntu", size=12))

        def scroll_y(*args):
            self.text_editor.yview(*args)
            self.line_numbers_text.yview(*args)

        def on_textscroll(*args):
            self.yscrollbar.set(*args)
            scroll_y("moveto", args[0])

        xscrollbar = tk.Scrollbar(text_editor_frame, orient=tk.HORIZONTAL, command=self.text_editor.xview)
        self.yscrollbar = tk.Scrollbar(text_editor_frame, orient=tk.VERTICAL, command=scroll_y)
        self.text_editor.config(xscrollcommand=xscrollbar.set, yscrollcommand=on_textscroll)

        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.line_numbers_text.pack(side=tk.LEFT, fill=tk.Y)
        self.text_editor.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        text_editor_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx="1in", pady=("0.25in", 0))
        self.text_editor.tag_config("highlight", background="light gray")

    def init_image_link_view(self):
        from PIL import Image
        import requests
        from io import BytesIO

        url = tksimpledialog.askstring(parent=self.root, title="Image", prompt="Enter the image link.")
        if url:
            toplevel = tk.Toplevel(self.root)
            toplevel.transient(self.root)
            toplevel.title("Image link")
            toplevel.resizable(False, False)
            tk.Label(toplevel, text="Image load failed.").grid(row=0, column=0)

            # Thanks to https://stackoverflow.com/questions/7391945/how-do-i-read-image-data-from-a-url-in-python
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.save("temp.png")

            image = tk.PhotoImage(file="temp.png")
            tk.Label(toplevel, image=image).grid(row=0, column=0)
            toplevel.image = image

    def init_font_chooser_view(self):
        pass

    def init_display_latex_view(self):
        from sympy import preview

        latex = tksimpledialog.askstring(parent=self.root, title="LaTeX", prompt="Enter your latex code.")
        if latex:
            toplevel = tk.Toplevel(self.root)
            toplevel.transient(self.root)
            toplevel.title("LaTeX")
            toplevel.resizable(False, False)
            fail_label = tk.Label(toplevel, text="LaTeX load failed.")
            fail_label.grid(row=0, column=0)

            preview(latex, viewer="file", filename="temp.png")
            image = tk.PhotoImage(file="temp.png")
            tk.Label(toplevel, image=image).grid(row=0, column=0)
            toplevel.image = image
            fail_label.destroy()

    def bind_content_change(self):
        self.text_editor.bind("<Any-KeyPress>", lambda e: self.controller.on_content_change(), add=True)
        self.text_editor.bind("<<Cut>>", lambda e: self.controller.on_content_change(), add=True)
        self.text_editor.bind("<<Paste>>", lambda e: self.controller.on_content_change(), add=True)
        self.text_editor.bind("<<Undo>>", lambda e: self.controller.on_content_change(), add=True)
        self.text_editor.bind("<<Redo>>", lambda e: self.controller.on_content_change(), add=True)

    def unbind_all(self):
        self.root.unbind("<Control-N>")
        self.root.unbind("<Control-N>")
        self.root.unbind("<Control-O>")
        self.root.unbind("<Control-o>")
        self.root.unbind("<Control-S>")
        self.root.unbind("<Control-s>")
        self.root.unbind("<Control-Shift-S>")
        self.root.unbind("<Control-Shift-s>")
        self.root.unbind("<Control-F>")
        self.root.unbind("<Control-f>")
        self.root.unbind("<Control-R>")
        self.root.unbind("<Control-r>")
        self.root.unbind("<Control-I>")
        self.root.unbind("<Control-i>")
        self.root.unbind("<Control-L>")
        self.root.unbind("<Control-l>")

    def clear(self):
        self.unbind_all()
        for widget in self.root.winfo_children():
            widget.destroy()


class EditorController:
    def __init__(self, view, noteutil, quiz, leitner):
        self.count = 0
        self.view = view
        self.noteutil = noteutil
        self.quiz = quiz
        self.leitner = leitner

        self.file_path = None
        self.file_name = None

        self.settings = {}

    def read_settings(self):
        with open(SETTINGS_DIR, mode="r") as f:
            try:
                program_settings = json.loads(f.read())
            except json.JSONDecodeError:
                program_settings = {}
            self.settings = program_settings.get("editor", {})
        if self.settings:
            self.file_path = self.settings.get("file_path", None)
            self.file_name = self.settings.get("file_name", None)
            if self.file_path is not None:
                with open(self.file_path, mode="r") as f:
                    self.on_open_file(f)

    def save_settings(self):
        self.settings["file_path"] = self.file_path
        self.settings["file_name"] = self.file_name

        with open(SETTINGS_DIR, mode="r") as f:
            try:
                program_settings = json.loads(f.read())
            except json.JSONDecodeError:
                program_settings = {}
        program_settings["editor"] = self.settings

        with open(SETTINGS_DIR, mode="w") as f:
            f.write(json.dumps(program_settings))

    def on_new_file(self):
        self.file_update()
        self.view.text_editor.delete(1.0, tk.END)
        return "break"

    def on_open_file(self, file=None):
        if file is None:
            file = tkfiledialog.askopenfile(parent=self.view.root, defaultextension=".txt", initialdir=NOTES_DIR,
                                            title="Open file",
                                            filetypes=[("NoteUtil Notes", "*.nu"), ("Text Documents", "*.txt"),
                                                       ("Markdown Documents", "*.md"), ("All Files", "*.*")])
        if file:
            self.view.text_editor.delete(1.0, tk.END)
            self.view.text_editor.insert(tk.END, file.read())
            self.file_update(file)
        return "break"

    def file_update(self, file=None):
        if file:
            self.file_name = os.path.basename(file.name)
            self.file_path = file.name
            self.view.root.title("NoteUtil Editor - " + self.file_name)
        else:
            self.file_name = None
            self.file_path = None
            self.view.root.title("NoteUtil Editor - Untitled")
        return "break"

    def on_save(self):
        if self.file_path is None:
            return self.on_save_as()
        with open(self.file_path, mode="w") as f:
            f.write(self.view.text_editor.get(1.0, tk.END).strip())

    def on_save_as(self):
        file_name = self.file_name if self.file_name is not None else ""
        file = tk.filedialog.asksaveasfile(defaultextension=".txt",
                                           initialdir=NOTES_DIR, initialfile=file_name, title="Save as",
                                           filetypes=[("NoteUtil Notes", "*.nu"), ("Text Documents", "*.txt"),
                                                      ("Markdown Documents", "*.md"), ("All Files", "*.*")])
        if file:
            self.file_update(file)
            with open(self.file_path, mode="w") as f:
                f.write(self.view.text_editor.get(1.0, tk.END).strip())
        return "break"

    def on_find(self):
        self.count += 1
        print(self.count)

    def on_replace(self):
        self.count += 1
        print(self.count)

    def on_about(self):
        webbrowser.open("https://github.com/JJamesWWang/noteutil")

    def on_content_change(self):
        self.set_line_numbers()

    def set_line_numbers(self):
        actual_line_numbers = ""
        row, col = self.view.text_editor.index(tk.END).split(".")
        for i in range(1, int(row) + 1):
            actual_line_numbers += str(i) + "\n"
        actual_line_numbers = actual_line_numbers[:-1]
        self.view.line_numbers_text.config(state=tk.NORMAL)
        self.view.line_numbers_text.delete(1.0, tk.END)
        self.view.line_numbers_text.insert(tk.END, actual_line_numbers)
        self.view.line_numbers_text.config(state=tk.DISABLED)
        self.view.line_numbers_text.yview(tk.MOVETO, self.view.yscrollbar.get()[0])

    def update_highlight(self, interval=100):
        self.view.text_editor.tag_remove("highlight", 1.0, tk.END)
        self.view.text_editor.tag_add("highlight", "insert linestart", "insert lineend+1c")
        self.view.text_editor.after(interval, self.update_highlight)

    def handle_exit(self):
        self.save_settings()
        option = "ok"
        previous_text = ""
        if self.file_path is not None:
            with open(self.file_path, mode="r") as f:
                previous_text = f.read()
        if previous_text.strip() != self.view.text_editor.get(1.0, tk.END).strip():
            option = tkmsgbox.askyesnocancel(parent=self.view.root, title="Window closing",
                                             message="Would you like to save before closing?")
            if option == tk.YES:
                self.on_save()
                tkmsgbox.showinfo(parent=self.view.root, title="Success!", message="Saved successfully.")
        if option is not None:
            self.view.clear()
        return option

    def on_close(self):
        if self.handle_exit() is not None:
            self.view.root.destroy()
