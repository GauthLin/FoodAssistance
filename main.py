import multiprocessing
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from Entity.Food import Food
from Manager.DBManager import DBManager
from Manager.FoodManager import FoodManager
from Manager.GmailManager import GmailManager
from Repository.FoodRepository import FoodRepository
from time import sleep

from Repository.UserRepository import UserRepository


class Assistance:
    def __init__(self):
        self.root = Tk()
        self.root.title("Assistance de cuisine")
        self.root.configure(padx="10", pady="10")

        self.food_repository = FoodRepository()
        self.user_repository = UserRepository()
        self.db_manager = DBManager()
        self.db_manager.init()
        self.food_manager = FoodManager()
        self.gmail = GmailManager()

        self.measuring_units = ('', 'g', 'kg', 'l', 'cl', 'ml', 'sachet', 'paquet', 'bouteille')
        self.foods = self.food_repository.get_foods()  # Liste des aliments dans la liste des courses
        self.mail_sender_accept = self.user_repository.get_users_mails()

    def start(self):
        self.display_window()

    def display_course_tab(self, tab):
        """ Affiche l'onglet "Liste de courses" """

        # Formulaire d'ajout de nourriture
        add_frame = Frame(tab)
        add_frame.grid(column=0, row=0, sticky=(W, E), padx=15, pady=10)

        food_name_var = StringVar()
        food_name_entry = ttk.Entry(add_frame, textvariable=food_name_var)
        food_name_entry.grid(column=0, row=0, sticky=(W, E))
        food_name_entry.configure(width=40)
        self.add_placeholder(food_name_entry, "Nom de l'aliment...")

        food_quantity_var = StringVar()
        food_quantity_spinbox = Spinbox(add_frame, textvariable=food_quantity_var, from_=0.0, to_=1000.0)
        food_quantity_spinbox.configure(width=10)
        food_quantity_spinbox.grid(column=1, row=0, padx=10)

        food_measuring_units_cb = ttk.Combobox(add_frame, values=self.measuring_units, state='readonly')
        food_measuring_units_cb.configure(width=10)
        food_measuring_units_cb.grid(column=2, row=0)

        food_add_btn = ttk.Button(add_frame, text="Ajouter l'aliment")
        foods_tree = ttk.Treeview(tab, columns=('id', 'quantity', 'unit', 'food'))

        def add_food(event=None):
            """ Fonction appelée lorsque l'utilisateur clique sur "Ajouter l'aliment" """
            food_add_btn.config(state='disabled')

            food_name = food_name_var.get().strip()

            # Vérification du nom de l'aliment
            if len(food_name) == 0 or food_name == "Nom de l'aliment...":
                messagebox.showerror(None, "Le nom de l'aliment ne peut pas être vide !")
                food_add_btn.config(state='normal')
                return

            if len(food_name) > 20:
                messagebox.showerror(None, "Le nom de l'aliment ne peut pas contenir plus de 20 caractères !")
                food_add_btn.config(state='normal')
                return

            # Vérification des quantités
            food_quantity = food_quantity_var.get().strip()
            if not food_quantity.isnumeric():
                messagebox.showerror(None, "La quantité doit être un nombre !")
                food_add_btn.config(state='normal')
                food_quantity_var.set(0)
                return

            food_quantity = float(food_quantity)
            if food_quantity < 0:
                messagebox.showerror(None, "La quantité ne peut pas être un nombre négatif !")
                food_add_btn.config(state='normal')
                return

            new_food = Food(food_name, food_quantity, food_measuring_units_cb.get())
            self.food_repository.save(new_food)
            self.foods.append(new_food)

            foods_tree.insert('', 'end',
                              values=(new_food.id, new_food.quantity, new_food.measuring_units, new_food.name))

            food_name_var.set('')
            food_name_entry.focus()
            food_quantity_var.set(0)
            food_measuring_units_cb.current(0)

            food_add_btn.config(state='normal')

        food_add_btn.config(command=add_food)
        food_add_btn.grid(column=4, row=0, padx=(10, 0))

        # Liste des courses
        tree_scroll = ttk.Scrollbar(tab)
        tree_scroll.grid(column=1, row=1, sticky=(S, N))
        tree_scroll.configure(command=foods_tree.yview)
        foods_tree.configure(yscrollcommand=tree_scroll.set)
        foods_tree['show'] = 'headings'
        foods_tree.heading('quantity', text='#')
        foods_tree.column('quantity', width=10)
        foods_tree.heading('unit', text='Unité')
        foods_tree.column('unit', width=10)
        foods_tree.heading('food', text='Aliment')
        foods_tree.column('food', width=400)
        foods_tree.configure(displaycolumns=('quantity', 'unit', 'food'))
        foods_tree.grid(column=0, row=1, sticky=(W, E))

        #  Bouton de suppression d'un aliment et d'envoie
        actions_frame = Frame(tab)
        actions_frame.grid(column=0, row=3, sticky=(W, E))
        actions_frame.configure(background='lightgrey', pady=10, padx=10)

        send_btn = Button(actions_frame, text='Envoyer la liste', command=self.send_foods)
        send_btn.grid(column=0, row=0)
        send_btn.configure(background='darkgreen', foreground='white')

        def delete_selected_food():
            if len(foods_tree.selection()) == 0:
                return

            answer = messagebox.askquestion(None, 'Êtes-vous sûr de vouloir supprimer cette aliment de la liste ?')
            if answer == 'no':
                return

            for item in foods_tree.selection():
                food_id = foods_tree.item(item, 'values')[0]

                for food in self.foods:
                    if int(food.id) == int(food_id):
                        self.food_repository.delete(food)
                        self.foods.remove(food)
                        foods_tree.delete(item)
                        del food
                        break

        delete_selected_food = Button(actions_frame, text="Supprimer l'aliment",
                                      command=delete_selected_food)
        delete_selected_food.grid(column=1, row=0, padx=10)
        delete_selected_food.configure(background='#FF9D00', foreground='white')

        def delete_all_foods():
            if len(foods_tree.get_children()) == 0:
                return

            answer = messagebox.askquestion(None, 'Êtes-vous sûr de vouloir supprimer tous les aliments de la liste ?')
            if answer == 'no':
                return

            for item in foods_tree.get_children():
                food_id = foods_tree.item(item, 'values')[0]

                for food in self.foods:
                    if int(food.id) == int(food_id):
                        self.food_repository.delete(food)
                        self.foods.remove(food)
                        foods_tree.delete(item)
                        del food
                        break

        delete_all_foods = Button(actions_frame, text='Supprimer tous les aliments de la liste',
                                  command=delete_all_foods)
        delete_all_foods.grid(column=2, row=0)
        delete_all_foods.configure(background='darkred', foreground='white')

        for food in self.foods:
            foods_tree.insert('', 'end', values=(food.id, food.quantity, food.measuring_units, food.name))

        # Bindings event
        food_name_entry.bind('<Return>', add_food)
        food_quantity_spinbox.bind('<Return>', add_food)
        food_measuring_units_cb.bind('<Return>', add_food)

    def send_foods(self):
        """
        Envoi la liste des courses à tous les utilisateurs
        """
        for mail in self.mail_sender_accept:
            self.gmail.send(mail, self.foods)

    def display_config_tab(self, tab):
        """
        Affiche l'onglet de "Configuration"
        """
        config_label = ttk.Label(tab, text="Utilisateurs")
        config_label.grid(column=0, row=0, padx=10, pady=10)

        user_mail_var = StringVar()
        user_email_entry = ttk.Entry(tab, textvariable=user_mail_var)
        user_email_entry.grid(column=1, row=0, sticky=(W, E))
        user_email_entry.config(width=40)
        self.add_placeholder(user_email_entry, 'Adresse mail...')

        add_user_mail_btn = ttk.Button(tab, text="Ajouter l'adresse mail")
        add_user_mail_btn.grid(column=2, row=0, padx=(5, 0))

        users_mails__sb = Scrollbar(tab)
        users_mails__sb.grid(column=2, row=1, sticky=(W, N, S))

        users_mails_lb = Listbox(tab, yscrollcommand=users_mails__sb.set)
        users_mails_lb.grid(column=1, row=1, sticky=(W, E))

        users_mails__sb.config(command=users_mails_lb.yview)

        def add_mail(event=None):
            mail = user_mail_var.get().strip()
            if mail == 'Adresse mail...' or mail == '':
                messagebox.showerror(None, "L'adresse mail ne peut pas être vide !")
                return

            if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail):
                messagebox.showerror(None, "L'adresse mail n'a pas un format valide !")
                return

            self.user_repository.add_mail(mail)
            self.mail_sender_accept.append(mail)
            users_mails_lb.insert('end', mail)
            user_mail_var.set('')

        def del_mail():
            for item in users_mails_lb.curselection():
                mail = users_mails_lb.get(item)
                question = messagebox.askquestion(None,
                                                  "Êtes-vous sûr(e) de vouloir supprimer l'adresse mail %s de la liste ?" % mail)

                if question == 'yes':
                    self.mail_sender_accept.remove(mail)
                    users_mails_lb.delete(item)
                    self.user_repository.del_mail(mail)

        add_user_mail_btn.config(command=add_mail)
        user_email_entry.bind('<Return>', add_mail)

        del_mail_btn = Button(tab, text="Supprimer l'adresse mail", command=del_mail)
        del_mail_btn.grid(column=1, row=2, sticky=(W, E, N))
        del_mail_btn.configure(bg='darkred', fg='white')

        for mail in self.mail_sender_accept:
            users_mails_lb.insert('end', mail)

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

    def add_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.bind('')
        entry.bind('<FocusIn>', lambda event: self.on_focusin_entry(event, text))
        entry.bind('<FocusOut>', lambda event: self.on_focusout_entry(event, text))

    def on_focusin_entry(self, event, text):
        entry = event.widget
        if entry.get() == text:
            entry.delete(0, "end")  # delete all the text in the entry
            entry.insert(0, '')
            entry.config(foreground='black')

    def on_focusout_entry(self, event, text):
        entry = event.widget
        if entry.get() == '':
            entry.insert(0, text)
            entry.config(foreground='grey')


def check_mail():
    gmail = GmailManager()

    while True:
        gmail.read()
        sleep(120)


if __name__ == '__main__':
    assistance = Assistance()

    mail_process = multiprocessing.Process(target=check_mail)
    mail_process.start()

    assistance.start()

    if mail_process.is_alive():
        mail_process.terminate()
