from tkinter import *
from tkinter import ttk

from Entity.Windows.AddAliment import AddAliment
from Entity.Windows.AdminMesure import AdminMesure


class Assistance:
    def __init__(self):
        self.root = Tk()
        self.root.title("Assistance de cuisine")
        self.root.configure(padx="10", pady="10")
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))

    def start(self):
        self.display_window()

    def display_course_tab(self, tab):
        ttk.Button(tab, text="Ajouter un aliment", command=self.display_window_add_aliment) \
            .grid(column=0, row=0, sticky=(W, E))

    def display_config_tab(self, tab):
        ttk.Button(tab, text="Administration des quantités", command=self.display_window_admin_quantity)\
            .grid(column=0, row=0, sticky=W)

    def display_window_admin_quantity(self):
        AdminMesure(self.root).display()

    def display_window(self):
        # Tabs
        notebook = ttk.Notebook(self.root)
        tab_course = ttk.Frame(notebook)
        tab_timer = ttk.Frame(notebook)
        tab_config = ttk.Frame(notebook)
        notebook.add(tab_course, text='Liste de courses')
        notebook.add(tab_timer, text='Minuteur')
        notebook.add(tab_config, text='Configuration')
        notebook.grid(column=0, row=0)

        # Liste de courses
        self.display_course_tab(tab_course)
        self.display_config_tab(tab_config)

        # Mainloop
        self.root.mainloop()

    def display_window_add_aliment(self):
        AddAliment(self.root).display()


if __name__ == '__main__':
    assistance = Assistance()
    assistance.start()
