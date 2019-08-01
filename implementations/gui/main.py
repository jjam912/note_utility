"""The starting program that greets the user and then continues to the configurator."""
import tkinter as tk
import tkinter.font as tkfont
from configurator import ConfiguratorView


class Main:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("NoteUtil")
        self.root.bind("<Button-1>", self.to_configurator)

        self.noteutil_label = None
        self.continue_label = None
        self.init_labels()
        self.popup_menu = None
        self.init_binds()

    def init_popup_menu(self, event):
        self.popup_menu = tk.Menu(event.widget, tearoff=False)
        self.popup_menu.add_command(label="Undo", accelerator="Ctrl+Z",
                                    command=lambda: event.widget.event_generate("<<Undo>>"))
        self.popup_menu.add_command(label="Redo", accelerator="Ctrl+Y",
                                    command=lambda: event.widget.event_generate("<<Redo>>"))
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Cut", accelerator="Ctrl+X",
                                    command=lambda: event.widget.event_generate("<<Cut>>"))
        self.popup_menu.add_command(label="Copy", accelerator="Ctrl+C",
                                    command=lambda: event.widget.event_generate("<<Copy>>"))
        self.popup_menu.add_command(label="Paste", accelerator="Ctrl+V",
                                    command=lambda: event.widget.event_generate("<<Paste>>"))
        self.popup_menu.add_command(label="Select All", accelerator="Ctrl+A",
                                    command=lambda: event.widget.event_generate("<<Select All>>"))

    def init_labels(self):
        self.noteutil_label = tk.Label(self.root, text="NoteUtil", pady=100, fg="blue",
                                       font=tkfont.Font(family="Ubuntu", size=192, weight="bold", underline=True))
        self.continue_label = tk.Label(self.root, text="Click anywhere to\ncontinue", pady=50,
                                       font=tkfont.Font(family="Ubuntu", size=96))

        self.noteutil_label.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.continue_label.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def init_binds(self):
        self.root.bind_class(tk.Text.__name__, "<<Select All>>", lambda e: e.widget.tag_add(tk.SEL, 1.0, tk.END))
        self.root.bind_class(tk.Text.__name__, "<<Select All>>", lambda e: e.widget.tag_add(tk.SEL, 1.0, tk.END))
        self.root.bind_class(tk.Text.__name__, "<Control-Z>", lambda e: e.widget.event_generate("<<Undo>>"))
        self.root.bind_class(tk.Text.__name__, "<Control-z>", lambda e: e.widget.event_generate("<<Undo>>"))
        self.root.bind_class(tk.Text.__name__, "<Control-Y>", lambda e: e.widget.event_generate("<<Redo>>"))
        self.root.bind_class(tk.Text.__name__, "<Control-y>", lambda e: e.widget.event_generate("<<Redo>>"))
        self.root.bind_class(tk.Text.__name__, "<Control-A>", lambda e: e.widget.event_generate("<<Select All>>"))
        self.root.bind_class(tk.Text.__name__, "<Control-a>", lambda e: e.widget.event_generate("<<Select All>>"))
        self.root.bind_class(tk.Text.__name__, "<Button-3>", self.popup)

        self.root.bind_class(tk.Entry.__name__, "<<Select All>>", lambda e: e.widget.select_range(0, tk.END))
        self.root.bind_class(tk.Entry.__name__, "<<Select All>>", lambda e: e.widget.select_range(0, tk.END))
        self.root.bind_class(tk.Entry.__name__, "<Control-A>", lambda e: e.widget.event_generate("<<Select All>>"))
        self.root.bind_class(tk.Entry.__name__, "<Control-a>", lambda e: e.widget.event_generate("<<Select All>>"))
        self.root.bind_class(tk.Entry.__name__, "<Button-3>", self.popup)

    def popup(self, event):
        self.init_popup_menu(event)
        self.popup_menu.tk_popup(event.x_root, event.y_root)
        return "break"

    def clear(self):
        """Removes all of the root's children"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def to_configurator(self, event=None):
        """Clears the root and then instantiates the ConfiguratorView."""
        self.root.unbind("<Button-1>")
        self.clear()
        ConfiguratorView(self.root)


if __name__ == "__main__":
    gui = tk.Tk()
    app = Main(gui)
    gui.geometry("1600x900+160+90")
    gui.mainloop()
