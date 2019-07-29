import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as tkmsgbox
import tkinter.simpledialog as tksimpledialog
import tkinter.ttk as ttk
import noteutil as nu
from disabled_text import DisabledText
import webbrowser


class ReviewerView:
    KEY_SHORTCUTS = ""

    def __init__(self, root, noteutil, quiz, leitner):
        self.root = root
        self.root.title("NoteUtil Reviewer")
        self.controller = ReviewerController(self, noteutil, quiz, leitner)

        self.menu_bar = None
        self.reveal_label = None
        self.init_menu_bar()

        self.session_label = None
        self.boxes_label = None
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
        option_menu = tk.Menu(self.menu_bar, tearoff=False)

        option_menu.add_command(label="Generate", command=self.controller.on_generate)
        option_menu.add_separator()

        option_menu.add_command(label="Reveal", command=self.controller.on_reveal)
        option_menu.add_command(label="Mark correct", command=self.controller.on_add_correct)
        option_menu.add_command(label="Mark incorrect", command=self.controller.on_add_incorrect)
        option_menu.add_separator()

        option_menu.add_command(label="Load", command=self.controller.on_load)
        option_menu.add_command(label="Save", command=self.controller.on_save)
        option_menu.add_command(label="Reset", command=self.controller.on_reset)
        self.menu_bar.add_cascade(label="Options", menu=option_menu)

    def init_notes_menu(self):
        notes_menu = tk.Menu(self.menu_bar, tearoff=False)
        notes_menu.add_command(label="View boxes", command=self.controller.on_view_boxes)
        notes_menu.add_command(label="View notes", command=self.controller.on_view_notes)
        notes_menu.add_separator()

        notes_menu.add_command(label="Edit current note", command=self.controller.on_edit_note)
        notes_menu.add_command(label="Quick search", command=self.controller.on_quick_search)
        self.menu_bar.add_cascade(label="Notes", menu=notes_menu)

    def init_navigate_menu(self):
        navigate_menu = tk.Menu(self.menu_bar, tearoff=False)
        navigate_menu.add_command(label="Go to configurator", command=self.controller.on_to_configurator)
        navigate_menu.add_command(label="Go to editor", command=self.controller.on_to_editor)
        navigate_menu.add_command(label="Go to searcher", command=self.controller.on_to_searcher)
        navigate_menu.add_command(label="Go to quizzer", command=self.controller.on_to_quizzer)
        self.menu_bar.add_cascade(label="Navigate", menu=navigate_menu)

    def init_tools_menu(self):
        tools_menu = tk.Menu(self.menu_bar, tearoff=False)
        tools_menu.add_command(label="View image link", command=self.init_image_link_view)
        tools_menu.add_command(label="Font selector", command=self.init_font_chooser_view)
        tools_menu.add_command(label="Display LaTeX", command=self.init_display_latex_view)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

    def init_settings_menu(self):
        settings_menu = tk.Menu(self.menu_bar, tearoff=False)
        settings_menu.add_command(label="Append box", command=self.controller.on_append_box)
        settings_menu.add_command(label="Pop box", command=self.controller.on_pop_box)
        settings_menu.add_command(label="Modify box", command=self.controller.on_modify_box)
        settings_menu.add_separator()

        settings_menu.add_checkbutton(label="Randomize terms", variable=self.controller.random,
                                      command=lambda: self.controller.on_generate)
        settings_menu.add_checkbutton(label="Display term first", variable=self.controller.term_first)
        settings_menu.add_checkbutton(label="Include extensions", variable=self.controller.include_extensions)
        settings_menu.add_command(label="Set term format", command=self.init_set_term_format_view)
        settings_menu.add_command(label="Set definition format", command=self.init_set_definition_format_view)
        settings_menu.add_command(label="Set extension format", command=self.init_set_extension_format_view)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)

    def init_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        help_menu.add_command(label="What is this?", command=self.controller.on_what_is_this)
        help_menu.add_command(label="Key shortcuts", command=self.controller.on_key_shortcuts)
        help_menu.add_command(label="About", command=self.controller.on_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def init_top_frame(self):
        top_frame = tk.Frame(self.root)
        self.session_label = tk.Label(top_frame, textvariable=self.controller.current_session)
        self.session_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.generate_button = tk.Button(top_frame, text="Generate", command=self.controller.on_generate)
        self.generate_button.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X)
        self.boxes_label = tk.Label(top_frame, textvariable=self.controller.reviewing_boxes)
        self.boxes_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 0))

    def init_question_text(self):
        question_frame = tk.LabelFrame(self.root, text="Question", padx=10, pady=10, labelanchor=tk.N)
        self.question_text = DisabledText(question_frame, wrap=tk.WORD, state=tk.DISABLED, width=1, height=1,
                                          font=tkfont.Font(family="Ubuntu", size=12))
        yscrollbar = tk.Scrollbar(question_frame, orient=tk.VERTICAL, command=self.question_text.yview)
        self.question_text.config(yscrollcommand=yscrollbar.set)
        self.question_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        question_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)
        self.question_text.insert(tk.END, "The question will be asked here.")

    def init_answer_text(self):
        answer_frame = tk.LabelFrame(self.root, text="Answer", padx=10, pady=10, labelanchor=tk.N)
        self.answer_text = DisabledText(answer_frame, wrap=tk.WORD, state=tk.DISABLED, width=1, height=1,
                                        font=tkfont.Font(family="Ubuntu", size=12))
        yscrollbar = tk.Scrollbar(answer_frame, orient=tk.VERTICAL, command=self.answer_text.yview)
        self.answer_text.config(yscrollcommand=yscrollbar.set)
        self.answer_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        answer_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, expand=True)
        self.answer_text.insert(tk.END, "The answer will be displayed here.")

    def init_button_frame(self):
        button_frame = tk.Frame(self.root)
        self.correct_button = tk.Button(button_frame, text="Correct", bd=5, command=self.controller.on_add_correct)
        self.correct_button.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.X, expand=True)
        self.reveal_button = tk.Button(button_frame, textvariable=self.controller.reveal, bd=5,
                                       command=self.controller.on_reveal)
        self.reveal_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.incorrect_button = tk.Button(button_frame, text="Incorrect", bd=5, command=self.controller.on_add_incorrect)
        self.incorrect_button.pack(side=tk.LEFT, padx=(0, 10), pady=10, fill=tk.X, expand=True)
        button_frame.pack(side=tk.TOP, fill=tk.X)

    # Views generated by Menu commands

    def init_note_view(self, boxes_description):
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Your notes in boxes")
        toplevel.transient(self.root)

        toplevel.notes_text = DisabledText(toplevel, wrap=tk.NONE)
        toplevel.notes_text.set(boxes_description)
        xscrollbar = tk.Scrollbar(toplevel, orient=tk.HORIZONTAL, command=toplevel.notes_text.xview)
        yscrollbar = tk.Scrollbar(toplevel, orient=tk.VERTICAL, command=toplevel.notes_text.yview)
        toplevel.notes_text.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
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
                 text=r"Use {0} for extension_name and {1} for content, \n for newline, and \t for tab.")
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

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class ReviewerController:
    def __init__(self, view, noteutil, quiz, leitner):
        self.count = 0
        self.view = view
        self.noteutil = noteutil
        self.quiz = quiz
        self.leitner = leitner
        self.reveal = tk.StringVar(value="Reveal")
        self.current_session = tk.StringVar(value="Current session: None")
        self.reviewing_boxes = tk.StringVar(value="Reviewing boxes: None")

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

    def format_question(self, note, term_format):
        question = term_format.get().format(note.term, note.definition, note.separator, note.nindex)
        if self.include_extensions.get():
            for extension in note.extensions:
                if self.extension_first[extension.name]:
                    question += self.extension_format[extension.name].format(
                        extension.name, extension.content)
        self.view.question_text.delete(1.0, tk.END)
        self.view.question_text.insert(tk.END, question)

    def format_answer(self, note, definition_format):
        answer = definition_format.get().format(note.term, note.definition, note.separator, note.nindex)
        if self.include_extensions.get():
            for extension in note.extensions:
                if not self.extension_first[extension.name]:
                    answer += self.extension_format[extension.name].format(
                        extension.name, extension.content)
        self.view.answer_text.delete(1.0, tk.END)
        self.view.answer_text.insert(tk.END, answer)

    def on_generate(self):
        self.current_session.set("Current session: " + str(self.leitner.session))
        self.reviewing_boxes.set("Reviewing boxes: " + ", ".join(list(map(str, filter(
            lambda number: self.leitner.session % self.leitner.times[number] == 0, self.leitner.boxes)))))
        self.reveal.set("Reveal")
        option_menu = self.view.menu_bar.winfo_children()[0]
        option_menu.entryconfigure(2, label="Reveal")

        for note in self.leitner.generate(randomize=self.random.get()):
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
        if tkmsgbox.askyesno(title="Save?", message="All pairs have been cycled.\n"
                                                    "Would you like to save your progress?"):
            self.leitner.save()
            tkmsgbox.showinfo(title="Success!", message="Saved successfully.")

    def on_reveal(self):
        option_menu = self.view.menu_bar.winfo_children()[0]
        if self.reveal.get() == "Reveal":
            self.reveal.set("Continue")
            option_menu.entryconfigure(2, label="Continue")
        else:
            self.reveal.set("Reveal")
            option_menu.entryconfigure(2, label="Reveal")

    def on_add_correct(self):
        if self.current_note is not None:
            self.leitner.correct(self.current_note)
            self.on_reveal()

    def on_add_incorrect(self):
        if self.current_note is not None:
            self.leitner.incorrect(self.current_note)
            self.on_reveal()

    def on_view_boxes(self):
        boxes_description = ""
        for number, time in self.leitner.times.items():
            boxes_description += "Box {0} with time period {1}".format(number, time) + "\n"
        tkmsgbox.showinfo(title="Box periods", message=boxes_description.strip())

    def on_view_notes(self):
        boxes_description = ""
        for number, note_list in self.leitner.boxes.items():
            boxes_description += "Box {0} with time period {1}:\n".format(number, self.leitner.times[number])
            for note in note_list:
                boxes_description += "\t" + note.content + "\n"
        self.view.init_note_view(boxes_description)

    def on_load(self):
        if tkmsgbox.askyesno(title="Load?", message="Would you like to load your previous save?\n"
                                                    "This will reset any unsaved progress."):
            self.leitner.load()
            tkmsgbox.showinfo(title="Success!", message="Loaded successfully.")
            self.on_generate()

    def on_save(self):
        if tkmsgbox.askyesno(title="Save?", message="Would you like to save your progress?"):
            self.leitner.save()
            tkmsgbox.showinfo(title="Success!", message="Saved successfully.")
            self.on_generate()
        return "break"

    def on_reset(self):
        if tkmsgbox.askyesno(title="Reset?", message="Are you sure you want to reset?\n"
                                                     "This will reset all of your notes to box 1."):
            self.leitner.reset()
            tkmsgbox.showinfo(title="Success!", message="Reset successfully.")
            self.on_generate()

    def edit_note(self, view):
        try:
            self.noteutil.edit(self.current_note.nindex, view.text_editor.get(1.0, tk.END))
            self.leitner.refresh(self.noteutil)
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

    def on_quick_search(self):
        self.view.init_quick_search_view()

    def on_to_configurator(self):
        from configurator import ConfiguratorView
        option = tkmsgbox.askyesnocancel(title="Window closing", message="Would you like to save before closing?")
        if option == tk.YES:
            self.leitner.save()
            tkmsgbox.showinfo(title="Success!", message="Saved successfully.")
        if option is not None:
            self.view.clear()
            ConfiguratorView(self.view.root)

    def on_to_editor(self):
        from editor import EditorView
        toplevel = tk.Tk()
        toplevel.geometry("1600x900+160+90")
        EditorView(toplevel, self.noteutil, self.quiz, self.leitner)
        toplevel.mainloop()

    def on_to_searcher(self):
        from searcher import SearcherView
        option = tkmsgbox.askyesnocancel(title="Window closing", message="Would you like to save before closing?")
        if option == tk.YES:
            self.leitner.save()
            tkmsgbox.showinfo(title="Success!", message="Saved successfully.")
        if option is not None:
            self.view.clear()
            SearcherView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_to_quizzer(self):
        from quizzer import QuizzerView
        option = tkmsgbox.askyesnocancel(title="Window closing", message="Would you like to save before closing?")
        if option == tk.YES:
            self.leitner.save()
            tkmsgbox.showinfo(title="Success!", message="Saved successfully.")
        if option is not None:
            self.view.clear()
            QuizzerView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_append_box(self):
        boxes_description = ""
        for number, time in self.leitner.times.items():
            boxes_description += "Box {0} with time period {1}".format(number, time) + "\n"
        time = tksimpledialog.askinteger(title="Append box", prompt=boxes_description
                                         + "\nWhat is the time period of the new box?")
        if time:
            try:
                self.leitner.append_box(time)
                tkmsgbox.showinfo(title="Success!", message="Successfully added box {0} with time period {1}".format(
                    len(self.leitner.times), time))
            except nu.TimeTooShort as e:
                tkmsgbox.showerror(title="Error appending box", message=e.args[0])

    def on_pop_box(self):
        if tkmsgbox.askyesno(title="Pop box", message="Remove last box?"):
            try:
                self.leitner.pop_box()
            except nu.LastBox as e:
                tkmsgbox.showerror(title="Error popping box", message=e.args[0])

    def on_modify_box(self):
        boxes_description = ""
        for number, time in self.leitner.times.items():
            boxes_description += "Box {0} with time period {1}".format(number, time) + "\n"

        box = tksimpledialog.askinteger(title="Choose box", prompt=boxes_description
                                        + "\nWhich box would you like to modify?")
        if box is None:
            return
        time = tk.simpledialog.askinteger(title="Modify box {0}".format(box), prompt=boxes_description
                                          + "\nWhat is the new time period of the box?")
        if time is None:
            return
        try:
            self.leitner.modify_box(box, time)
        except (nu.TimeTooShort, nu.TimeTooLong) as e:
            tkmsgbox.showerror(title="Error modifying box", message=e.args[0])

    def on_save_term_formats(self, view):
        try:
            self.term_format1 = view.new_term_format1
            self.term_format2 = view.new_term_format2

        except ValueError:
            tkmsgbox.showerror(title="Error saving term format", message="Something went wrong "
                                                                         "formatting the term.")
            return "break"
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
            return "break"

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
            return "break"
        if view.extension_format.get() != "":
            view.extension_format.set(view.extension_format.get().replace("\\n", "\n"))
            view.extension_format.set(view.extension_format.get().replace("\\t", "\t"))
            self.extension_format[view.extension_name.get()] = view.extension_format.get()
        if view.extension_first.get() != -1:
            self.extension_first[view.extension_name.get()] = bool(view.extension_first.get())

        tkmsgbox.showinfo(title="Success!", message="Extension format saved successfully.")

    def on_what_is_this(self):
        webbrowser.open("https://github.com/JJamesWWang/noteutil/blob/master/README.md#Leitner")

    def on_key_shortcuts(self):
        tkmsgbox.showinfo(title="Key shortcuts", message=self.view.KEY_SHORTCUTS)

    def on_about(self):
        webbrowser.open("https://github.com/JJamesWWang/noteutil")

    def on_close(self):
        option = tkmsgbox.askyesnocancel(title="Window closing", message="Would you like to save before closing?")
        if option == tk.YES:
            self.leitner.save()
            tkmsgbox.showinfo(title="Success!", message="Saved successfully.")
        if option is not None:
            self.view.root.destroy()
