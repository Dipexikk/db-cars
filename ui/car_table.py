import tkinter as tk
from tkinter import ttk

class CarTable(ttk.Frame):
    COLUMNS = ("id", "brand", "model", "year", "price", "color", "mileage")
    COLUMNS_NAME = {
        "id": "ID",
        "brand": "Značka",
        "model": "Model",
        "year": "Rok",
        "price": "Cena (Kč)",
        "color": "Barva",
        "mileage": "Najeto (km)"
    }

    def __init__(self, parent):
        super().__init__(parent)
        self._create_widgets()

    def _create_widgets(self):
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.tree = ttk.Treeview(
            self,
            columns=self.COLUMNS,
            show="headings",
            selectmode="browse"
        )

        scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._configure_columns()

    def _configure_columns(self):
        widths = {
            "id": 50, "brand": 100, "model": 100,
            "year": 70, "price": 120,
            "color": 100, "mileage": 120
        }

        for col in self.COLUMNS:
            self.tree.heading(col, text=self.COLUMNS_NAME[col])
            self.tree.column(col, width=widths[col], anchor=tk.CENTER)

    def refresh(self, cars):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for car in cars:
            self.tree.insert("", tk.END, values=(
                car["id"],
                car["brand"],
                car["model"],
                car["year"],
                car["price"],
                car["color"],
                car["mileage"]
            ))
