from tkinter import *
from tkinter import ttk

from Manager.Window import Window


class AddFood:
    def __init__(self, root):
        self.root = root
        self.window_manager = Window(root)
        self.measuringUnits = ('', 'g', 'kg', 'l', 'cl', 'ml', 'sachet', 'paquet')

    def display(self):
        """
        Affichage de la fenêtre d'ajout d'alimentation
        :return:
        """
        window = self.window_manager.create_default_window("Ajout d'un aliment")
