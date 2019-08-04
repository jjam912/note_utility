import tkinter as tk
import tkinter.font as tkfont
import tkinter.simpledialog as tksimpledialog
import tkinter.messagebox as tkmsgbox
import noteutil as nu
from noteutil.comparisons import CompareOptions


class SearcherView:
    def __init__(self, root: tk.Tk, noteutil, quiz, leitner):
        self.root = root
        self.root.title("NoteUtil Searcher")
        self.controller = SearcherController(self, noteutil, quiz, leitner)

        self.by_eval_button = None
        self.by_content_button = None
        self.by_rcontent_button = None
        self.by_nindex_button = None
        self.by_is_pair_button = None
        self.by_is_heading_button = None
        self.by_has_extensions_button = None
        self.by_has_categories_button = None
        self.init_main_params()

        self.if_equals_button = None
        self.if_similar_button = None
        self.if_in_button = None
        self.if_simin_button = None
        self.if_less_button = None
        self.if_lesse_button = None
        self.if_greater_button = None
        self.if_greatere_button = None
        self.init_compare_options()

        self.new_button = None
        self.and_this_button = None
        self.or_this_button = None
        self.init_narrow_options()

        # Pair
        self.by_term_button = None
        self.by_definition_button = None
        # Heading
        self.by_heading_button = None
        self.by_level_button = None
        self.by_level_name_button = None
        self.by_begin_nindex_button = None
        self.by_end_nindex_button = None
        # Extension
        self.by_extension_names_button = None
        # Category
        self.by_category_names_button = None
        self.init_sub_params()

        self.buttons = [
            self.by_eval_button, self.by_content_button, self.by_rcontent_button, self.by_nindex_button,
            self.by_is_pair_button, self.by_is_heading_button, self.by_has_extensions_button,
            self.by_has_categories_button, self.if_equals_button, self.if_similar_button, self.if_in_button,
            self.if_simin_button, self.if_less_button, self.if_lesse_button, self.if_greater_button,
            self.if_greatere_button, self.and_this_button, self.or_this_button, self.by_term_button, self.by_definition_button,
            self.by_heading_button, self.by_level_button, self.by_level_name_button, self.by_begin_nindex_button,
            self.by_end_nindex_button, self.by_extension_names_button, self.by_category_names_button
        ]
        self.main_compare_buttons = [self.by_content_button, self.by_rcontent_button, self.by_nindex_button,
                                     self.by_is_pair_button, self.by_is_heading_button, self.by_has_extensions_button,
                                     self.by_has_categories_button]
        self.compare_option_buttons = [self.if_equals_button, self.if_similar_button, self.if_in_button,
                                       self.if_simin_button, self.if_less_button, self.if_lesse_button,
                                       self.if_greater_button, self.if_greatere_button]
        self.narrow_buttons = [self.new_button, self.or_this_button, self.and_this_button]
        self.sub_compare_buttons = [self.by_term_button, self.by_definition_button, self.by_heading_button,
                                    self.by_level_button, self.by_level_name_button, self.by_begin_nindex_button,
                                    self.by_end_nindex_button, self.by_extension_names_button,
                                    self.by_category_names_button]

        self.int_buttons = [self.by_nindex_button, self.by_level_button, self.by_begin_nindex_button,
                            self.by_end_nindex_button, self.if_less_button, self.if_lesse_button,
                            self.if_greater_button, self.if_greatere_button]
        self.string_buttons = [self.by_content_button, self.by_rcontent_button, self.by_term_button,
                               self.by_definition_button, self.by_heading_button, self.by_level_name_button,
                               self.by_extension_names_button, self.by_category_names_button,
                               self.if_similar_button, self.if_in_button, self.if_simin_button]
        self.bool_buttons = [self.by_is_pair_button, self.by_is_heading_button, self.by_has_extensions_button,
                             self.by_has_categories_button]
        self.bool_button_links = {self.by_is_pair_button: [self.by_term_button, self.by_definition_button],
                                  self.by_is_heading_button: [self.by_heading_button, self.by_level_button,
                                                              self.by_level_name_button, self.by_begin_nindex_button,
                                                              self.by_end_nindex_button],
                                  self.by_has_extensions_button: [self.by_extension_names_button],
                                  self.by_has_categories_button: [self.by_category_names_button]}
        self.int_compare_buttons = [self.if_less_button, self.if_lesse_button, self.if_greater_button,
                                    self.if_greatere_button]
        self.string_compare_buttons = [self.if_similar_button, self.if_in_button, self.if_simin_button]

        self.search_bar = None
        self.search_button = None
        self.search_icon = None
        self.init_search_bar()

        self.results_list = None
        self.init_results_list()

        self.menu_bar = None
        self.init_menu_bar()

        self.modify_grid()

    def init_menu_bar(self):
        self.menu_bar = tk.Menu(self.root, tearoff=False)
        self.init_view_menu()
        self.init_notes_menu()
        self.init_navigate_menu()
        self.init_tools_menu()
        self.init_help_menu()
        self.root.config(menu=self.menu_bar)

    def init_view_menu(self):
        view_menu = tk.Menu(self.menu_bar, tearoff=False)
        view_menu.add_command(label="Change output format", command=self.controller.on_change_output_format)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

    def init_notes_menu(self):
        notes_menu = tk.Menu(self.menu_bar, tearoff=False)
        notes_menu.add_command(label="Select search bar", command=self.on_select_search_bar)
        notes_menu.add_command(label="Edit note", command=self.controller.on_edit_note)
        notes_menu.add_separator()
        notes_menu.add_command(label="View correct", command=self.controller.on_view_correct)
        notes_menu.add_command(label="View incorrect", command=self.controller.on_view_incorrect)
        notes_menu.add_command(label="View unmarked", command=self.controller.on_view_unmarked)
        notes_menu.add_separator()
        notes_menu.add_command(label="View boxes", command=self.controller.on_view_boxes)
        self.menu_bar.add_cascade(label="Notes", menu=notes_menu)

    def init_navigate_menu(self):
        navigate_menu = tk.Menu(self.menu_bar, tearoff=False)
        navigate_menu.add_command(label="Go to configurator", command=self.controller.on_to_configurator)
        navigate_menu.add_command(label="Go to editor", command=self.controller.on_to_editor)
        navigate_menu.add_command(label="Go to quizzer", command=self.controller.on_to_quizzer)
        navigate_menu.add_command(label="Go to reviewer", command=self.controller.on_to_reviewer)
        self.menu_bar.add_cascade(label="Navigate", menu=navigate_menu)

    def init_tools_menu(self):
        tools_menu = tk.Menu(self.menu_bar, tearoff=False)
        tools_menu.add_command(label="View image link", command=self.init_image_link_view)
        tools_menu.add_command(label="Font selector", command=self.init_font_chooser_view)
        tools_menu.add_command(label="Display LaTeX", command=self.init_display_latex_view)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

    def init_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        help_menu.add_command(label="Search by explanation", command=self.controller.on_search_explanation)
        help_menu.add_command(label="Compare by explanation", command=self.controller.on_compare_explanation)
        help_menu.add_command(label="Narrow with explanation", command=self.controller.on_narrow_explanation)
        help_menu.add_command(label="About", command=self.controller.on_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def init_main_params(self):
        search_frame = tk.LabelFrame(self.root, text="Search by:")
        self.by_eval_button = tk.Radiobutton(search_frame, variable=self.controller.parameter_option, text="Eval",
                                             value="Eval", state=tk.DISABLED, command=self.on_eval_button)
        self.by_eval_button.value = "Eval"
        self.by_eval_button.grid(row=0, column=0, sticky=tk.W)
        self.by_content_button = tk.Radiobutton(search_frame, variable=self.controller.parameter_option, text="Content",
                                                value="Content", command=self.on_button_click)
        self.by_content_button.value = "Content"
        self.by_content_button.grid(row=1, column=0, sticky=tk.W)
        self.by_rcontent_button = tk.Radiobutton(search_frame, variable=self.controller.parameter_option,
                                                 text="Raw content", value="Raw content", command=self.on_button_click)
        self.by_rcontent_button.value = "Raw content"
        self.by_rcontent_button.grid(row=2, column=0, sticky=tk.W)
        self.by_nindex_button = tk.Radiobutton(search_frame, variable=self.controller.parameter_option,
                                               text="Note index", value="Note index", state=tk.DISABLED,
                                               command=self.on_button_click)
        self.by_nindex_button.value = "Note index"
        self.by_nindex_button.grid(row=3, column=0, sticky=tk.W)
        self.by_is_pair_button = tk.Checkbutton(search_frame, variable=self.controller.by_is_pair, text="Is pair",
                                                command=self.on_bool_button)
        self.by_is_pair_button.value = self.controller.by_is_pair
        self.by_is_pair_button.grid(row=0, column=1, sticky=tk.W)
        self.by_is_heading_button = tk.Checkbutton(search_frame, variable=self.controller.by_is_heading,
                                                   text="Is heading", command=self.on_bool_button)
        self.by_is_heading_button.value = self.controller.by_is_heading
        self.by_is_heading_button.grid(row=1, column=1, sticky=tk.W)
        self.by_has_extensions_button = tk.Checkbutton(search_frame, variable=self.controller.by_has_extensions,
                                                       text="Has extensions", command=self.on_bool_button)
        self.by_has_extensions_button.value = self.controller.by_has_extensions
        self.by_has_extensions_button.grid(row=2, column=1, sticky=tk.W)
        self.by_has_categories_button = tk.Checkbutton(search_frame, variable=self.controller.by_has_categories,
                                                       text="Has categories", command=self.on_bool_button)
        self.by_has_categories_button.value = self.controller.by_has_categories
        self.by_has_categories_button.grid(row=3, column=1, sticky=tk.W)
        search_frame.grid(row=0, column=1, sticky=tk.EW)

    def init_compare_options(self):
        compare_frame = tk.LabelFrame(self.root, text="Compare by:")
        self.if_equals_button = tk.Radiobutton(compare_frame, variable=self.controller.compare_option, text="Equals",
                                               value="Equals", command=self.on_button_click)
        self.if_equals_button.value = "Equals"
        self.if_equals_button.grid(row=0, column=0, sticky=tk.W)
        self.if_similar_button = tk.Radiobutton(compare_frame, variable=self.controller.compare_option, text="Similar",
                                                value="Similar", command=self.on_button_click)
        self.if_similar_button.value = "Similar"
        self.if_similar_button.grid(row=1, column=0, sticky=tk.W)
        self.if_in_button = tk.Radiobutton(compare_frame, variable=self.controller.compare_option, text="In",
                                           value="In", command=self.on_button_click)
        self.if_in_button.value = "In"
        self.if_in_button.grid(row=2, column=0, stick=tk.W)
        self.if_simin_button = tk.Radiobutton(compare_frame, variable=self.controller.compare_option, text="Similar in",
                                              value="Similar in", command=self.on_button_click)
        self.if_simin_button.value = "Similar in"
        self.if_simin_button.grid(row=3, column=0, sticky=tk.W)
        self.if_less_button = tk.Radiobutton(compare_frame, variable=self.controller.compare_option, text="Less than",
                                             value="Less than", state=tk.DISABLED, command=self.on_button_click)
        self.if_less_button.value = "Less than"
        self.if_less_button.grid(row=0, column=1, sticky=tk.W)
        self.if_lesse_button = tk.Radiobutton(compare_frame, variable=self.controller.compare_option, text="Less/Equal",
                                              value="Less/Equal", state=tk.DISABLED, command=self.on_button_click)
        self.if_lesse_button.value = "Less/Equal"
        self.if_lesse_button.grid(row=1, column=1, sticky=tk.W)
        self.if_greater_button = tk.Radiobutton(compare_frame, variable=self.controller.compare_option,
                                                text="Greater than", value="Greater than", state=tk.DISABLED,
                                                command=self.on_button_click)
        self.if_greater_button.value = "Greater than"
        self.if_greater_button.grid(row=2, column=1, sticky=tk.W)
        self.if_greatere_button = tk.Radiobutton(compare_frame, variable=self.controller.compare_option,
                                                 text="Greater/Equal", value="Greater/Equal", state=tk.DISABLED,
                                                 command=self.on_button_click)
        self.if_greatere_button.value = "Greater/Equal"
        self.if_greatere_button.grid(row=3, column=1, sticky=tk.W)
        compare_frame.grid(row=0, column=2, sticky=tk.EW)

    def init_narrow_options(self):
        narrow_frame = tk.LabelFrame(self.root, text="Narrow with:")
        self.new_button = tk.Radiobutton(narrow_frame, variable=self.controller.narrow_option, text="New", value="New")
        self.new_button.value = "New"
        self.new_button.grid(row=0, column=0, sticky=tk.W)
        self.or_this_button = tk.Radiobutton(narrow_frame, variable=self.controller.narrow_option, text="Or",
                                             value="Or", state=tk.DISABLED)
        self.or_this_button.value = "Or"
        self.or_this_button.grid(row=1, column=0, sticky=tk.W)
        self.and_this_button = tk.Radiobutton(narrow_frame, variable=self.controller.narrow_option, text="And",
                                              value="And", state=tk.DISABLED)
        self.and_this_button.value = "And"
        self.and_this_button.grid(row=2, column=0, sticky=tk.W)
        # TODO: Add Invert button
        narrow_frame.grid(row=0, column=3, columnspan=2, padx=(0, 20), sticky=tk.NSEW)

    def init_sub_params(self):
        subsearch_frame = tk.LabelFrame(self.root, text="Search by:")
        self.by_term_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                             text="Term", value="Term", state=tk.DISABLED,
                                             command=self.on_button_click)
        self.by_term_button.value = "Term"
        self.by_term_button.grid(row=0, column=0, sticky=tk.W)
        self.by_definition_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                   text="Definition", value="Definition", state=tk.DISABLED,
                                                   command=self.on_button_click)
        self.by_definition_button.value = "Definition"
        self.by_definition_button.grid(row=1, column=0, sticky=tk.W)
        self.by_heading_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                text="Heading", value="Heading", state=tk.DISABLED,
                                                command=self.on_button_click)
        self.by_heading_button.value = "Heading"
        self.by_heading_button.grid(row=2, column=0, sticky=tk.W)
        self.by_level_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                              text="Level", value="Level", state=tk.DISABLED,
                                              command=self.on_button_click)
        self.by_level_button.value = "Level"
        self.by_level_button.grid(row=3, column=0, sticky=tk.W)
        self.by_level_name_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                   text="Level name", value="Level name", state=tk.DISABLED,
                                                   command=self.on_button_click)
        self.by_level_name_button.value = "Level name"
        self.by_level_name_button.grid(row=4, column=0, sticky=tk.W)
        self.by_begin_nindex_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                     text="Begin note index", value="Begin note index",
                                                     state=tk.DISABLED, command=self.on_button_click)
        self.by_begin_nindex_button.value = "Begin note index"
        self.by_begin_nindex_button.grid(row=5, column=0, sticky=tk.W)
        self.by_end_nindex_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                   text="End note index", value="End note index", state=tk.DISABLED,
                                                   command=self.on_button_click)
        self.by_end_nindex_button.value = "End note index"
        self.by_end_nindex_button.grid(row=6, column=0, sticky=tk.W)
        self.by_extension_names_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                        text="Extension names", value="Extension names",
                                                        state=tk.DISABLED, command=self.on_button_click)
        self.by_extension_names_button.value = "Extension names"
        self.by_extension_names_button.grid(row=7, column=0, sticky=tk.W)
        self.by_category_names_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                       text="Category names", value="Category names", state=tk.DISABLED,
                                                       command= self.on_button_click)
        self.by_category_names_button.value = "Category names"
        self.by_category_names_button.grid(row=8, column=0, sticky=tk.W)
        subsearch_frame.grid(row=1, column=0, rowspan=2, padx=20, pady=20, sticky=tk.NS)

    def init_search_bar(self):
        self.search_bar = tk.Entry(self.root, font=tkfont.Font(family="Ubuntu", size=12))
        self.search_icon = tk.PhotoImage(file="icons/magnifying_glass.png")
        self.search_button = tk.Button(self.search_bar, image=self.search_icon, command=self.controller.on_search,
                                       relief=tk.GROOVE)
        self.search_button.pack(side=tk.RIGHT)

        self.search_bar.insert(tk.END, "Enter your search query in here.")
        self.search_bar.grid(row=1, column=1, columnspan=4, padx=(0, 20), pady=10, sticky=tk.EW)
        self.search_bar.bind("<Return>", self.controller.on_search)

    def init_results_list(self):
        self.results_list = tk.Listbox(self.root, activestyle="dotbox", selectmode=tk.SINGLE,
                                       font=tkfont.Font(family="Ubuntu", size=12))
        xscroll_bar = tk.Scrollbar(self.results_list, orient=tk.HORIZONTAL)
        yscroll_bar = tk.Scrollbar(self.results_list, orient=tk.VERTICAL)
        xscroll_bar.config(command=self.results_list.xview)
        yscroll_bar.config(command=self.results_list.yview)
        self.results_list.config(xscrollcommand=xscroll_bar.set, yscrollcommand=yscroll_bar.set)
        self.results_list.insert(tk.END, "Your results will show up here.")
        self.results_list.grid(row=2, column=1, columnspan=4, padx=(0, 20), pady=(0, 20), sticky=tk.NSEW)

    def modify_grid(self):
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(4, weight=1)

    def on_button_click(self):
        if self.controller.compare_option.get() == "Equals":
            enabled = [self.by_eval_button]
            enabled.extend(self.main_compare_buttons)
            enabled.extend(self.compare_option_buttons)
            for kbutton, linked_buttons in self.bool_button_links.items():
                if kbutton.value.get():
                    enabled.extend(linked_buttons)
            for button in enabled:
                button.config(state=tk.NORMAL)
        elif self.controller.parameter_option.get() in map(lambda b: b.value, self.int_buttons):
            self.by_eval_button.config(state=tk.DISABLED)
            for button in self.string_buttons:
                button.deselect()
                button.config(state=tk.DISABLED)
        elif self.controller.parameter_option.get() in map(lambda b: b.value, self.string_buttons):
            self.by_eval_button.config(state=tk.DISABLED)
            for button in self.int_buttons:
                button.deselect()
                button.config(state=tk.DISABLED)

    def on_eval_button(self):
        if self.controller.parameter_option.get() == "Eval":
            self.search_bar.delete(0, tk.END)
            self.controller.add_kwargs()
            query = self.controller.search_eval + ")"
            self.search_bar.insert(tk.END, query)
            for button in self.main_compare_buttons + self.compare_option_buttons + self.sub_compare_buttons:
                button.deselect()
                button.config(state=tk.DISABLED)
        else:
            self.controller.search_eval = "self.noteutil.get_list("
            for button in self.main_compare_buttons + self.compare_option_buttons:
                button.config(state=tk.NORMAL)

    def on_bool_button(self):
        for kbutton, linked_buttons in self.bool_button_links.items():
            if kbutton.value.get():
                for button in self.bool_button_links[kbutton]:
                    button.config(state=tk.NORMAL)
            else:
                for button in self.bool_button_links[kbutton]:
                    button.deselect()
                    button.config(state=tk.DISABLED)
        self.on_button_click()

    def on_select_search_bar(self):
        self.search_bar.event_generate("<<Select All>>")
        self.search_bar.focus_set()

    # Views generated by Menu commands
    def init_note_view(self, description):
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Your Notes")
        toplevel.transient(self.root)

        toplevel.notes_text = tk.Text(toplevel, wrap=tk.NONE)
        toplevel.notes_text.insert(tk.END, description)
        xscrollbar = tk.Scrollbar(toplevel, orient=tk.HORIZONTAL, command=toplevel.notes_text.xview)
        yscrollbar = tk.Scrollbar(toplevel, orient=tk.VERTICAL, command=toplevel.notes_text.yview)
        toplevel.notes_text.config(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set, state=tk.DISABLED)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        toplevel.notes_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

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

    def clear(self):
        self.root.unbind("<Button-1>")
        for widget in self.root.winfo_children():
            widget.destroy()


class SearcherController:
    def __init__(self, view, noteutil, quiz, leitner):
        self.count = 0
        self.view = view
        self.notes = []
        self.noteutil = noteutil
        self.quiz = quiz
        self.leitner = leitner
        self.search_eval = "self.noteutil.get_list("

        self.by_is_pair = tk.BooleanVar()
        self.by_is_heading = tk.BooleanVar()
        self.by_has_extensions = tk.BooleanVar()
        self.by_has_categories = tk.BooleanVar()

        self.parameter_option = tk.StringVar(value="Content")
        self.compare_option = tk.StringVar(value="Similar in")
        self.narrow_option = tk.StringVar(value="New")

        self.compare_button_functions = {
            "Equals":           CompareOptions.EQUALS,
            "Similar":          CompareOptions.SIMILAR,
            "In":               CompareOptions.IN,
            "Similar in":       CompareOptions.SIMIN,
            "Less than":        CompareOptions.LESS,
            "Less/Equal":       CompareOptions.LESSE,
            "Greater than":     CompareOptions.GREATER,
            "Greater/Equal":    CompareOptions.GREATERE,
        }

    def on_change_output_format(self):
        self.count += 1
        print(self.count)

    def add_kwargs(self):
        self.search_eval += "content=\"{0}\", " if self.by_content.get() else ""
        self.search_eval += "rcontent=\"{1}\", " if self.by_rcontent.get() else ""
        self.search_eval += "nindex={2}, " if self.by_nindex.get() else ""
        self.search_eval += "term=\"{3}\", " if self.by_term.get() else ""
        self.search_eval += "definition=\"{4}\", " if self.by_definition.get() else ""
        self.search_eval += "heading=\"{5}\", " if self.by_heading.get() else ""
        self.search_eval += "level={6}, " if self.by_level.get() else ""
        self.search_eval += "level_name=\"{7}\", " if self.by_level_name.get() else ""
        self.search_eval += "begin_nindex={8}, " if self.by_begin_nindex.get() else ""
        self.search_eval += "end_nindex={9}, " if self.by_end_nindex.get() else ""
        self.search_eval += "extension_names=\"{10}\", " if self.by_extension_names.get() else ""
        self.search_eval += "category_names=\"{11}\", " if self.by_category_names.get() else ""
        self.search_eval = self.search_eval[:-2]
        self.search_eval += ")"

    def on_search(self, event=None):
        self.add_kwargs()
        try:
            print(self.search_eval)
            searched_notes = eval(self.search_eval).format()
            print(searched_notes)
            self.notes.extend(searched_notes if searched_notes else [])
        except SyntaxError:
            tkmsgbox.showerror(title="Error searching", message="No search options were selected.")

        if self.by_is_pair.get():
            self.notes = list(filter(lambda n: n.is_pair(), self.notes))
        if self.by_is_heading.get():
            self.notes = list(filter(lambda n: n.is_heading(), self.notes))
        if self.by_has_extensions.get():
            self.notes = list(filter(lambda n: n.has_extensions(), self.notes))
        if self.by_has_categories.get():
            self.notes = list(filter(lambda n: n.has_catgeories(), self.notes))
        for note in self.notes:
            self.view.results_list.insert(tk.END, note.rcontent)
        self.search_eval = "self.noteutil.get_list("

    def on_edit_note(self):
        self.count += 1
        print(self.count)
        return "break"

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

    def on_view_boxes(self):
        boxes_description = ""
        for number, note_list in self.leitner.boxes.items():
            boxes_description += "Box {0} with time period {1}:\n".format(number, self.leitner.times[number])
            for note in note_list:
                boxes_description += "\t" + note.content + "\n"
        self.view.init_notes_view(boxes_description.strip())

    def on_to_configurator(self):
        from configurator import ConfiguratorView
        self.view.clear()
        ConfiguratorView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_to_editor(self):
        from editor import EditorView
        toplevel = tk.Tk()
        toplevel.geometry("1600x900+160+90")
        EditorView(toplevel, self.noteutil, self.quiz, self.leitner)
        toplevel.mainloop()

    def on_to_quizzer(self):
        from quizzer import QuizzerView
        self.view.clear()
        QuizzerView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_to_reviewer(self):
        from reviewer import ReviewerView
        self.view.clear()
        ReviewerView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_search_explanation(self):
        self.count += 1
        print(self.count)

    def on_compare_explanation(self):
        self.count += 1
        print(self.count)

    def on_narrow_explanation(self):
        self.count += 1
        print(self.count)

    def on_about(self):
        self.count += 1
        print(self.count)


if __name__ == "__main__":
    gui = tk.Tk()
    app = SearcherView(gui, None, None, None)
    gui.geometry("1600x900+160+90")
    gui.mainloop()


