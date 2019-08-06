"""GUI for quizzing through NoteUtil.Quiz."""
import os
import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as tkmsgbox
import tkinter.simpledialog as tksimpledialog
import tkinter.ttk as ttk
import noteutil as nu
import json
import webbrowser


SETTINGS_DIR = os.path.join(os.getcwd(), "settings.json")


class QuizzerView:
    def __init__(self, root, noteutil, quiz, leitner):
        self.root = root
        self.root.title("NoteUtil Quizzer")
        self.controller = QuizzerController(self, noteutil, quiz, leitner)

        self.menu_bar = None
        self.reveal_label = None
        self.init_menu_bar()

        self.division_combobox = None
        self.generate_button = None
        self.init_top_frame()

        self.question_text = None
        self.init_question_text()

        self.answer_text = None
        self.init_answer_text()

        self.reveal_button = None
        self.correct_button = None
        self.incorrect_button = None
        self.init_button_frame()

        self.root.protocol("WM_DELETE_WINDOW", self.controller.on_close)

    def init_menu_bar(self):
        self.menu_bar = tk.Menu(self.root, tearoff=False)
        self.init_option_menu()
        self.init_notes_menu()
        self.init_navigate_menu()
        self.init_tools_menu()
        self.init_settings_menu()
        self.init_help_menu()
        self.root.config(menu=self.menu_bar)

    def init_option_menu(self):
        options_menu = tk.Menu(self.menu_bar, tearoff=False)

        options_menu.add_command(label="Generate", accelerator="Ctrl+G", command=self.controller.on_generate)
        options_menu.add_separator()

        options_menu.add_command(label="Reveal", accelerator="H", command=self.controller.on_reveal)
        self.root.bind("<H>", lambda e: self.controller.on_reveal())
        self.root.bind("<h>", lambda e: self.controller.on_reveal())
        options_menu.add_command(label="Add to correct", accelerator="J", command=self.controller.on_add_correct)
        self.root.bind("<J>", lambda e: self.controller.on_add_correct())
        self.root.bind("<j>", lambda e: self.controller.on_add_correct())
        options_menu.add_command(label="Add to incorrect", accelerator="K", command=self.controller.on_add_incorrect)
        self.root.bind("<K>", lambda e: self.controller.on_add_incorrect())
        self.root.bind("<k>", lambda e: self.controller.on_add_incorrect())
        options_menu.add_separator()

        options_menu.add_command(label="Load", accelerator="Ctrl+O", command=self.controller.on_load)
        self.root.bind("<Control-O>", lambda e: self.controller.on_load())
        self.root.bind("<Control-o>", lambda e: self.controller.on_load())
        options_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.controller.on_save)
        self.root.bind("<Control-S>", lambda e: self.controller.on_save())
        self.root.bind("<Control-s>", lambda e: self.controller.on_save())
        options_menu.add_command(label="Reset", accelerator="Ctrl+R", command=self.controller.on_reset)
        self.root.bind("<Control-R>", lambda e: self.controller.on_reset())
        self.root.bind("<Control-r>", lambda e: self.controller.on_reset())
        self.menu_bar.add_cascade(label="Options", menu=options_menu)

    def init_notes_menu(self):
        notes_menu = tk.Menu(self.menu_bar, tearoff=False)
        notes_menu.add_command(label="View correct", command=self.controller.on_view_correct)
        notes_menu.add_command(label="View incorrect", command=self.controller.on_view_incorrect)
        notes_menu.add_command(label="View unmarked", command=self.controller.on_view_unmarked)
        notes_menu.add_separator()

        notes_menu.add_command(label="Edit current note", accelerator="Ctrl+E", command=self.controller.on_edit_note)
        self.root.bind("<Control-E>", lambda e: self.controller.on_edit_note())
        self.root.bind("<Control-e>", lambda e: self.controller.on_edit_note())
        notes_menu.add_command(label="Quick search", accelerator="Ctrl+F", command=self.init_quick_search_view)
        self.root.bind("<Control-F>", lambda e: self.init_quick_search_view)
        self.root.bind("<Control-f>", lambda e: self.init_quick_search_view)
        self.menu_bar.add_cascade(label="Notes", menu=notes_menu)

    def init_navigate_menu(self):
        navigate_menu = tk.Menu(self.menu_bar, tearoff=False)
        navigate_menu.add_command(label="Go to configurator", command=self.controller.on_to_configurator)
        navigate_menu.add_command(label="Go to editor", command=self.controller.on_to_editor)
        navigate_menu.add_command(label="Go to searcher", command=self.controller.on_to_searcher)
        navigate_menu.add_command(label="Go to reviewer", command=self.controller.on_to_reviewer)
        self.menu_bar.add_cascade(label="Navigate", menu=navigate_menu)

    def init_tools_menu(self):
        tools_menu = tk.Menu(self.menu_bar, tearoff=False)
        tools_menu.add_command(label="View image link", accelerator="Ctrl+I", command=self.init_image_link_view)
        self.root.bind("<Control-I>", lambda e: self.init_image_link_view())
        self.root.bind("<Control-i>", lambda e: self.init_image_link_view())
        tools_menu.add_command(label="Display LaTeX", accelerator="Ctrl+L", command=self.init_display_latex_view)
        self.root.bind("<Control-L>", lambda e: self.init_display_latex_view())
        self.root.bind("<Control-l>", lambda e: self.init_display_latex_view())
        tools_menu.add_command(label="Font selector", command=self.init_font_chooser_view)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

    def init_settings_menu(self):
        settings_menu = tk.Menu(self.menu_bar, tearoff=False)
        settings_menu.add_checkbutton(label="Randomize terms", variable=self.controller.random)
        settings_menu.add_checkbutton(label="Display term first", variable=self.controller.term_first)
        settings_menu.add_checkbutton(label="Include extensions", variable=self.controller.include_extensions)
        settings_menu.add_command(label="Set term format", command=self.init_set_term_format_view)
        settings_menu.add_command(label="Set definition format", command=self.init_set_definition_format_view)
        settings_menu.add_command(label="Set extension format", command=self.init_set_extension_format_view)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)

    def init_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        help_menu.add_command(label="What is this?", command=self.controller.on_what_is_this)
        help_menu.add_command(label="About", command=self.controller.on_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def init_top_frame(self):
        top_frame = tk.Frame(self.root)
        self.division_combobox = ttk.Combobox(top_frame, justify=tk.LEFT, state="readonly", takefocus=False,
                                              postcommand=self.controller.on_division_prompt,
                                              textvariable=self.controller.division)
        self.division_combobox.pack(side=tk.LEFT, padx=10, expand=True, anchor=tk.E)

        self.generate_button = tk.Button(top_frame, text="Generate", state=tk.DISABLED,
                                         command=self.controller.on_generate)
        self.generate_button.pack(side=tk.LEFT, padx=(0, 10), expand=True, anchor=tk.W)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))

    def init_question_text(self):
        question_frame = tk.LabelFrame(self.root, text="Question", padx=10, pady=10, labelanchor=tk.N)
        self.question_text = tk.Text(question_frame, wrap=tk.WORD, width=1, height=1,
                                     font=tkfont.Font(family="Ubuntu", size=12))
        yscrollbar = tk.Scrollbar(question_frame, orient=tk.VERTICAL, takefocus=False, command=self.question_text.yview)
        self.question_text.config(yscrollcommand=yscrollbar.set)
        self.question_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        question_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)
        self.question_text.insert(tk.END, "The question will be asked here.")
        self.question_text.config(state=tk.DISABLED)

    def init_answer_text(self):
        answer_frame = tk.LabelFrame(self.root, text="Answer", padx=10, pady=10, labelanchor=tk.N)
        self.answer_text = tk.Text(answer_frame, wrap=tk.WORD, width=1, height=1,
                                   font=tkfont.Font(family="Ubuntu", size=12))
        yscrollbar = tk.Scrollbar(answer_frame, orient=tk.VERTICAL, takefocus=False, command=self.answer_text.yview)
        self.answer_text.config(yscrollcommand=yscrollbar.set)
        self.answer_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        answer_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, expand=True)
        self.answer_text.insert(tk.END, "The answer will be displayed here.")
        self.answer_text.config(state=tk.DISABLED)

    def init_button_frame(self):
        button_frame = tk.Frame(self.root)
        self.correct_button = tk.Button(button_frame, text="Correct", bd=5, command=self.controller.on_add_correct)
        self.correct_button.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.X, expand=True)
        self.reveal_button = tk.Button(button_frame, textvariable=self.controller.reveal, bd=5,
                                       command=self.controller.on_reveal)
        self.reveal_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.incorrect_button = tk.Button(button_frame, text="Incorrect", bd=5,
                                          command=self.controller.on_add_incorrect)
        self.incorrect_button.pack(side=tk.LEFT, padx=(0, 10), pady=10, fill=tk.X, expand=True)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        # Views generated by Menu commands

    def init_notes_view(self, notes_description):
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Your Notes")
        toplevel.transient(self.root)

        toplevel.notes_text = tk.Text(toplevel, wrap=tk.NONE)
        toplevel.notes_text.insert(tk.END, notes_description)
        xscrollbar = tk.Scrollbar(toplevel, orient=tk.HORIZONTAL, command=toplevel.notes_text.xview)
        yscrollbar = tk.Scrollbar(toplevel, orient=tk.VERTICAL, command=toplevel.notes_text.yview)
        toplevel.notes_text.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, state=tk.DISABLED)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        toplevel.notes_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    def init_edit_note_view(self):
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Edit Note")
        toplevel.transient(self.root)
        tk.Label(toplevel, text="Displayed below is the raw content of the current note.",
                 font=tkfont.Font(family="Ubuntu", size=12)).grid(row=0, column=0, ipady=5)

        toplevel.text_editor = tk.Text(toplevel, wrap=tk.WORD, font=tkfont.Font(family="Ubuntu", size=12),
                                       width=52, height=5)
        yscrollbar = tk.Scrollbar(toplevel, orient=tk.VERTICAL, command=toplevel.text_editor.yview)
        toplevel.text_editor.config(yscrollcommand=yscrollbar.set)

        yscrollbar.grid(row=1, column=2, padx=(0, 10), sticky=tk.NS)
        toplevel.text_editor.insert(tk.END, self.controller.current_note.rcontent)
        toplevel.text_editor.grid(row=1, column=0, columnspan=2, padx=(10, 0), sticky=tk.NSEW)

        tk.Button(toplevel, text="Edit", command=lambda: self.controller.edit_note(
            toplevel)).grid(row=0, column=1, columnspan=2, padx=(5, 10), sticky=tk.EW)

    def init_quick_search_view(self):
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Quick search")
        toplevel.transient(self.root)
        toplevel.geometry("800x450")

        def is_int(string):
            try:
                int(string)
                return True
            except ValueError:
                return False

        toplevel.query = tk.StringVar()
        query_entry = tk.Entry(toplevel, width=52, textvariable=toplevel.query, validate="key")
        search_icon = tk.PhotoImage(file="icons/magnifying_glass.png")

        def on_content():
            query_entry.delete(0, tk.END)
            query_entry.config(validatecommand=True)

        def on_nindex():
            query_entry.delete(0, tk.END)
            query_entry.config(validatecommand=(toplevel.register(is_int), "%P"))

        options_frame = tk.LabelFrame(toplevel, text="Search by:")
        toplevel.search_option = tk.StringVar(value="content")
        content_radiobutton = tk.Radiobutton(options_frame, text="Content", value="content", anchor=tk.W,
                                             variable=toplevel.search_option, command=on_content)
        nindex_radiobutton = tk.Radiobutton(options_frame, text="Note index", value="nindex", anchor=tk.W,
                                            variable=toplevel.search_option, command=on_nindex)
        content_radiobutton.pack(side=tk.TOP)
        nindex_radiobutton.pack(side=tk.TOP)
        toplevel.results = tk.StringVar()

        list_frame = tk.Frame(toplevel)
        toplevel.results_list = tk.Listbox(list_frame, activestyle="dotbox", listvariable=toplevel.results,
                                           selectmode=tk.SINGLE)
        yscrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=toplevel.results_list.yview)
        xscrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=toplevel.results_list.xview)
        toplevel.results_list.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        search_button = tk.Button(query_entry, image=search_icon,
                                  command=lambda: self.controller.quick_search(toplevel))
        search_button.image = search_icon
        query_entry.bind("<Return>", lambda e: self.controller.quick_search(toplevel))

        options_frame.pack(side=tk.TOP, fill=tk.X)
        search_button.pack(side=tk.RIGHT)
        query_entry.pack(side=tk.TOP, fill=tk.X)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        toplevel.results_list.pack(fill=tk.BOTH, expand=True)
        list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def init_image_link_view(self):
        from PIL import Image
        import requests
        from io import BytesIO

        url = tksimpledialog.askstring(title="Image", prompt="Enter the image link.")
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

        latex = tksimpledialog.askstring(title="LaTeX", prompt="Enter your latex code.")
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

    def init_set_term_format_view(self):
        toplevel = tk.Toplevel(self.root)
        toplevel.transient(self.root)
        toplevel.title("Set term format")
        toplevel.resizable(True, False)

        tk.Label(toplevel, text=r"Use {0} for term, {1} for definition, {2} for separator, {3} for note index, "
                                "\n" + r"\n for newline, and \t for tab" + "\n").pack(side=tk.TOP)
        tk.Label(toplevel, text="Term format 1 (Used when the term is displayed first):").pack(side=tk.TOP)
        toplevel.new_term_format1 = tk.StringVar()
        tk.Entry(toplevel, textvariable=toplevel.new_term_format1).pack(side=tk.TOP, expand=True, fill=tk.X)
        tk.Label(toplevel, text="Term format 2 (Used when the term is displayed second):").pack(side=tk.TOP)
        toplevel.new_term_format2 = tk.StringVar()
        tk.Entry(toplevel, textvariable=toplevel.new_term_format2).pack(side=tk.TOP, expand=True, fill=tk.X)
        tk.Button(toplevel, text="Save", command=lambda: self.controller.on_save_term_formats(
            toplevel)).pack(side=tk.TOP, fill=tk.X, expand=True)

    def init_set_definition_format_view(self):
        toplevel = tk.Toplevel(self.root)
        toplevel.transient(self.root)
        toplevel.title("Set definition format")
        toplevel.resizable(True, False)

        tk.Label(toplevel, text=r"Use {0} for term, {1} for definition, {2} for separator, {3} for note index, "
                                "\n" + r"\n for newline, and \t for tab" + "\n").pack(side=tk.TOP)
        tk.Label(toplevel, text="Definition format 1 (Used when the definition is displayed first):"
                 ).pack(side=tk.TOP)
        toplevel.new_definition_format1 = tk.StringVar()
        tk.Entry(toplevel, textvariable=toplevel.new_definition_format1).pack(side=tk.TOP, expand=True, fill=tk.X)
        tk.Label(toplevel, text="Definition format 2 (Used when the definition is displayed second):"
                 ).pack(side=tk.TOP)
        toplevel.new_definition_format2 = tk.StringVar()
        tk.Entry(toplevel, textvariable=toplevel.new_definition_format2).pack(side=tk.TOP, expand=True, fill=tk.X)
        tk.Button(toplevel, text="Save", command=lambda: self.controller.on_save_definition_formats(
            toplevel)).pack(side=tk.TOP, fill=tk.X, expand=True)

    def init_set_extension_format_view(self):
        toplevel = tk.Toplevel(self.root)
        toplevel.transient(self.root)
        toplevel.title("Set extension format")
        toplevel.resizable(True, False)

        tk.Label(toplevel, text="Please select an extension:").pack(side=tk.TOP)

        toplevel.extension_name = tk.StringVar()
        toplevel.extension_name_combobox = ttk.Combobox(toplevel, justify=tk.LEFT,
                                                        postcommand=lambda:
                                                        self.controller.on_extension_name_prompt(toplevel),
                                                        textvariable=toplevel.extension_name)
        toplevel.extension_name_combobox.pack(side=tk.TOP, fill=tk.X, expand=True)
        tk.Label(toplevel,
                 text=r"Use {0} for extension_name, {1} for content, \n for newline, and \t for tab.").pack(
            side=tk.TOP)
        toplevel.extension_format = tk.StringVar()
        tk.Entry(toplevel, textvariable=toplevel.extension_format).pack(side=tk.TOP, expand=True, fill=tk.X)
        tk.Label(toplevel, text="Show with:").pack(side=tk.TOP)
        toplevel.extension_first = tk.IntVar(value=-1)
        radio_button_frame = tk.Frame(toplevel)
        tk.Radiobutton(radio_button_frame, text="Question", value=1,
                       variable=toplevel.extension_first).pack(side=tk.LEFT)
        tk.Radiobutton(radio_button_frame, text="Answer", value=0,
                       variable=toplevel.extension_first).pack(side=tk.LEFT)
        radio_button_frame.pack(side=tk.TOP)
        tk.Button(toplevel, text="Save", command=lambda: self.controller.on_save_extension_format(
            toplevel)).pack(side=tk.TOP, fill=tk.X, expand=True)

    def unbind_all(self):
        self.root.unbind("<Control-G>")
        self.root.unbind("<Control-g>")
        self.root.unbind("<H>")
        self.root.unbind("<h>")
        self.root.unbind("<J>")
        self.root.unbind("<j>")
        self.root.unbind("<K>")
        self.root.unbind("<k>")
        self.root.unbind("<L>")
        self.root.unbind("<l>")
        self.root.unbind("<Control-O>")
        self.root.unbind("<Control-o>")
        self.root.unbind("<Control-S>")
        self.root.unbind("<Control-s>")
        self.root.unbind("<Control-R>")
        self.root.unbind("<Control-r>")
        self.root.unbind("<Control-E>")
        self.root.unbind("<Control-e>")
        self.root.unbind("<Control-F>")
        self.root.unbind("<Control-f>")
        self.root.unbind("<Control-I>")
        self.root.unbind("<Control-i>")
        self.root.unbind("<Control-L>")
        self.root.unbind("<Control-l>")

    def clear(self):
        self.controller.save_settings()
        self.unbind_all()
        for widget in self.root.winfo_children():
            widget.destroy()


class QuizzerController:
    def __init__(self, view, noteutil, quiz, leitner):
        self.view = view
        self.noteutil = noteutil
        self.quiz = quiz
        self.leitner = leitner
        self.division = tk.StringVar(value="Select a division:")
        self.reveal = tk.StringVar(value="Reveal")

        self.current_note = None
        self.random = tk.BooleanVar(value=True)
        self.term_first = tk.BooleanVar(value=True)
        self.term_format1 = tk.StringVar(value="Define the term: {0}")
        self.term_format2 = tk.StringVar(value="The term is: {0}\nNote Index: {3}")
        self.definition_format1 = tk.StringVar(value="Guess the term: {1}")
        self.definition_format2 = tk.StringVar(value="The definition is: {1}\nNote Index: {3}")

        self.include_extensions = tk.BooleanVar(value=True)
        self.extension_format = {}
        self.extension_first = {}
        for ext_name in self.noteutil.extension_names:
            self.extension_format[ext_name] = "\n{0}: {1}"
            self.extension_first[ext_name] = False

        self.settings = {}

    def read_settings(self):
        with open(SETTINGS_DIR, mode="r") as f:
            try:
                program_settings = json.loads(f.read())
            except json.JSONDecodeError:
                program_settings = {}
            self.settings = program_settings.get("quizzer", {})
        if self.settings:
            self.random.set(self.settings["random"])
            self.term_first.set(self.settings["term_first"])
            self.term_format1.set(self.settings["term_format1"])
            self.term_format2.set(self.settings["term_format2"])
            self.definition_format1.set(self.settings["definition_format1"])
            self.definition_format2.set(self.settings["definition_format2"])
            self.include_extensions.set(self.settings["include_extensions"])
            self.extension_format = self.settings["extension_format"]
            self.extension_first = self.settings["extension_first"]

    def save_settings(self):
        self.settings["random"] = self.random.get()
        self.settings["term_first"] = self.term_first.get()
        self.settings["term_format1"] = self.term_format1.get()
        self.settings["term_format2"] = self.term_format2.get()
        self.settings["definition_format1"] = self.definition_format1.get()
        self.settings["definition_format2"] = self.definition_format2.get()
        self.settings["include_extensions"] = self.include_extensions.get()
        self.settings["extension_format"] = self.extension_format
        self.settings["extension_first"] = self.extension_first

        with open(SETTINGS_DIR, mode="r") as f:
            try:
                program_settings = json.loads(f.read())
            except json.JSONDecodeError:
                program_settings = {}
        program_settings["quizzer"] = self.settings

        with open(SETTINGS_DIR, mode="w") as f:
            f.write(json.dumps(program_settings))

    def on_division_prompt(self):
        self.division.set("")
        self.view.generate_button.config(state=tk.NORMAL)
        self.view.menu_bar.winfo_children()[0].entryconfigure(0, state=tk.NORMAL)
        self.view.root.bind("<Control-G>", lambda e: self.on_generate())
        self.view.root.bind("<Control-g>", lambda e: self.on_generate())
        self.view.division_combobox.config(values=list(map(lambda n: n.heading_name, self.noteutil.heading_order)))

    def format_question(self, note, term_format):
        question = term_format.get().format(note.term, note.definition, note.separator, note.nindex)
        if self.include_extensions.get():
            for extension in note.extensions:
                if self.extension_first[extension.name]:
                    question += self.extension_format[extension.name].format(
                        extension.name, extension.content)
        self.view.question_text.config(state=tk.NORMAL)
        self.view.question_text.delete(1.0, tk.END)
        self.view.question_text.insert(tk.END, question)
        self.view.question_text.config(state=tk.DISABLED)

    def format_answer(self, note, definition_format):
        answer = definition_format.get().format(note.term, note.definition, note.separator, note.nindex)
        if self.include_extensions.get():
            for extension in note.extensions:
                if not self.extension_first[extension.name]:
                    answer += self.extension_format[extension.name].format(
                        extension.name, extension.content)
        self.view.answer_text.config(state=tk.NORMAL)
        self.view.answer_text.delete(1.0, tk.END)
        self.view.answer_text.insert(tk.END, answer)
        self.view.answer_text.config(state=tk.DISABLED)

    def on_generate(self):
        self.reveal.set("Reveal")
        option_menu = self.view.menu_bar.winfo_children()[0]
        option_menu.entryconfigure(2, label="Reveal")
        option_menu.entryconfigure(2, accelerator="H")
        self.view.root.unbind("<L>")
        self.view.root.unbind("<l>")
        self.view.root.bind("<H>", lambda e: self.on_reveal())
        self.view.root.bind("<h>", lambda e: self.on_reveal())
        self.view.question_text.tag_add(tk.SEL, 1.0, 1.1)       # Removes highlight from Combobox

        try:
            self.quiz.select_pairs(self.division.get())
        except (nu.DivisionNotFound, nu.HeadingExpected) as ex:
            return tkmsgbox.showerror(title="Error generating quiz", message=ex.args[0])

        for note in self.quiz.generate(randomize=self.random.get()):
            if self.term_first.get():
                self.format_question(note, self.term_format1)
            else:
                self.format_question(note, self.definition_format1)
            self.current_note = None
            self.view.reveal_button.wait_variable(self.reveal)
            if self.term_first.get():
                self.format_answer(note, self.definition_format2)
            else:
                self.format_answer(note, self.term_format2)
            self.current_note = note
            self.view.reveal_button.wait_variable(self.reveal)

        self.current_note = None
        self.quiz.save()
        tkmsgbox.showinfo(title="Complete!", message="All pairs have been cycled.\n"
                                                     "Your progress has been saved.")

    def on_reveal(self):
        option_menu = self.view.menu_bar.winfo_children()[0]
        if self.reveal.get() == "Reveal":
            self.reveal.set("Continue")
            option_menu.entryconfigure(2, label="Continue")
            option_menu.entryconfigure(2, accelerator="L")
            self.view.root.unbind("<H>")
            self.view.root.unbind("<h>")
            self.view.root.bind("<L>", lambda e: self.on_reveal())
            self.view.root.bind("<l>", lambda e: self.on_reveal())
        else:
            self.reveal.set("Reveal")
            option_menu.entryconfigure(2, label="Reveal")
            option_menu.entryconfigure(2, accelerator="H")
            self.view.root.unbind("<L>")
            self.view.root.unbind("<l>")
            self.view.root.bind("<H>", lambda e: self.on_reveal())
            self.view.root.bind("<h>", lambda e: self.on_reveal())

    def on_add_correct(self):
        if self.current_note is not None:
            self.quiz.append(self.current_note, correct=True)
            self.on_reveal()

    def on_add_incorrect(self):
        if self.current_note is not None:
            self.quiz.append(self.current_note, correct=False)
            self.on_reveal()

    def on_view_correct(self):
        notes_description = ""
        for note in self.quiz.correct:
            notes_description += note.rcontent + "\n"
        self.view.init_notes_view(notes_description)

    def on_view_incorrect(self):
        notes_description = ""
        for note in self.quiz.incorrect:
            notes_description += note.rcontent + "\n"
        self.view.init_notes_view(notes_description)

    def on_view_unmarked(self):
        notes_description = ""
        for note in self.quiz.unmarked:
            notes_description += note.rcontent + "\n"
        self.view.init_notes_view(notes_description)

    def on_load(self):
        if tkmsgbox.askyesno(title="Load?", message="Would you like to load your previous save?\n"
                                                    "This will reset any unsaved progress."):
            self.quiz.load()
            self.view.answer_text.config(state=tk.NORMAL)
            self.view.answer_text.delete(1.0, tk.END)
            self.view.answer_text.insert(tk.END, "Your previous save was loaded.")
            self.view.answer_text.config(state=tk.DISABLED)
            self.on_generate()

    def on_save(self):
        self.quiz.save()
        self.view.answer_text.config(state=tk.NORMAL)
        self.view.answer_text.delete(1.0, tk.END)
        self.view.answer_text.insert(tk.END, "Your progress was saved.")
        self.view.answer_text.config(state=tk.DISABLED)
        self.on_generate()

    def on_reset(self):
        if tkmsgbox.askyesno(title="Reset?", message="Are you sure you want to reset?\n"
                                                     "This will reset all of your notes to unmarked."):
            self.quiz.reset()
            self.view.answer_text.config(state=tk.NORMAL)
            self.view.answer_text.delete(1.0, tk.END)
            self.view.answer_text.insert(tk.END, "Your progress was reset.")
            self.view.answer_text.config(state=tk.DISABLED)
            self.on_generate()

    def edit_note(self, view):
        try:
            self.noteutil.edit(self.current_note.nindex, view.text_editor.get(1.0, tk.END))
            self.quiz.refresh(self.noteutil)
            view.destroy()
            self.on_generate()
        except nu.NoteError as e:
            tkmsgbox.showerror("Failed edit", message=e.args[0])

    def on_edit_note(self):
        if self.current_note is not None:
            self.view.init_edit_note_view()
        else:
            tkmsgbox.showerror(title="Error editing Note", message="There either is no current note or you have to "
                                                                   "reveal the current note before editing it.")

    def quick_search(self, view):
        view.results_list.delete(0, tk.END)
        if view.search_option.get() == "content":
            notes = self.noteutil.get_list(content=view.query.get(), compare=nu.CompareOptions.SIMIN)
        else:
            notes = self.noteutil.get_list(nindex=int(view.query.get()))
        if notes is not None:
            view.results_list.insert(tk.END, *list(map(lambda n: n.rcontent, notes)))
        else:
            tkmsgbox.showinfo(title="Nothing", message="No results found.")

    def on_to_configurator(self):
        from configurator import ConfiguratorView
        self.quiz.save()
        self.view.clear()
        ConfiguratorView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_to_editor(self):
        from main import Main
        from editor import EditorView
        toplevel = Main()
        toplevel.geometry("1600x900+160+90")
        EditorView(toplevel, self.noteutil, self.quiz, self.leitner)
        toplevel.mainloop()

    def on_to_searcher(self):
        from searcher import SearcherView
        self.quiz.save()
        self.view.clear()
        SearcherView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_to_reviewer(self):
        from reviewer import ReviewerView
        self.quiz.save()
        self.view.clear()
        ReviewerView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_save_term_formats(self, view):
        try:
            self.term_format1 = view.new_term_format1
            self.term_format2 = view.new_term_format2

        except ValueError:
            tkmsgbox.showerror(title="Error saving term format", message="Something went wrong "
                                                                         "formatting the term.")
        if view.new_term_format1.get() != "":
            view.new_term_format1.set(view.new_term_format1.get().replace("\\n", "\n"))
            view.new_term_format1.set(view.new_term_format1.get().replace("\\t", "\t"))
            view.new_term_format1.get().format(0, 1, 2, 3)
        if view.new_term_format2.get() != "":
            view.new_term_format2.set(view.new_term_format2.get().replace("\\n", "\n"))
            view.new_term_format2.set(view.new_term_format2.get().replace("\\t", "\t"))
            view.new_term_format2.get().format(0, 1, 2, 3)
        tkmsgbox.showinfo(title="Success!", message="Term formats saved successfully.")
        view.destroy()

    def on_save_definition_formats(self, view):
        try:
            view.new_definition_format1.get().format(0, 1, 2, 3)
            view.new_definition_format2.get().format(0, 1, 2, 3)
        except ValueError:
            tkmsgbox.showerror(title="Error saving definition format", message="Something went wrong "
                                                                               "formatting the definition")
        if view.new_definition_format1.get() != "":
            view.new_definition_format1.set(view.new_definition_format1.get().replace("\\n", "\n"))
            view.new_definition_format1.set(view.new_definition_format1.get().replace("\\t", "\t"))
            self.definition_format1 = view.new_definition_format1
        if view.new_definition_format2.get() != "":
            view.new_definition_format2.set(view.new_definition_format2.get().replace("\\n", "\n"))
            view.new_definition_format2.set(view.new_definition_format2.get().replace("\\t", "\t"))
            self.definition_format2 = view.new_definition_format2
        tkmsgbox.showinfo(title="Success!", message="Definition formats saved successfully.")
        view.destroy()

    def on_extension_name_prompt(self, view):
        view.extension_name.set("")
        view.extension_format.set("")
        view.extension_first.set(-1)
        view.extension_name_combobox.config(values=self.noteutil.extension_names)

    def on_save_extension_format(self, view):
        try:
            view.extension_format.get().format(0, 1)
        except ValueError:
            tkmsgbox.showerror(title="Error saving extension format", message="Something went wrong "
                                                                              "formatting the extension")
        if view.extension_format.get() != "":
            view.extension_format.set(view.extension_format.get().replace("\\n", "\n"))
            view.extension_format.set(view.extension_format.get().replace("\\t", "\t"))
            self.extension_format[view.extension_name.get()] = view.extension_format.get()
        if view.extension_first.get() != -1:
            self.extension_first[view.extension_name.get()] = bool(view.extension_first.get())

        tkmsgbox.showinfo(title="Success!", message="Extension format saved successfully.")

    def on_what_is_this(self):
        webbrowser.open("https://github.com/JJamesWWang/noteutil/blob/master/README.md#Quiz")

    def on_about(self):
        webbrowser.open("https://github.com/JJamesWWang/noteutil")

    def on_close(self):
        import sys
        self.save_settings()
        self.noteutil.save()
        self.quiz.save()
        self.view.root.destroy()
        sys.exit()
