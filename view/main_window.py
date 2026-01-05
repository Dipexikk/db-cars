import tkinter as tk
from tkinter import ttk, messagebox
from ui.car_table import CarTable
from view.add_car_form import AddCarForm
import json
import os

class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self._configure_window()
        self._create_widgets()
        self._load_data()

    def _configure_window(self):
        self.root.title("🚗 Správa Aut")
        self.root.geometry("900x500")

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            main_frame,
            text="Správa autobazaru",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(0, 15))

        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.table = CarTable(table_frame)
        self.table.pack(fill=tk.BOTH, expand=True)

        buttons = ttk.Frame(main_frame)
        buttons.pack(pady=10)

        ttk.Button(
            buttons,
            text="➕ Přidat auto",
            command=self._open_add_form
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            buttons,
            text="➖ Odebrat auto",
            command=self._delete_selected
        ).pack(side=tk.LEFT, padx=5)

        self.stats_label = ttk.Label(main_frame)
        self.stats_label.pack()

    def _load_data(self):
        os.makedirs("data", exist_ok=True)

        try:
            with open("data/cars.json", "r", encoding="utf-8") as f:
                self.cars = json.load(f)
        except FileNotFoundError:
            self.cars = []

        self.table.refresh(self.cars)

        total = sum(car["price"] for car in self.cars)
        self.stats_label.config(
            text=f"Počet aut: {len(self.cars)} | Celková hodnota: {total} Kč"
        )

    def _open_add_form(self):
        AddCarForm(self.root, self._load_data)

    def _delete_selected(self):
        selected = self.table.tree.selection()

        if not selected:
            messagebox.showwarning("Upozornění", "Vyber auto")
            return

        car_id = self.table.tree.item(selected)["values"][0]

        self.cars = [c for c in self.cars if c["id"] != car_id]

        with open("data/cars.json", "w", encoding="utf-8") as f:
            json.dump(self.cars, f, indent=4, ensure_ascii=False)

        self._load_data()

    def run(self):
        self.root.mainloop()
