import tkinter as tk
from tkinter import ttk, messagebox
import json

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
        try:
            with open("data/cars.json", "r", encoding="utf-8") as f:
                cars = json.load(f)

            new_id = max((car["id"] for car in cars), default=-1) + 1

            car = {
                "id": new_id,
                "brand": self.entries["brand"].get(),
                "model": self.entries["model"].get(),
                "year": int(self.entries["year"].get()),
                "price": int(self.entries["price"].get()),
                "color": self.entries["color"].get(),
                "mileage": int(self.entries["mileage"].get())
            }

            cars.append(car)

            with open("data/cars.json", "w", encoding="utf-8") as f:
                json.dump(cars, f, indent=4, ensure_ascii=False)

            self.on_save_callback()
            self.destroy()

        except ValueError:
            messagebox.showerror(
                "Chyba",
                "Rok, cena a nájezd musí být čísla"
            )
