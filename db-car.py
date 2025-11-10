
import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = os.path.join(os.path.dirname(__file__), "cars.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT,
            model TEXT,
            year INTEGER,
            gearbox TEXT,
            price REAL,
            capacity FLOAT,
            color TEXT
        )
        """
    )
    conn.commit()
    conn.close()


class CarDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Databáze aut")
        self.create_widgets()
        init_db()
        self.load_cars()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        # STYLY PRO TLAČÍTKA (zelené / červené)
        style = ttk.Style(self.root)
        # Nastavení základních barev (u některých témat může být potřeba použít tk.Button)
        style.configure("Green.TButton", background="#28a745")
        style.map(
            "Green.TButton",
            background=[("active", "#218838"), ("disabled", "#9fd2a7")],
            foreground=[("active", "#383838")],
        )
        style.configure("Red.TButton", background="#dc3545")
        style.map(
            "Red.TButton",
            background=[("active", "#c82333"), ("disabled", "#e79a9a")],
            foreground=[("active", "#383838")],
        )

        # Treeview pro zobrazení aut
        cols = ("id", "brand", "model", "year", "gearbox", "price", "capacity", "color")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        headings = {
            "id": "ID",
            "brand": "Značka",
            "model": "Model",
            "year": "Rok",
            "gearbox": "Převodovka",
            "price": "Cena",
            "capacity": "Obsah",
            "color": "Barva",
        }
        for c in cols:
            self.tree.heading(c, text=headings[c])
            if c == "id":
                self.tree.column(c, width=40, anchor="center")
            elif c in ("brand", "model", "gearbox", "color"):
                self.tree.column(c, width=120, anchor="w")
            else:
                self.tree.column(c, width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=(0, 10))

        # Tlačítka
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", expand=False)
        add_btn = ttk.Button(btn_frame, text="Přidat", command=self.open_add_window, style="Green.TButton")
        add_btn.pack(side="left", padx=(0, 5))
        del_btn = ttk.Button(btn_frame, text="Vymazat", command=self.delete_selected, style="Red.TButton")
        del_btn.pack(side="left")

    def load_cars(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, brand, model, year, gearbox, price, capacity, color FROM cars ORDER BY id")
        for r in cur.fetchall():
            self.tree.insert("", "end", values=r)
        conn.close()

    def open_add_window(self):
        win = tk.Toplevel(self.root)
        win.title("Přidat auto")
        win.grab_set()

        labels = ["Značka", "Model", "Rok výroby", "Typ převodovky", "Cena", "Obsah", "Barva"]
        self.entries = {}

        form = ttk.Frame(win, padding=10)
        form.pack(fill="both", expand=True)

        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w", pady=4)
            if label == "Typ převodovky":
                cb = ttk.Combobox(form, values=["Manuál", "Automat"], state="readonly")
                cb.grid(row=i, column=1, sticky="ew", padx=6)
                cb.current(0)
                self.entries["gearbox"] = cb
            else:
                ent = ttk.Entry(form)
                ent.grid(row=i, column=1, sticky="ew", padx=6)
                key = {
                    "Značka": "brand",
                    "Model": "model",
                    "Rok výroby": "year",
                    "Cena": "price",
                    "Obsah": "capacity",
                    "Barva": "color",
                }[label]
                self.entries[key] = ent

        form.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(win, padding=(10, 0, 10, 10))
        btn_frame.pack(fill="x", expand=False)
        submit = ttk.Button(btn_frame, text="Uložit", command=lambda: self.add_car(win), style="Green.TButton")
        submit.pack(side="right", padx=(5, 0))
        cancel = ttk.Button(btn_frame, text="Zrušit", command=win.destroy, style="Red.TButton")
        cancel.pack(side="right")

    def add_car(self, win):
        try:
            brand = self.entries["brand"].get().strip()
            model = self.entries["model"].get().strip()
            year = int(self.entries["year"].get().strip())
            gearbox = self.entries["gearbox"].get().strip()
            price = float(self.entries["price"].get().strip())
            capacity = float(self.entries["capacity"].get().strip())
            color = self.entries["color"].get().strip()
        except Exception:
            messagebox.showerror("Chyba", "Zkontrolujte vyplněná pole a formát (rok - celé číslo, cena/obsah - číslo).")
            return

        if not brand or not model:
            messagebox.showerror("Chyba", "Značka a model jsou povinné.")
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cars (brand, model, year, gearbox, price, capacity, color) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (brand, model, year, gearbox, price, capacity, color),
        )
        conn.commit()
        conn.close()
        win.destroy()
        self.load_cars()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Vyberte řádek k odstranění.")
            return
        item = self.tree.item(sel[0])
        car_id = item["values"][0]
        if messagebox.askyesno("Potvrdit", f"Opravdu smazat vozidlo ID {car_id}?"):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM cars WHERE id = ?", (car_id,))
            conn.commit()
            conn.close()
            self.load_cars()


if __name__ == "__main__":
    root = tk.Tk()
    app = CarDBApp(root)
    root.mainloop()
#