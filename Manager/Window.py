from tkinter import *


class Window:
    def __init__(self, root):
        self.root = root

    def create_default_window(self, title):
        window = Toplevel(self.root)
        window.title(title)
        window.configure(padx="10", pady="10")

        return window
