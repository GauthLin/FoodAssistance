from tkinter import *
from tkinter import ttk

from Entity.Windows.AdminMesure import AdminMesure
from Manager.Window import Window


class AddAliment:
    def __init__(self, root):
        self.root = root
        self.window_manager = Window(root)

    def display(self):
        """
        Affichage de la fenêtre d'ajout d'alimentation
        :return:
        """
        window = self.window_manager.create_default_window("Ajout d'un aliment")
        ttk.Button(window, text="Administration des quantités", command=self.display_window_admin_quantity)\
            .grid(column=0, row=0, sticky=W)

    def display_window_admin_quantity(self):
        AdminMesure(self.root).display()
