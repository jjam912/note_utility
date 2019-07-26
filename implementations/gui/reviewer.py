import tkinter as tk
import tkinter.font as tkfont
from disabled_text import DisabledText


class ReviewerView:
    def __init__(self, root, noteutil, quiz, leitner):
        self.root = root
        self.root.title("NoteUtil Reviewer")
        self.controller = ReviewerController(self, noteutil, quiz, leitner)

        self.menu_bar = None
        self.reveal_label = None
        self.init_menu_bar()

        self.current_session = tk.StringVar(value="Current session: None")
        self.reviewing_boxes = tk.StringVar(value="Reviewing boxes: None")
        self.session_label = None
        self.boxes_label = None
        self.generate_button = None
        self.init_top_frame()

        self.term_text = None
        self.init_term_text()

        self.definition_text = None
        self.init_definition_text()

        self.reveal_button = None
        self.correct_button = None
        self.incorrect_button = None
        self.init_button_frame()

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
        tools_menu.add_command(label="View image link", command=self.controller.on_view_image_link)
        tools_menu.add_command(label="Font selector", command=self.controller.on_font_selector)
        tools_menu.add_command(label="Display LaTeX", command=self.controller.on_display_latex)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)

    def init_settings_menu(self):
        settings_menu = tk.Menu(self.menu_bar, tearoff=False)
        settings_menu.add_command(label="Append box", command=self.controller.on_append_box)
        settings_menu.add_command(label="Pop box", command=self.controller.on_pop_box)
        settings_menu.add_command(label="Edit box", command=self.controller.on_edit_box)
        settings_menu.add_separator()

        settings_menu.add_checkbutton(label="Randomize terms", variable=self.controller.random)
        settings_menu.add_checkbutton(label="Display term first", variable=self.controller.term_first)
        settings_menu.add_checkbutton(label="Include extensions", variable=self.controller.include_extensions)
        settings_menu.add_command(label="Set term format", command=self.controller.on_set_term_format)
        settings_menu.add_command(label="Set definition format", command=self.controller.on_set_definition_format)
        settings_menu.add_command(label="Set extension format", command=self.controller.on_set_extension_format)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)

    def init_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=False)
        help_menu.add_command(label="What is this?", command=self.controller.on_what_is_this)
        help_menu.add_command(label="About", command=self.controller.on_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def init_top_frame(self):
        top_frame = tk.Frame(self.root)
        self.session_label = tk.Label(top_frame, textvariable=self.current_session)
        self.session_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.generate_button = tk.Button(top_frame, text="Generate", command=self.controller.on_generate)
        self.generate_button.pack(side=tk.LEFT, fill=tk.X)
        self.boxes_label = tk.Label(top_frame, textvariable=self.reviewing_boxes)
        self.boxes_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))

    def init_term_text(self):
        term_frame = tk.LabelFrame(self.root, text="Term", padx=10, pady=10, labelanchor=tk.N)
        self.term_text = DisabledText(term_frame, wrap=tk.WORD, state=tk.DISABLED, width=1, height=1,
                                      font=tkfont.Font(family="Ubuntu", size=12))
        yscrollbar = tk.Scrollbar(term_frame, orient=tk.VERTICAL, command=self.term_text.yview)
        self.term_text.config(yscrollcommand=yscrollbar.set)
        self.term_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        term_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)
        self.term_text.insert(tk.END, "The term will be given here.")

    def init_definition_text(self):
        definition_frame = tk.LabelFrame(self.root, text="Definition", padx=10, pady=10, labelanchor=tk.N)
        self.definition_text = DisabledText(definition_frame, wrap=tk.WORD, state=tk.DISABLED, width=1, height=1,
                                            font=tkfont.Font(family="Ubuntu", size=12))
        yscrollbar = tk.Scrollbar(definition_frame, orient=tk.VERTICAL, command=self.definition_text.yview)
        self.definition_text.config(yscrollcommand=yscrollbar.set)
        self.definition_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        definition_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, expand=True)
        self.definition_text.insert(tk.END, "The definition will be displayed here.")

    def init_button_frame(self):
        button_frame = tk.Frame(self.root)
        self.correct_button = tk.Button(button_frame, text="Correct", bd=5, command=self.controller.on_add_correct)
        self.correct_button.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.X, expand=True)
        self.reveal_button = tk.Button(button_frame, text="Reveal", bd=5, command=self.controller.on_reveal)
        self.reveal_button.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.incorrect_button = tk.Button(button_frame, text="Incorrect", bd=5, command=self.controller.on_add_incorrect)
        self.incorrect_button.pack(side=tk.LEFT, padx=(0, 10), pady=10, fill=tk.X, expand=True)
        button_frame.pack(side=tk.TOP, fill=tk.X)

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

        self.random = tk.BooleanVar(value=True)
        self.term_first = tk.BooleanVar(value=True)
        self.include_extensions = tk.BooleanVar(value=True)
        self.reveal = True

    def on_generate(self):
        self.count += 1
        print(self.count)

    def on_reveal(self):
        option_menu = self.view.menu_bar.winfo_children()[0]
        if self.reveal:
            self.view.reveal_button.config(text="Continue")
            option_menu.entryconfigure(2, label="Continue")
        else:
            self.view.reveal_button.config(text="Reveal")
            option_menu.entryconfigure(2, label="Reveal")
        self.reveal = not self.reveal

    def on_add_correct(self):
        self.view.term_text.insert(tk.END, "Heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy :) ")

    def on_add_incorrect(self):
        self.view.term_text.delete(1.0, tk.END)

    def on_view_boxes(self):
        self.count += 1
        print(self.count)

    def on_view_notes(self):
        self.count += 1
        print(self.count)

    def on_load(self):
        self.count += 1
        print(self.count)

    def on_save(self):
        self.count += 1
        print(self.count)

    def on_reset(self):
        self.count += 1
        print(self.count)

    def on_edit_note(self):
        self.count += 1
        print(self.count)

    def on_quick_search(self):
        self.count += 1
        print(self.count)

    def on_to_configurator(self):
        from configurator import ConfiguratorView
        self.view.clear()
        ConfiguratorView(self.view.root)

    def on_to_editor(self):
        from editor import EditorView
        self.view.clear()
        EditorView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_to_searcher(self):
        from searcher import SearcherView
        self.view.clear()
        SearcherView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_to_quizzer(self):
        from quizzer import QuizzerView
        self.view.clear()
        QuizzerView(self.view.root, self.noteutil, self.quiz, self.leitner)

    def on_view_image_link(self):
        self.count += 1
        print(self.count)

    def on_font_selector(self):
        self.count += 1
        print(self.count)

    def on_display_latex(self):
        self.count += 1
        print(self.count)

    def on_append_box(self):
        self.count += 1
        print(self.count)

    def on_pop_box(self):
        self.count += 1
        print(self.count)

    def on_edit_box(self):
        self.count += 1
        print(self.count)

    def on_set_term_format(self):
        self.count += 1
        print(self.count)

    def on_set_definition_format(self):
        self.count += 1
        print(self.count)

    def on_set_extension_format(self):
        self.count += 1
        print(self.count)

    def on_what_is_this(self):
        self.count += 1
        print(self.count)

    def on_about(self):
        self.count += 1
        print(self.count)


if __name__ == "__main__":
    gui = tk.Tk()
    app = ReviewerView(gui, None, None, None)
    gui.geometry("1600x900+160+90")
    gui.mainloop()
