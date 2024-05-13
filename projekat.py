from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import ttk, messagebox, simpledialog
import csv

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_csv_row(self):
        return [self.name, self.price, self.quantity]

class SubProduct(Product):
    def __init__(self, name, price, sub_type, quantity):
        super().__init__(name, price, quantity)
        self.sub_type = sub_type

    def to_csv_row(self):
        return [self.name, self.price, self.sub_type, self.quantity]

class ShoppingCartItem:
    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity=1):
        for item in self.items:
            if item.product == product:
                item.quantity += quantity
                return
        self.items.append(ShoppingCartItem(product, quantity))

    def remove_item(self, index):
        del self.items[index]

    def calculate_total(self):
        return sum(item.product.price * item.quantity for item in self.items)

class StoreApp:
    def __init__(self, master):
        self.master = master
        master.title("Prodavnica sa probom teme ? ")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Postavljanje boja
        self.bg_color = "white"  # Promijenjena boja pozadine na crnu
        self.text_color = "#333333"
        self.button_color = "#4CAF50"
        self.button_text_color = "white"
        self.heading_color = "#2c3e50"
        self.heading_text_color = "white"

        master.config(bg=self.bg_color)

        # Postavljanje fonta
        self.font = ("Helvetica", 12)

        self.products = [
            Product("Laptop", 800, 10),
            Product("Miš", 30, 20),
            Product("Tastatura", 50, 15),
            Product("Monitor", 200, 5),
            SubProduct("All in One PC", 1200, "Različite konfiguracije", 8),
            SubProduct("Zvučnici", 80, "2.1, 5.1, Bluetooth", 12),
            SubProduct("Head Set", 50, "Bežični, s mikrofonom", 10),
            SubProduct("Routeri", 100, "Single Band, Dual Band", 15),
            SubProduct("Grafička kartica", 300, "AMD, NVIDIA", 7),
            SubProduct("Zvučna kartica", 40, "USB, PCIe", 9),
            SubProduct("Web Kamera", 60, "720p, 1080p", 11),
            SubProduct("RAM Memorija", 70, "DDR3, DDR4", 14),
            SubProduct("Hard Diskovi (HD)", 80, "500GB, 1TB, 2TB", 20),
            SubProduct("Solid State Drive (SSD)", 100, "256GB, 512GB, 1TB", 18)
        ]

        self.shopping_cart = ShoppingCart()
        self.logged_in_user = None

        self.product_frame = tk.Frame(master, bg=self.bg_color)
        self.product_frame.pack(pady=20, padx=20)

        self.product_listbox = tk.Listbox(self.product_frame, width=50, height=10, font=self.font)
        self.product_listbox.pack(side=tk.LEFT, padx=10)

        self.product_scrollbar = tk.Scrollbar(self.product_frame, orient=tk.VERTICAL)
        self.product_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.product_listbox.config(yscrollcommand=self.product_scrollbar.set)
        self.product_scrollbar.config(command=self.product_listbox.yview)

        self.product_listbox.bind("<Button-3>", self.show_product_details)  # Desni klik na proizvod

        self.search_label = tk.Label(master, text="Pretraga:", bg=self.bg_color, fg=self.text_color, font=self.font)
        self.search_label.pack()

        self.search_entry = tk.Entry(master, font=self.font, width=50)
        self.search_entry.pack()

        self.search_button = tk.Button(master, text="Pretraži", command=self.search_products, bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.search_button.pack()

        self.add_to_cart_button = tk.Button(master, text="Dodaj u korpu", command=self.add_to_cart, bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.add_to_cart_button.pack()

        self.cart_label = tk.Label(master, text="Korpa:", bg=self.bg_color, fg=self.text_color, font=self.font)
        self.cart_label.pack()

        self.cart_listbox = tk.Listbox(master, width=50, height=5, font=self.font)
        self.cart_listbox.pack()

        self.remove_from_cart_button = tk.Button(master, text="Ukloni iz korpe", command=self.remove_item, bg="red", fg=self.button_text_color, font=self.font)
        self.remove_from_cart_button.pack()

        self.checkout_button = tk.Button(master, text="Checkout", command=self.checkout, bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.checkout_button.pack()

        self.total_label = tk.Label(master, text="", bg=self.bg_color, fg=self.text_color, font=self.font)
        self.total_label.pack()

        self.load_all_products()

        # Prikazuje ime korisnika u donjem desnom uglu
        self.logged_in_user_label = tk.Label(master, text="", anchor="e", bg=self.bg_color, fg=self.text_color, font=self.font)
        self.logged_in_user_label.pack(side=tk.RIGHT)
        self.product_listbox.bind("<Double-Button-1>", self.show_product_details)
        # Dodajemo gumb za odjavu korisnika
        self.logout_button = tk.Button(master, text="Odjavi se", command=self.logout, bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.logout_button.pack(side=tk.RIGHT)

        self.login_button = tk.Button(master, text="Prijavi se", command=self.login, bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.login_button.pack(side=tk.RIGHT)

        self.register_button = tk.Button(master, text="Registracija", command=self.register, bg=self.button_color, fg=self.button_text_color, font=self.font)
        self.register_button.pack(side=tk.RIGHT)

        # Učitaj korisnike iz CSV datoteke
        self.users = self.load_users_from_csv("users.csv")

        # Glavni meni
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        # Meni "File"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Izlaz", command=master.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Meni "Account"
        self.account_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.account_menu.add_command(label="Registracija", command=self.register)
        self.account_menu.add_command(label="Prijavi se", command=self.login)
        self.account_menu.add_command(label="Odjavi se", command=self.logout)
        self.menu_bar.add_cascade(label="Account", menu=self.account_menu)

        # Meni "Help"
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Pomoć", command=self.show_help)
        self.help_menu.add_command(label="Kontakt", command=self.show_contact)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

    def load_all_products(self):
        self.product_listbox.delete(0, tk.END)
        for product in self.products:
            if isinstance(product, SubProduct):
                self.product_listbox.insert(tk.END, f"{product.name} - ${product.price} - Lager: {product.quantity} komada ({product.sub_type})")
            else:
                self.product_listbox.insert(tk.END, f"{product.name} - ${product.price} - Lager: {product.quantity} komada")

    def search_products(self):
        if not self.logged_in_user:
            messagebox.showwarning("Upozorenje", "Morate biti prijavljeni da biste koristili pretragu.")
            return

        query = self.search_entry.get().lower()
        if query == "":
            self.load_all_products()
            return
        self.product_listbox.delete(0, tk.END)
        for product in self.products:
            if query in product.name.lower() or (isinstance(product, SubProduct) and query in product.sub_type.lower()):
                if isinstance(product, SubProduct):
                    self.product_listbox.insert(tk.END, f"{product.name} - ${product.price} - Lager: {product.quantity} komada ({product.sub_type})")
                else:
                    self.product_listbox.insert(tk.END, f"{product.name} - ${product.price} - Lager: {product.quantity} komada")

    def add_to_cart(self):
        if not self.logged_in_user:
            messagebox.showwarning("Upozorenje", "Morate biti prijavljeni da biste dodali proizvod u korpu.")
            return

        selection = self.product_listbox.curselection()
        if selection:
            index = selection[0]
            product = self.products[index]
            if product.quantity > 0:
                if isinstance(product, SubProduct):
                    self.choose_subproduct(product)
                else:
                    quantity = simpledialog.askinteger("Količina", f"Unesite količinu za {product.name}:")
                    if quantity is not None and quantity > 0 and product.quantity >= quantity:
                        self.shopping_cart.add_item(product, quantity)
                        product.quantity -= quantity
                        self.load_all_products()
                        self.update_cart_display()
                    else:
                        messagebox.showwarning("Upozorenje", f"Nema dovoljno proizvoda na lageru.")

    def choose_subproduct(self, product):
        subproduct_window = tk.Toplevel(self.master)
        subproduct_window.title(f"Izaberite {product.name}")

        tk.Label(subproduct_window, text=f"Izaberite {product.name}:", bg=self.bg_color, fg=self.text_color, font=self.font).pack()

        subproduct_listbox = tk.Listbox(subproduct_window, width=100, height=10, font=self.font)
        subproduct_listbox.pack()

        for sub_product in self.products:
            if isinstance(sub_product, SubProduct) and sub_product.name == product.name:
                subproduct_listbox.insert(tk.END, f"{sub_product.name} - ${sub_product.price} ({sub_product.sub_type})")

        def add_subproduct_to_cart():
            selection = subproduct_listbox.curselection()
            if selection:
                index = selection[0]
                sub_product = [p for p in self.products if isinstance(p, SubProduct) and p.name == product.name][index]
                if sub_product.quantity > 0:
                    self.shopping_cart.add_item(sub_product)
                    sub_product.quantity -= 1
                    self.load_all_products()
                    self.update_cart_display()
                    subproduct_window.destroy()
                else:
                    messagebox.showwarning("Upozorenje", f"Nema dovoljno proizvoda na lageru.")

        add_button = tk.Button(subproduct_window, text="Dodaj u korpu", command=add_subproduct_to_cart, bg=self.button_color, fg=self.button_text_color, font=self.font)
        add_button.pack()

    def update_cart_display(self):
        self.cart_listbox.delete(0, tk.END)
        for item in self.shopping_cart.items:
            self.cart_listbox.insert(tk.END, f"{item.product.name} - ${item.product.price} x {item.quantity}")
        total = self.shopping_cart.calculate_total()
        self.total_label.config(text=f"Total: ${total}")

    def remove_item(self):
        if not self.logged_in_user:
            messagebox.showwarning("Upozorenje", "Morate biti prijavljeni da biste uklonili proizvod iz korpe.")
            return

        selection = self.cart_listbox.curselection()
        if selection:
            index = selection[0]
            item = self.shopping_cart.items[index]
            item.product.quantity += item.quantity
            self.shopping_cart.remove_item(index)
            self.load_all_products()
            self.update_cart_display()

    def checkout(self):
        if not self.logged_in_user:
            messagebox.showwarning("Upozorenje", "Morate biti prijavljeni da biste izvršili checkout.")
            return

        total = self.shopping_cart.calculate_total()
        payment_method = simpledialog.askstring("Plaćanje", "Odaberite način plaćanja (npr. kartica, gotovina):")
        if payment_method:
            if payment_method.lower() == "kartica":
                self.input_credit_card_info()
            else:
                tk.messagebox.showinfo("Checkout", f"Total to pay: ${total}\nNačin plaćanja: {payment_method}")
            self.save_products_to_csv("products.csv")
            self.shopping_cart = ShoppingCart()
            self.update_cart_display()
            self.load_all_products()

    def input_credit_card_info(self):
        credit_card_window = tk.Toplevel(self.master)
        credit_card_window.title("Unesite podatke o kreditnoj kartici")

        tk.Label(credit_card_window, text="Broj kartice:", bg=self.bg_color, fg=self.text_color, font=self.font).pack()
        card_number_entry = tk.Entry(credit_card_window, font=self.font, width=50)
        card_number_entry.pack()

        tk.Label(credit_card_window, text="Ime i prezime vlasnika:", bg=self.bg_color, fg=self.text_color, font=self.font).pack()
        owner_name_entry = tk.Entry(credit_card_window, font=self.font, width=50)
        owner_name_entry.pack()

        def process_payment():
            card_number = card_number_entry.get()
            owner_name = owner_name_entry.get()
            if card_number and owner_name:
                tk.messagebox.showinfo("Uspješno", "Plaćanje uspješno obavljeno.")
                credit_card_window.destroy()
            else:
                tk.messagebox.showwarning("Upozorenje", "Molimo unesite sve potrebne podatke.")

        submit_button = tk.Button(credit_card_window, text="Potvrdi", command=process_payment, bg=self.button_color, fg=self.button_text_color, font=self.font)
        submit_button.pack()

    def load_users_from_csv(self, filename):
        users = {}
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    username = row[0]
                    password = row[1]
                    users[username] = password
        except FileNotFoundError:
            tk.messagebox.showerror("Greška", "Datoteka korisnika nije pronađena.")
        return users

    def register(self):
        username = simpledialog.askstring("Registracija", "Unesite korisničko ime:")
        if username:
            if username in self.users:
                tk.messagebox.showwarning("Upozorenje", "Korisničko ime već postoji.")
                return
            password = simpledialog.askstring("Registracija", "Unesite lozinku:")
            if password:
                self.users[username] = password
                self.save_users_to_csv("users.csv")

    def login(self):
        username = simpledialog.askstring("Prijava", "Unesite korisničko ime:")
        if username:
            password = simpledialog.askstring("Prijava", "Unesite lozinku:")
            if username in self.users and self.users[username] == password:
                self.logged_in_user = username
                self.logged_in_user_label.config(text=f"Prijavljeni ste kao: {self.logged_in_user}")
            else:
                tk.messagebox.showwarning("Neuspjela prijava", "Pogrešno korisničko ime ili lozinka.")

    def logout(self):
        self.logged_in_user = None
        self.logged_in_user_label.config(text="")
        tk.messagebox.showinfo("Odjava", "Uspješno ste se odjavili.")

    def save_users_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for username, password in self.users.items():
                writer.writerow([username, password])

    def save_products_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for product in self.products:
                writer.writerow(product.to_csv_row())

    def show_product_details(self, event):
        index = self.product_listbox.nearest(event.y)
        product = self.products[index]
        messagebox.showinfo("Detalji proizvoda", f"{product.name}\nCijena: ${product.price}\nLager: {product.quantity} komada")

    def show_help(self):
        messagebox.showinfo("Pomoć", "Ovo je aplikacija za prodaju proizvoda. Koristite meni 'Account' za prijavu i registraciju.")

    def show_contact(self):
        messagebox.showinfo("Kontakt", "Za podršku kontaktirajte: support@example.com")
def calculate_average_price(self):
    total_price = sum(product.price for product in self.products)
    average_price = total_price / len(self.products)
    messagebox.showinfo("Prosječna cijena proizvoda", f"Prosječna cijena proizvoda u prodavnici je: ${average_price:.2f}")

def show_available_quantities(self):
    available_quantities_info = "\n".join([f"{product.name}: {product.quantity} komada" for product in self.products])
    messagebox.showinfo("Raspoložive količine proizvoda", available_quantities_info)

def add_new_product(self):
    name = simpledialog.askstring("Dodavanje novog proizvoda", "Unesite ime proizvoda:")
    if name:
        price = simpledialog.askfloat("Dodavanje novog proizvoda", "Unesite cijenu proizvoda:")
        if price:
            quantity = simpledialog.askinteger("Dodavanje novog proizvoda", "Unesite količinu proizvoda:")
            if quantity:
                product = Product(name, price, quantity)
                self.products.append(product)
                self.load_all_products()
                messagebox.showinfo("Dodavanje novog proizvoda", "Novi proizvod uspješno dodan.")
def show_product_details_popup(self, event):
    index = self.product_listbox.nearest(event.y)
    if index >= 0:
        product = self.products[index]
        detail_message = f"{product.name}\nCijena: ${product.price}\nLager: {product.quantity} komada"
        messagebox.showinfo("Detalji proizvoda", detail_message)

root = tk.Tk()
app = StoreApp(root)
root.mainloop()