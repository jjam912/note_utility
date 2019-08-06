"""The starting program that greets the user and then continues to the configurator."""
import tkinter as tk
from welcomer import Welcomer


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_popup = None
        self.entry_popup = None
        self.init_binds()

    def init_text_popup(self, event):
        self.text_popup = tk.Menu(event.widget, tearoff=False)
        self.text_popup.add_command(label="Undo", accelerator="Ctrl+Z",
                                    command=lambda: event.widget.event_generate("<<Undo>>"))
        self.text_popup.add_command(label="Redo", accelerator="Ctrl+Y",
                                    command=lambda: event.widget.event_generate("<<Redo>>"))
        self.text_popup.add_separator()
        self.text_popup.add_command(label="Cut", accelerator="Ctrl+X",
                                    command=lambda: event.widget.event_generate("<<Cut>>"))
        self.text_popup.add_command(label="Copy", accelerator="Ctrl+C",
                                    command=lambda: event.widget.event_generate("<<Copy>>"))
        self.text_popup.add_command(label="Paste", accelerator="Ctrl+V",
                                    command=lambda: event.widget.event_generate("<<Paste>>"))
        self.text_popup.add_command(label="Select All", accelerator="Ctrl+A",
                                    command=lambda: event.widget.event_generate("<<Select All>>"))

    def init_entry_popup(self, event):
        self.entry_popup = tk.Menu(event.widget, tearoff=False)
        self.entry_popup.add_command(label="Cut", accelerator="Ctrl+X",
                                     command=lambda: event.widget.event_generate("<<Cut>>"))
        self.entry_popup.add_command(label="Copy", accelerator="Ctrl+C",
                                     command=lambda: event.widget.event_generate("<<Copy>>"))
        self.entry_popup.add_command(label="Paste", accelerator="Ctrl+V",
                                     command=lambda: event.widget.event_generate("<<Paste>>"))
        self.entry_popup.add_command(label="Select All", accelerator="Ctrl+A",
                                     command=lambda: event.widget.event_generate("<<Select All>>"))

    def init_binds(self):
        self.bind_class(tk.Text.__name__, "<<Select All>>", lambda e: e.widget.tag_add(tk.SEL, 1.0, tk.END))
        self.bind_class(tk.Text.__name__, "<<Select All>>", lambda e: e.widget.tag_add(tk.SEL, 1.0, tk.END))
        self.bind_class(tk.Text.__name__, "<Control-Z>", lambda e: e.widget.event_generate("<<Undo>>"))
        self.bind_class(tk.Text.__name__, "<Control-z>", lambda e: e.widget.event_generate("<<Undo>>"))
        self.bind_class(tk.Text.__name__, "<Control-Y>", lambda e: e.widget.event_generate("<<Redo>>"))
        self.bind_class(tk.Text.__name__, "<Control-y>", lambda e: e.widget.event_generate("<<Redo>>"))
        self.bind_class(tk.Text.__name__, "<Control-A>", lambda e: e.widget.event_generate("<<Select All>>"))
        self.bind_class(tk.Text.__name__, "<Control-a>", lambda e: e.widget.event_generate("<<Select All>>"))
        self.bind_class(tk.Text.__name__, "<Button-3>", self.open_text_popup)

        self.bind_class(tk.Entry.__name__, "<<Select All>>", lambda e: e.widget.select_range(0, tk.END))
        self.bind_class(tk.Entry.__name__, "<<Select All>>", lambda e: e.widget.select_range(0, tk.END))
        self.bind_class(tk.Entry.__name__, "<Control-A>", lambda e: e.widget.event_generate("<<Select All>>"))
        self.bind_class(tk.Entry.__name__, "<Control-a>", lambda e: e.widget.event_generate("<<Select All>>"))
        self.bind_class(tk.Entry.__name__, "<Button-3>", self.open_entry_popup)

    def open_text_popup(self, event):
        self.init_text_popup(event)
        self.text_popup.tk_popup(event.x_root, event.y_root)
        return "break"

    def open_entry_popup(self, event):
        self.init_entry_popup(event)
        self.entry_popup.tk_popup(event.x_root, event.y_root)
        return "break"


if __name__ == "__main__":
    gui = Main()
    Welcomer(gui)

    gui.geometry("1600x900+160+90")
    gui.mainloop()
