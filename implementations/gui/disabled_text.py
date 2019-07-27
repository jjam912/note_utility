import tkinter as tk


def switch(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        self.config(state=tk.NORMAL)
        return_ = func(*args, **kwargs)
        self.config(state=tk.DISABLED)
        return return_
    return wrapper


class DisabledText(tk.Text):
    def __init__(self, master=None, cnf: dict={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.config(state=tk.DISABLED)

    @switch
    def set(self, text, *args):
        super().delete(1.0, tk.END)
        super().insert(tk.END, text, *args)

    @switch
    def insert(self, index, chars, *args):
        super().insert(index, chars, *args)

    @switch
    def delete(self, index1, index2=None):
        super().delete(index1, index2)
