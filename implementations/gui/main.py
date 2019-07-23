import tkinter as tk
import tkinter.font as tkfont
from configurator import ConfiguratorView


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("NoteUtil")
        self.root.bind("<Button-1>", self.navigate_config)

        self.noteutil_label = None
        self.continue_label = None
        self.init_labels()

    def init_labels(self):
        self.noteutil_label = tk.Label(self.root, text="NoteUtil", pady=100, fg="blue",
                                       font=tkfont.Font(family="Ubuntu", size=192, weight="bold", underline=True))
        self.continue_label = tk.Label(self.root, text="Click anywhere to\ncontinue", pady=50,
                                       font=tkfont.Font(family="Ubuntu", size=96))

        self.noteutil_label.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self.continue_label.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    def clear(self):
        self.root.unbind("<Button-1>")
        for widget in self.root.winfo_children():
            widget.destroy()

    def navigate_config(self, event):
        self.clear()
        ConfiguratorView(self.root)


if __name__ == "__main__":
    gui = tk.Tk()
    app = Main(gui)
    gui.geometry("1600x900+160+90")
    gui.mainloop()
