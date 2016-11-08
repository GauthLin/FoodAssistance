from tkinter import *
from tkinter import ttk

from Entity.Windows.AddAliment import AddAliment


class Assistance:
    def __init__(self):
        self.root = Tk()
        self.root.title("Assistance de cuisine")
        self.root.configure(padx="10", pady="10")

    def start(self):
        self.display_window()

    def display_course_tab(self, tab):
        ttk.Button(tab, text="Ajouter un aliment", command=self.display_window_add_aliment) \
            .grid(column=0, row=0, sticky=(W, E))

    def display_window(self):
        # Tabs
        notebook = ttk.Notebook(self.root)
        tab_course = ttk.Frame(notebook)
        tab_timer = ttk.Frame(notebook)
        notebook.add(tab_course, text='Liste de courses')
        notebook.add(tab_timer, text='Minuteur')
        notebook.grid(column=0, row=0)

        # Liste de courses
        self.display_course_tab(tab_course)

        # Mainloop
        self.root.mainloop()

    def display_window_add_aliment(self):
        AddAliment(self.root).display()


if __name__ == '__main__':
    assistance = Assistance()
    assistance.start()
