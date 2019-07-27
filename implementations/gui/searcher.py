import tkinter as tk
import tkinter.font as tkfont


class SearcherView:
    def __init__(self, root: tk.Tk, noteutil, quiz, leitner):
        self.root = root
        self.root.title("NoteUtil Searcher")
        self.controller = SearcherController(self, noteutil, quiz, leitner)

        self.menu_bar = None
        self.init_menu_bar()

        self.by_eval = tk.BooleanVar()
        self.by_eval_button = None
        self.by_content = tk.BooleanVar(value=True)
        self.by_content_button = None
        self.by_rcontent = tk.BooleanVar()
        self.by_rcontent_button = None
        self.by_nindex = tk.BooleanVar()
        self.by_nindex_button = None
        self.by_is_pair = tk.BooleanVar()
        self.by_is_pair_button = None
        self.by_is_heading = tk.BooleanVar()
        self.by_is_heading_button = None
        self.by_has_extensions = tk.BooleanVar()
        self.by_has_extensions_button = None
        self.by_has_categories = tk.BooleanVar()
        self.by_has_categories_button = None
        self.init_main_compare()

        self.if_equals = tk.BooleanVar()
        self.if_equals_button = None
        self.if_similar = tk.BooleanVar()
        self.if_similar_button = None
        self.if_in = tk.BooleanVar()
        self.if_in_button = None
        self.if_simin = tk.BooleanVar(value=True)
        self.if_simin_button = None
        self.if_less = tk.BooleanVar()
        self.if_less_button = None
        self.if_lesse = tk.BooleanVar()
        self.if_lesse_button = None
        self.if_greater = tk.BooleanVar()
        self.if_greater_button = None
        self.if_greatere = tk.BooleanVar()
        self.if_greatere_button = None
        self.init_compare_options()

        self.and_this = tk.BooleanVar()
        self.and_this_button = None
        self.or_this = tk.BooleanVar()
        self.or_this_button = None
        self.init_narrow_options()

        # Pair
        self.by_term = tk.BooleanVar()
        self.by_term_button = None
        self.by_definition = tk.BooleanVar()
        self.by_definition_button = None
        # Heading
        self.by_heading = tk.BooleanVar()
        self.by_heading_button = None
        self.by_level = tk.BooleanVar()
        self.by_level_button = None
        self.by_level_name = tk.BooleanVar()
        self.by_level_name_button = None
        self.by_begin_nindex = tk.BooleanVar()
        self.by_begin_nindex_button = None
        self.by_end_nindex = tk.BooleanVar()
        self.by_end_nindex_button = None
        # Extension
        self.by_extension_names = tk.BooleanVar()
        self.by_extension_names_button = None
        # Category
        self.by_category_names = tk.BooleanVar()
        self.by_category_names_button = None
        self.init_sub_compare()

        self.search_bar = None
        self.search_button = None
        self.search_icon = None
        self.init_search_bar()

        self.results_list = None
        self.init_results_list()

        self.modify_grid()

    def init_menu_bar(self):
        self.menu_bar = tk.Menu(self.root, tearoff=False)
        self.init_notes_menu()
        self.init_view_menu()
        self.init_navigate_menu()
        self.init_tools_menu()
        self.init_help_menu()
        self.root.config(menu=self.menu_bar)

    def init_notes_menu(self):
        notes_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Notes", menu=notes_menu)

    def init_view_menu(self):
        view_menu = tk.Menu(self.menu_bar, tearoff=False)
        view_menu.add_command(label="Change output format", command=self.controller.on_change_output_format)
        self.menu_bar.add_cascade(label="View", menu=view_menu)

    def init_navigate_menu(self):
        navigate_menu = tk.Menu(self.menu_bar, tearoff=False)
        navigate_menu.add_command(label="Go to configurator", command=self.controller.on_to_configurator)
        navigate_menu.add_command(label="Go to editor", command=self.controller.on_to_editor)
        navigate_menu.add_command(label="Go to quizzer", command=self.controller.on_to_quizzer)
        navigate_menu.add_command(label="Go to reviewer", command=self.controller.on_to_reviewer)
        self.menu_bar.add_cascade(label="Navigate", menu=navigate_menu)

    def init_tools_menu(self):
        tools_menu = tk.Menu(self.menu_bar, tearoff=False)
        tools_menu.add_command(label="View image link", command=self.controller.on_view_image_link)
        tools_menu.add_command(label="Font selector", command=self.controller.on_font_selector)
        tools_menu.add_command(label="Display LaTeX", command=self.controller.on_display_latex)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

    def init_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        help_menu.add_command(label="Search by explanation", command=self.controller.on_search_explanation)
        help_menu.add_command(label="Compare by explanation", command=self.controller.on_compare_explanation)
        help_menu.add_command(label="Narrow with explanation", command=self.controller.on_narrow_explanation)
        help_menu.add_command(label="About", command=self.controller.on_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def init_main_compare(self):
        search_frame = tk.LabelFrame(self.root, text="Search by:")
        self.by_eval_button = tk.Checkbutton(search_frame, variable=self.by_eval, text="Eval")
        self.by_eval_button.grid(row=0, column=0, sticky=tk.W)
        self.by_content_button = tk.Checkbutton(search_frame, variable=self.by_content, text="Content")
        self.by_content_button.grid(row=1, column=0, sticky=tk.W)
        self.by_rcontent_button = tk.Checkbutton(search_frame, variable=self.by_rcontent, text="Raw content")
        self.by_rcontent_button.grid(row=2, column=0, sticky=tk.W)
        self.by_nindex_button = tk.Checkbutton(search_frame, variable=self.by_nindex, text="Note index")
        self.by_nindex_button.grid(row=3, column=0, sticky=tk.W)
        self.by_is_pair_button = tk.Checkbutton(search_frame, variable=self.by_is_pair, text="Is pair",
                                                command=self.controller.on_is_pair)
        self.by_is_pair_button.grid(row=0, column=1, sticky=tk.W)
        self.by_is_heading_button = tk.Checkbutton(search_frame, variable=self.by_is_heading, text="Is heading",
                                                   command=self.controller.on_is_heading)
        self.by_is_heading_button.grid(row=1, column=1, sticky=tk.W)
        self.by_has_extensions_button = tk.Checkbutton(search_frame, variable=self.by_has_extensions,
                                                       text="Has extensions", command=self.controller.on_has_extensions)
        self.by_has_extensions_button.grid(row=2, column=1, sticky=tk.W)
        self.by_has_categories_button = tk.Checkbutton(search_frame, variable=self.by_has_categories,
                                                       text="Has categories", command=self.controller.on_has_categories)
        self.by_has_categories_button.grid(row=3, column=1, sticky=tk.W)
        search_frame.grid(row=0, column=1, sticky=tk.EW)

    def init_compare_options(self):
        compare_frame = tk.LabelFrame(self.root, text="Compare by:")
        self.if_equals_button = tk.Checkbutton(compare_frame, variable=self.if_equals, text="Equals")
        self.if_equals_button.grid(row=0, column=0, sticky=tk.W)
        self.if_similar_button = tk.Checkbutton(compare_frame, variable=self.if_similar, text="Similar")
        self.if_similar_button.grid(row=1, column=0, sticky=tk.W)
        self.if_in_button = tk.Checkbutton(compare_frame, variable=self.if_in, text="In")
        self.if_in_button.grid(row=2, column=0, sticky=tk.W)
        self.if_simin_button = tk.Checkbutton(compare_frame, variable=self.if_simin, text="Similar in")
        self.if_simin_button.grid(row=3, column=0, sticky=tk.W)
        self.if_less_button = tk.Checkbutton(compare_frame, variable=self.if_less, text="Less than")
        self.if_less_button.grid(row=0, column=1, sticky=tk.W)
        self.if_lesse_button = tk.Checkbutton(compare_frame, variable=self.if_lesse, text="Less/Equal")
        self.if_lesse_button.grid(row=1, column=1, sticky=tk.W)
        self.if_greater_button = tk.Checkbutton(compare_frame, variable=self.if_greater, text="Greater than")
        self.if_greater_button.grid(row=2, column=1, sticky=tk.W)
        self.if_greatere_button = tk.Checkbutton(compare_frame, variable=self.if_greatere, text="Greater/Equal")
        self.if_greatere_button.grid(row=3, column=1, sticky=tk.W)
        compare_frame.grid(row=0, column=2, sticky=tk.EW)

    def init_narrow_options(self):
        narrow_frame = tk.LabelFrame(self.root, text="Narrow with:")
        self.or_this_button = tk.Checkbutton(narrow_frame, variable=self.or_this, text="Or", state=tk.DISABLED)
        self.or_this_button.grid(row=0, column=0, sticky=tk.W)
        self.and_this_button = tk.Checkbutton(narrow_frame, variable=self.and_this, text="And", state=tk.DISABLED)
        self.and_this_button.grid(row=1, column=0, sticky=tk.W)
        narrow_frame.grid(row=0, column=3, columnspan=2, padx=(0, 20), sticky=tk.NSEW)

    def init_sub_compare(self):
        subsearch_frame = tk.LabelFrame(self.root, text="Search by:")
        self.by_term_button = tk.Checkbutton(subsearch_frame, variable=self.by_term,
                                             text="Term", state=tk.DISABLED)
        self.by_term_button.grid(row=0, column=0, sticky=tk.W)
        self.by_definition_button = tk.Checkbutton(subsearch_frame, variable=self.by_definition,
                                                   text="Definition", state=tk.DISABLED)
        self.by_definition_button.grid(row=1, column=0, sticky=tk.W)
        self.by_heading_button = tk.Checkbutton(subsearch_frame, variable=self.by_heading,
                                                text="Heading", state=tk.DISABLED)
        self.by_heading_button.grid(row=2, column=0, sticky=tk.W)
        self.by_level_button = tk.Checkbutton(subsearch_frame, variable=self.by_level,
                                              text="Level", state=tk.DISABLED)
        self.by_level_button.grid(row=3, column=0, sticky=tk.W)
        self.by_level_name_button = tk.Checkbutton(subsearch_frame, variable=self.by_level_name,
                                                   text="Level name", state=tk.DISABLED)
        self.by_level_name_button.grid(row=4, column=0, sticky=tk.W)
        self.by_begin_nindex_button = tk.Checkbutton(subsearch_frame, variable=self.by_begin_nindex,
                                                     text="Begin note index", state=tk.DISABLED)
        self.by_begin_nindex_button.grid(row=5, column=0, sticky=tk.W)
        self.by_end_nindex_button = tk.Checkbutton(subsearch_frame, variable=self.by_end_nindex,
                                                   text="End note index", state=tk.DISABLED)
        self.by_end_nindex_button.grid(row=6, column=0, sticky=tk.W)
        self.by_extension_names_button = tk.Checkbutton(subsearch_frame, variable=self.by_extension_names,
                                                        text="Extension names", state=tk.DISABLED)
        self.by_extension_names_button.grid(row=7, column=0, sticky=tk.W)
        self.by_category_names_button = tk.Checkbutton(subsearch_frame, variable=self.by_category_names,
                                                       text="Category names", state=tk.DISABLED)
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
        self.search_bar.bind("<Control-a>", self.search_bar_select_all)
        self.search_bar.bind("<Control-A>", self.search_bar_select_all)

    def search_bar_select_all(self, event=None):
        self.search_bar.select_range(0, tk.END)
        self.search_bar.icursor(tk.END)
        return "break"

    def init_results_list(self):
        self.results_list = tk.Listbox(self.root, activestyle="dotbox", listvariable=self.controller.notes,
                                       selectmode=tk.SINGLE, font=tkfont.Font(family="Ubuntu", size=12))
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

    def clear(self):
        self.root.unbind("<Button-1>")
        for widget in self.root.winfo_children():
            widget.destroy()


class SearcherController:
    # TODO: Each Checkbox limits what other checkboxes may be checked. Implement this? (literally will take 30 hours)
    def __init__(self, view, noteutil, quiz, leitner):
        self.count = 0
        self.view = view
        self.notes = tk.StringVar()
        self.noteutil = noteutil
        self.quiz = quiz
        self.leitner = leitner

    def on_change_output_format(self):
        self.count += 1
        print(self.count)

    def on_to_configurator(self):
        from configurator import ConfiguratorView
        self.view.clear()
        ConfiguratorView(self.view.root)

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

    def on_view_image_link(self):
        self.count += 1
        print(self.count)

    def on_font_selector(self):
        self.count += 1
        print(self.count)

    def on_display_latex(self):
        self.count += 1
        print(self.count)

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

    def set_checkbuttons(self, state, *buttons):
        for button in buttons:
            button.config(state=state)

    def on_is_pair(self):
        if self.view.by_is_pair.get():
            self.set_checkbuttons(tk.NORMAL, self.view.by_term_button, self.view.by_definition_button)
        else:
            self.set_checkbuttons(tk.DISABLED, self.view.by_term_button, self.view.by_definition_button)

    def on_is_heading(self):
        if self.view.by_is_heading.get():
            self.set_checkbuttons(tk.NORMAL, self.view.by_heading_button, self.view.by_level_button,
                                  self.view.by_level_name_button, self.view.by_begin_nindex_button,
                                  self.view.by_end_nindex_button)
        else:
            self.set_checkbuttons(tk.DISABLED, self.view.by_heading_button, self.view.by_level_button,
                                  self.view.by_level_name_button, self.view.by_begin_nindex_button,
                                  self.view.by_end_nindex_button)

    def on_has_extensions(self):
        if self.view.by_has_extensions.get():
            self.set_checkbuttons(tk.NORMAL, self.view.by_extension_names_button)
        else:
            self.set_checkbuttons(tk.DISABLED, self.view.by_extension_names_button)

    def on_has_categories(self):
        if self.view.by_has_categories.get():
            self.set_checkbuttons(tk.NORMAL, self.view.by_category_names_button)
        else:
            self.set_checkbuttons(tk.DISABLED, self.view.by_category_names_button)

    def on_search(self, event=None):
        self.count += 1
        print(self.count)
        return "break"


if __name__ == "__main__":
    gui = tk.Tk()
    app = SearcherView(gui, None, None, None)
    gui.geometry("1600x900+160+90")
    gui.mainloop()


