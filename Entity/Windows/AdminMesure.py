from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from Manager.Window import Window


class AdminMesure:
    def __init__(self, root):
        self.window_manager = Window(root)

        self.name = StringVar()

        self.mesures_name = ['kg', 'g']
        self.mesures_name_var = StringVar(value=self.mesures_name)

    def display(self):
        """
        Affichage de la fenêtre qui permet d'ajouter et supprimer
        les différentes mesures (kg, g, sachet, paquet...)
        :return:
        """
        window = self.window_manager.create_default_window("Administration des mesures")
        ttk.Label(window, text="Nom de la mesure: ").grid(column=0, row=0, sticky=E)

        name_entry = ttk.Entry(window, textvariable=self.name, width=20)
        name_entry.grid(column=1, row=0, sticky=(W, E))

        ttk.Button(window, text="Ajouter", command=self.add).grid(column=2, row=0, sticky=W)

        lb_mesures = Listbox(window, listvariable=self.mesures_name_var, height=5)
        lb_mesures.grid(column=1, row=1, sticky=(W, E))

        lb_scrollbar = Scrollbar(window, orient=VERTICAL, command=lb_mesures.yview)
        lb_scrollbar.grid(column=2, row=1, sticky=(W, S, N))
        lb_mesures.configure(yscrollcommand=lb_scrollbar.set)

        ttk.Button(window, text="Supprimer", command=self.delete).grid(column=4, row=1, sticky=W)

    def add(self):
        name = self.name.get()
        if name in self.mesures_name:
            messagebox.showerror(None, "Cette mesure existe déjà !")
            return

        if name == "":
            messagebox.showerror(None, "Le nom de la mesure ne peut pas être vide !")
            return

        self.mesures_name.append(self.name.get())
        self.mesures_name_var.set(value=self.mesures_name)

        self.name.set("")

    def delete(self):
        pass
