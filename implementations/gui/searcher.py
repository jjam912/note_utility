import tkinter as tk
import tkinter.font as tkfont
import tkinter.simpledialog as tksimpledialog
import tkinter.messagebox as tkmsgbox
import noteutil as nu
from noteutil.comparisons import CompareOptions
import webbrowser


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

        self.invert_button = None
        self.new_button = None
        self.and_this_button = None
        self.or_this_button = None
        self.init_narrow_options()

        # Pair
        self.by_term_button = None
        self.by_definition_button = None
        # Heading
        self.by_heading_button = None
        self.by_heading_name_button = None
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
            self.if_greatere_button, self.and_this_button, self.or_this_button, self.by_term_button,
            self.by_definition_button, self.by_heading_button, self.by_heading_name_button, self.by_level_button,
            self.by_level_name_button, self.by_begin_nindex_button,self.by_end_nindex_button,
            self.by_extension_names_button, self.by_category_names_button
        ]
        self.main_param_buttons = [self.by_content_button, self.by_rcontent_button, self.by_nindex_button,
                                   self.by_is_pair_button, self.by_is_heading_button, self.by_has_extensions_button,
                                   self.by_has_categories_button]
        self.compare_option_buttons = [self.if_equals_button, self.if_similar_button, self.if_in_button,
                                       self.if_simin_button, self.if_less_button, self.if_lesse_button,
                                       self.if_greater_button, self.if_greatere_button]
        self.narrow_buttons = [self.invert_button, self.new_button, self.or_this_button, self.and_this_button]
        self.sub_param_buttons = [self.by_term_button, self.by_definition_button, self.by_heading_button,
                                  self.by_heading_name_button, self.by_level_button, self.by_level_name_button,
                                  self.by_begin_nindex_button, self.by_end_nindex_button,
                                  self.by_extension_names_button, self.by_category_names_button]

        self.int_buttons = [self.by_nindex_button, self.by_level_button, self.by_begin_nindex_button,
                            self.by_end_nindex_button, self.if_less_button, self.if_lesse_button,
                            self.if_greater_button, self.if_greatere_button]
        self.string_buttons = [self.by_content_button, self.by_rcontent_button, self.by_term_button,
                               self.by_definition_button, self.by_heading_button, self.by_heading_name_button,
                               self.by_level_name_button, self.by_extension_names_button, self.by_category_names_button,
                               self.if_similar_button, self.if_in_button, self.if_simin_button]
        self.bool_buttons = [self.by_is_pair_button, self.by_is_heading_button, self.by_has_extensions_button,
                             self.by_has_categories_button]
        self.bool_button_links = {self.by_is_pair_button: [self.by_term_button, self.by_definition_button],
                                  self.by_is_heading_button: [self.by_heading_button, self.by_heading_name_button,
                                                              self.by_level_button, self.by_level_name_button,
                                                              self.by_begin_nindex_button, self.by_end_nindex_button],
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
        self.results_list_menu = None
        self.init_results_list()

        self.menu_bar = None
        self.init_menu_bar()

        self.modify_grid()

    def init_menu_bar(self):
        self.menu_bar = tk.Menu(self.root, tearoff=False)
        self.init_notes_menu()
        self.init_navigate_menu()
        self.init_tools_menu()
        self.init_help_menu()
        self.root.config(menu=self.menu_bar)

    def init_notes_menu(self):
        notes_menu = tk.Menu(self.menu_bar, tearoff=False)
        notes_menu.add_command(label="Set note preview", command=self.init_set_note_preview_view)
        notes_menu.add_command(label="Select search bar", accelerator="Ctrl+F", command=self.on_select_search_bar)
        self.root.bind("<Control-F>", lambda e: self.on_select_search_bar())
        self.root.bind("<Control-f>", lambda e: self.on_select_search_bar())
        notes_menu.add_command(label="View note", accelerator="Ctrl+O",  command=self.controller.on_view_note)
        self.root.bind("<Control-O>", lambda e: self.controller.on_view_note())
        self.root.bind("<Control-o>", lambda e: self.controller.on_view_note())
        notes_menu.add_command(label="Edit note", accelerator="Ctrl+E", command=self.init_edit_note_view)
        self.root.bind("<Control-E>", lambda e: self.init_edit_note_view())
        self.root.bind("<Control-e>", lambda e: self.init_edit_note_view())
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
        tools_menu.add_command(label="View image link", accelerator="Ctrl+I", command=self.init_image_link_view)
        self.root.bind("<Control-I>", lambda e: self.init_image_link_view())
        self.root.bind("<Control-i>", lambda e: self.init_image_link_view())
        tools_menu.add_command(label="Font selector", command=self.init_font_chooser_view)
        tools_menu.add_command(label="Display LaTeX", accelerator="Ctrl+L", command=self.init_display_latex_view)
        self.root.bind("<Control-L>", lambda e: self.init_display_latex_view())
        self.root.bind("<Control-l>", lambda e: self.init_display_latex_view())
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
        self.by_eval_button = tk.Checkbutton(search_frame, variable=self.controller.by_eval, text="Eval",
                                             command=self.on_eval_button)
        self.by_eval_button.value = self.controller.by_eval
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

        self.invert_button = tk.Checkbutton(narrow_frame, variable=self.controller.invert_option, text="Invert")
        self.invert_button.value = self.controller.invert_option
        self.invert_button.grid(row=0, column=0, sticky=tk.W)
        self.new_button = tk.Radiobutton(narrow_frame, variable=self.controller.narrow_option, text="New", value="New")
        self.new_button.value = "New"
        self.new_button.grid(row=1, column=0, sticky=tk.W)
        self.or_this_button = tk.Radiobutton(narrow_frame, variable=self.controller.narrow_option, text="Or",
                                             value="Or",)
        self.or_this_button.value = "Or"
        self.or_this_button.grid(row=2, column=0, sticky=tk.W)
        self.and_this_button = tk.Radiobutton(narrow_frame, variable=self.controller.narrow_option, text="And",
                                              value="And",)
        self.and_this_button.value = "And"
        self.and_this_button.grid(row=3, column=0, sticky=tk.W)
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
        self.by_heading_name_button=tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                   text="Heading name", value="Heading name", state=tk.DISABLED,
                                                   command=self.on_button_click)
        self.by_heading_name_button.value = "Heading name"
        self.by_heading_name_button.grid(row=3, column=0, sticky=tk.W)
        self.by_level_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                              text="Level", value="Level", state=tk.DISABLED,
                                              command=self.on_button_click)
        self.by_level_button.value = "Level"
        self.by_level_button.grid(row=4, column=0, sticky=tk.W)
        self.by_level_name_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                   text="Level name", value="Level name", state=tk.DISABLED,
                                                   command=self.on_button_click)
        self.by_level_name_button.value = "Level name"
        self.by_level_name_button.grid(row=5, column=0, sticky=tk.W)
        self.by_begin_nindex_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                     text="Begin note index", value="Begin note index",
                                                     state=tk.DISABLED, command=self.on_button_click)
        self.by_begin_nindex_button.value = "Begin note index"
        self.by_begin_nindex_button.grid(row=6, column=0, sticky=tk.W)
        self.by_end_nindex_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                   text="End note index", value="End note index", state=tk.DISABLED,
                                                   command=self.on_button_click)
        self.by_end_nindex_button.value = "End note index"
        self.by_end_nindex_button.grid(row=7, column=0, sticky=tk.W)
        self.by_extension_names_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                        text="Extension names", value="Extension names",
                                                        state=tk.DISABLED, command=self.on_button_click)
        self.by_extension_names_button.value = "Extension names"
        self.by_extension_names_button.grid(row=8, column=0, sticky=tk.W)
        self.by_category_names_button = tk.Radiobutton(subsearch_frame, variable=self.controller.parameter_option,
                                                       text="Category names", value="Category names", state=tk.DISABLED,
                                                       command= self.on_button_click)
        self.by_category_names_button.value = "Category names"
        self.by_category_names_button.grid(row=9, column=0, sticky=tk.W)
        subsearch_frame.grid(row=1, column=0, rowspan=2, padx=20, pady=20, sticky=tk.NS)

    def init_search_bar(self):
        search_bar_frame = tk.Frame(self.root)
        self.search_bar = tk.Entry(search_bar_frame, font=tkfont.Font(family="Ubuntu", size=12))
        self.search_icon = tk.PhotoImage(file="icons/magnifying_glass.png")
        self.search_button = tk.Button(search_bar_frame, image=self.search_icon, command=self.controller.on_search,
                                       relief=tk.GROOVE)

        self.search_bar.insert(tk.END, "Enter your search query in here.")
        self.search_button.pack(side=tk.RIGHT)
        self.search_bar.pack(fill=tk.X, expand=True)
        search_bar_frame.grid(row=1, column=1, columnspan=4, padx=(0, 20), pady=10, sticky=tk.EW)
        self.search_bar.bind("<Return>", self.controller.on_search)

    def init_results_list(self):
        results_list_frame = tk.Frame(self.root)
        self.results_list = tk.Listbox(results_list_frame, activestyle="dotbox", selectmode=tk.SINGLE,
                                       font=tkfont.Font(family="Ubuntu", size=12))
        xscroll_bar = tk.Scrollbar(results_list_frame, width=16, orient=tk.HORIZONTAL, command=self.results_list.xview)
        yscroll_bar = tk.Scrollbar(results_list_frame, width=16, orient=tk.VERTICAL, command=self.results_list.yview)
        self.results_list.config(xscrollcommand=xscroll_bar.set, yscrollcommand=yscroll_bar.set)
        self.results_list.insert(tk.END, "Your results will show up here.")
        xscroll_bar.pack(side=tk.BOTTOM, fill=tk.X)
        yscroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_list.pack(fill=tk.BOTH, expand=True)
        results_list_frame.grid(row=2, column=1, columnspan=4, padx=(0, 20), pady=(0, 20), sticky=tk.NSEW)

        self.results_list_menu = tk.Menu(self.results_list, tearoff=False)
        self.results_list_menu.add_command(label="View", command=self.controller.on_view_note)
        self.results_list_menu.add_command(label="Edit", command=self.init_edit_note_view)

        def popup_menu(event):
            self.results_list.selection_clear(0, tk.END)
            self.results_list.selection_set(self.results_list.nearest(event.y))
            self.results_list_menu.tk_popup(event.x_root, event.y_root)

        self.results_list.bind("<Button-3>", lambda e: popup_menu(e))

    def modify_grid(self):
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(4, weight=1)

    def on_button_click(self):
        if self.controller.compare_option.get() == "Equals":
            enabled = [self.by_eval_button]
            enabled.extend(self.main_param_buttons)
            enabled.extend(self.compare_option_buttons)
            for kbutton, linked_buttons in self.bool_button_links.items():
                if kbutton.value.get():
                    enabled.extend(linked_buttons)
            for button in enabled:
                button.config(state=tk.NORMAL)
        elif self.controller.parameter_option.get() in map(lambda b: b.value, self.int_buttons):
            for button in self.string_buttons:
                button.deselect()
                button.config(state=tk.DISABLED)
        elif self.controller.parameter_option.get() in map(lambda b: b.value, self.string_buttons):
            for button in self.int_buttons:
                button.deselect()
                button.config(state=tk.DISABLED)

    def on_eval_button(self):
        if self.controller.by_eval.get():
            self.search_bar.delete(0, tk.END)
            query = self.controller.search_eval
            self.search_bar.insert(tk.END, query)
            for button in self.main_param_buttons + self.compare_option_buttons + self.sub_param_buttons:
                button.deselect()
                button.config(state=tk.DISABLED)
        else:
            self.controller.search_eval = "self.noteutil.iget_list(" \
                if self.controller.invert_option.get() else "self.noteutil.get_list("
            for button in self.main_param_buttons + self.compare_option_buttons:
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
    def init_set_note_preview_view(self):
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Set note preview")
        toplevel.transient(self.root)
        toplevel.resizable(True, False)

        tk.Label(toplevel, text="Use {0} for content, {1} for rcontent, {2} for note index, {3} for term, \n"
                                "{4} for definition, {5} for heading, {6} for heading name, {7} for level, \n"
                                "{8} for level name, {9} for begin note index, {10} for end note index, \n"
                                "{11} for extension names, and {12} for category_names, \n").pack(side=tk.TOP)
        tk.Label(toplevel, text="Note preview:").pack(side=tk.TOP)
        note_preview = tk.StringVar()

        def on_save():
            self.controller.note_preview.set(note_preview.get())
            toplevel.destroy()

        entry = tk.Entry(toplevel, textvariable=note_preview)
        entry.pack(side=tk.TOP, expand=True, fill=tk.X)
        entry.bind("<Return>", lambda e: on_save())
        tk.Button(toplevel, text="Save", command=on_save).pack(side=tk.TOP, fill=tk.X)

    def init_notes_view(self, description):
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

    def init_edit_note_view(self):
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Edit Note")
        toplevel.transient(self.root)
        tk.Label(toplevel, text="Displayed below is the raw content of the selected note.",
                 font=tkfont.Font(family="Ubuntu", size=12)).grid(row=0, column=0, ipady=5)

        toplevel.text_editor = tk.Text(toplevel, wrap=tk.WORD, font=tkfont.Font(family="Ubuntu", size=12),
                                       width=52, height=5)
        yscrollbar = tk.Scrollbar(toplevel, orient=tk.VERTICAL, command=toplevel.text_editor.yview)
        toplevel.text_editor.config(yscrollcommand=yscrollbar.set)

        yscrollbar.grid(row=1, column=2, padx=(0, 10), sticky=tk.NS)

        try:
            toplevel.nindex = self.results_list.curselection()[0]
            toplevel.note = self.controller.notes[toplevel.nindex]
        except IndexError:
            toplevel.destroy()
            return tkmsgbox.showerror(title="Error editing", message="Please select a valid note from the list.")

        toplevel.text_editor.insert(tk.END, toplevel.note.rcontent)
        toplevel.text_editor.grid(row=1, column=0, columnspan=2, padx=(10, 0), sticky=tk.NSEW)

        tk.Button(toplevel, text="Edit", command=lambda: self.controller.edit_note(
            toplevel)).grid(row=0, column=1, columnspan=2, padx=(5, 10), sticky=tk.EW)

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

    def unbind_all(self):
        self.root.unbind("<Control-F>")
        self.root.unbind("<Control-f>")
        self.root.unbind("<Control-O>")
        self.root.unbind("<Control-o>")
        self.root.unbind("<Control-E>")
        self.root.unbind("<Control-e>")
        self.root.unbind("<Control-I>")
        self.root.unbind("<Control-i>")
        self.root.unbind("<Control-L>")
        self.root.unbind("<Control-l>")

    def clear(self):
        self.unbind_all()
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
        self.note_preview = tk.StringVar(value="{1}")

        self.by_eval = tk.BooleanVar()
        self.by_is_pair = tk.BooleanVar()
        self.by_is_heading = tk.BooleanVar()
        self.by_has_extensions = tk.BooleanVar()
        self.by_has_categories = tk.BooleanVar()
        self.invert_option = tk.BooleanVar()

        self.parameter_option = tk.StringVar(value="Content")
        self.compare_option = tk.StringVar(value="Similar in")
        self.narrow_option = tk.StringVar(value="New")

        self.compare_button_functions = {
            "Equals":           "CompareOptions.EQUALS",
            "Similar":          "CompareOptions.SIMILAR",
            "In":               "CompareOptions.IN",
            "Similar in":       "CompareOptions.SIMIN",
            "Less than":        "CompareOptions.LESS",
            "Less/Equal":       "CompareOptions.LESSE",
            "Greater than":     "CompareOptions.GREATER",
            "Greater/Equal":    "CompareOptions.GREATERE",
        }

    def on_change_output_format(self):
        self.count += 1
        print(self.count)

    def add_kwargs(self, query):
        self.search_eval += "content=\"{}\"".format(query) if self.parameter_option.get() == "Content" else ""
        self.search_eval += "rcontent=\"{}\"".format(query) if self.parameter_option.get() == "Raw content" else ""
        self.search_eval += "nindex={}".format(query) if self.parameter_option.get() == "Note index" else ""
        self.search_eval += "term=\"{}\"".format(query) if self.parameter_option.get() == "Term" else ""
        self.search_eval += "definition=\"{}\"".format(query) if self.parameter_option.get() == "Definition" else ""
        self.search_eval += "heading=\"{}\"".format(query) if self.parameter_option.get() == "Heading" else ""
        self.search_eval += "heading_name=\"{}\"".format(query) if self.parameter_option.get() == "Heading name" else ""
        self.search_eval += "level={}".format(query) if self.parameter_option.get() == "Level" else ""
        self.search_eval += "level_name=\"{}\"".format(query) if self.parameter_option.get() == "Level name" else ""
        self.search_eval += "begin_nindex={}".format(query) \
            if self.parameter_option.get() == "Begin note index" else ""
        self.search_eval += "end_nindex={}".format(query) if self.parameter_option.get() == "End note index" else ""
        self.search_eval += "extension_names=\"{}\"".format(query) \
            if self.parameter_option.get() == "Extension names" else ""
        self.search_eval += "category_names=\"{}\"".format(query) \
            if self.parameter_option.get() == "Category names" else ""

        for compare_button in self.view.compare_option_buttons:
            if self.compare_option.get() == compare_button.value:
                self.search_eval += ", compare=" + self.compare_button_functions[compare_button.value]
        self.search_eval += ")"

    def on_search(self, event=None):
        self.view.results_list.delete(0, tk.END)
        if self.narrow_option.get() == "New":
            self.notes = []

        if not self.by_eval.get():
            self.search_eval = "self.noteutil.iget_list(" if self.invert_option.get() else "self.noteutil.get_list("
            self.add_kwargs(self.view.search_bar.get().strip())
        else:
            self.search_eval = self.view.search_bar.get().strip()

        try:
            searched_notes = eval(self.search_eval)
            if self.narrow_option.get() == "And":
                self.notes = list(filter(lambda n: n in searched_notes, self.notes))
            elif self.narrow_option.get() == "Or":
                self.notes.extend(searched_notes if searched_notes else [])
                self.notes.sort()
                notes_set = [self.notes[0]]
                for i in range(1, len(self.notes)):
                    if self.notes[i] != self.notes[i-1]:
                        notes_set.append(self.notes[i])
                self.notes = notes_set
            else:
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
            self.notes = list(filter(lambda n: n.has_categories(), self.notes))
        for note in self.notes:
            self.view.results_list.insert(tk.END, self.note_preview.get().format(
                note.content, note.rcontent, note.nindex, note.term, note.definition, note.heading, note.heading_name,
                note.level, note.level_name, note.begin_nindex, note.end_nindex,
                ", ".join(note.extension_names) if note.extension_names else "None",
                ", ".join(note.category_names) if note.category_names else "None",
            ))

    def on_view_note(self, event=None):
        try:
            nindex = self.view.results_list.curselection()[0]
            note = self.notes[nindex]
        except IndexError:
            return tkmsgbox.showerror(title="Error viewing", message="Please select a valid note from the list.")
        note_description = ("Note:\n"
                            "-----\n"
                            "Content:\n"
                            "{0}\n"
                            "\n"
                            "Raw Content:\n"
                            "{1}\n"
                            "\n"
                            "Note index: {2}\n"
                            "\n"
                            "Term:\n"
                            "{3}\n"
                            "\n"
                            "Definition:\n"
                            "{4}\n"
                            "\n"
                            "Heading: {5}\n"
                            "\n"
                            "Heading name:\n"
                            "{6}\n"
                            "\n"
                            "Level: {7}\n"
                            "Level name:       {8}\n"
                            "Begin note index: {9}\n"
                            "End note index:   {10}\n"
                            "Extension names:  {11}\n"
                            "Category names:   {12}\n"
                            "-----\n"
                            ).format(note.content, note.rcontent, note.nindex, note.term, note.definition, note.heading,
                                     note.heading_name, note.level, note.level_name, note.begin_nindex, note.end_nindex,
                                     ", ".join(note.extension_names) if note.extension_names else "None",
                                     ", ".join(note.category_names) if note.category_names else "None")
        for extension in note.extensions:
            note_description += ("Extension:\n"
                                 "----------\n"
                                 "Content:\n"
                                 "{0}\n"
                                 "\n"
                                 "Name: {1}\n"
                                 "----------\n"
                                 ).format(extension.content, extension.name)
        self.view.init_notes_view(note_description)

    def edit_note(self, view):
        try:
            self.noteutil.edit(view.note.nindex, view.text_editor.get(1.0, tk.END))
            view.destroy()
        except nu.NoteError as e:
            tkmsgbox.showerror("Failed edit", message=e.args[0])

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
        webbrowser.open("https://github.com/JJamesWWang/noteutil")


if __name__ == "__main__":
    gui = tk.Tk()
    app = SearcherView(gui, None, None, None)
    gui.geometry("1600x900+160+90")
    gui.mainloop()


