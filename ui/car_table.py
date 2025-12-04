import tkinter as tk
from tkinter import ttk

class CarTable(ttk.Frame):
    COLUMNS = ("id", "brand", "model", "year", "price", "color", "mileage")
    COLUMNS_NAME = {
        "id": "ID",
        "brand": "Značka",
        "model": "Model",
        "year": "Rok",
        "price": "Cena",
        "color": "Barva",
        "mileage": "Najeto (km)",
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
            selectmode="browse",
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            show="headings",
            selectmode="browse"
        )
                
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _configure_columns(self):
        column_widths = {
            "id": 50, "brand": 100, "model": 100,
            "year": 70, "price": 100, "color": 100,
            "mileage": 100}
        
        for col in self.COLUMNS:
            self.tree.heading(col, text=self.COLUMNS_NAME[col])
            self.tree.column(col, width=column_widths[col], anchor=tk.CENTER)

