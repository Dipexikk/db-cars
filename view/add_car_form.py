import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class AddCarForm(tk.Toplevel):

    def __init__(self, parent, on_save_callback):
        super().__init__(parent)

        self.on_save_callback = on_save_callback
        self.entries = {}

        self.title("Přidat auto")
        self.geometry("300x420")
        self.resizable(False, False)

        self._create_widgets()

    def _create_widgets(self):
        fields = {
            "brand": "Značka",
            "model": "Model",
            "year": "Rok",
            "price": "Cena",
            "color": "Barva",
            "mileage": "Najeto"
        }

        for key, label in fields.items():
            ttk.Label(self, text=label).pack(pady=(10, 0))
            entry = ttk.Entry(self)
            entry.pack(fill=tk.X, padx=20)
            self.entries[key] = entry

        ttk.Button(self, text="Uložit", command=self._save).pack(pady=20)

    def _save(self):
        # 1) Získání a ořezání vstupů
        brand = self.entries["brand"].get().strip()
        model = self.entries["model"].get().strip()
        year = self.entries["year"].get().strip()
        price = self.entries["price"].get().strip()
        color = self.entries["color"].get().strip()
        mileage = self.entries["mileage"].get().strip()

        # 2) Kontrola prázdných polí
        if not all([brand, model, year, price, color, mileage]):
            messagebox.showerror("Chyba", "Všechna pole musí být vyplněna.")
            return

        # 3) Kontrola, že rok/cena/najeto jsou čísla
        if not year.isdigit():
            messagebox.showerror("Chyba", "Rok musí být číslo.")
            return

        if not price.isdigit():
            messagebox.showerror("Chyba", "Cena musí být číslo.")
            return

        if not mileage.isdigit():
            messagebox.showerror("Chyba", "Najeto musí být číslo.")
            return

        year = int(year)
        price = int(price)
        mileage = int(mileage)

        # 4) Logické validace
        current_year = datetime.now().year

        if year < 1900 or year > current_year:
            messagebox.showerror("Chyba", f"Rok musí být mezi 1900 a {current_year}.")
            return

        if price < 0:
            messagebox.showerror("Chyba", "Cena nemůže být záporná.")
            return

        if mileage < 0:
            messagebox.showerror("Chyba", "Najeto nemůže být záporné.")
            return

        # 5) Načtení existujících dat
        try:
            with open("data/cars.json", "r", encoding="utf-8") as f:
                cars = json.load(f)
        except FileNotFoundError:
            cars = []

        # 6) Vygenerování nového ID
        new_id = max((car["id"] for car in cars), default=-1) + 1

        car = {
            "id": new_id,
            "brand": brand,
            "model": model,
            "year": year,
            "price": price,
            "color": color,
            "mileage": mileage
        }

        # 7) Uložení do JSON
        with open("data/cars.json", "w", encoding="utf-8") as f:
            json.dump(cars + [car], f, indent=4, ensure_ascii=False)

        # 8) Refresh a zavření okna
        self.on_save_callback()
        self.destroy()
