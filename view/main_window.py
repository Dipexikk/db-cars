import tkinter as tk
from tkinter import ttk, messagebox
from ui.car_table import CarTable
from view.add_car_form import AddCarForm
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class MainWindow:

    def __init__(self):
        self.root = tk.Tk()
        self._configure_window()
        self._load_data()
        self._create_widgets()

    def _configure_window(self):
        self.root.title("🚗 Správa Aut")
        self.root.state("zoomed")



    def _create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            self.main_frame,
            text="Správa autobazaru",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(0, 15))

        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self._create_table_view()

    # tabulka

    def _create_table_view(self):
        self._clear_content()

        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.table = CarTable(table_frame)
        self.table.pack(fill=tk.BOTH, expand=True)
        self.table.tree.bind("<Double-1>", self._open_car_detail)

        buttons = ttk.Frame(self.content_frame)
        buttons.pack(pady=10)

        ttk.Button(buttons, text="➕ Přidat auto", command=self._open_add_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons, text="➖ Odebrat auto", command=self._delete_selected).pack(side=tk.LEFT, padx=5)

        self.table.refresh(self.cars)

    # detaily aut

    def _open_car_detail(self, event):
        selected = self.table.tree.selection()
        if not selected:
            return

        self.selected_car = self.table.tree.item(selected)["values"]
        self._clear_content()

        ttk.Button(self.content_frame, text="⬅ ZPĚT", command=self._create_table_view).pack(anchor="w")

        body = ttk.Frame(self.content_frame)
        body.pack(fill=tk.BOTH, expand=True, pady=15)

        self.left = ttk.Frame(body)
        self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        self.right = ttk.Frame(body)
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self._render_image()
        self._render_actions()

    # obrazek

    def _render_image(self):
        for w in self.left.winfo_children():
            w.destroy()

        car_id = self.selected_car[0]
        img_file = None

        for ext in ("png", "jpg", "jpeg"):
            path = f"images/{car_id}.{ext}"
            if os.path.exists(path):
                img_file = path
                break

        if img_file:
            img = Image.open(img_file).resize((700, 520))
            self.car_img = ImageTk.PhotoImage(img)
            tk.Label(self.left, image=self.car_img).pack()
        else:
            ttk.Label(self.left, text="Fotka není k dispozici").pack(expand=True)

    # akce

    def _render_actions(self):
        for w in self.right.winfo_children():
            w.destroy()

        # Styl pro velká tlačítka
        style = ttk.Style()
        style.configure("Big.TButton", font=("Segoe UI", 40))

        ttk.Label(
            self.right,
            text=f"{self.selected_car[1]} {self.selected_car[2]}",
            font=("Segoe UI", 50, "bold")
        ).pack(pady=10)

        ttk.Button(
            self.right,
            text="🛒 KOUPIT",
            style="Big.TButton",
            command=self._start_loading_invoice
        ).pack(pady=20, fill=tk.BOTH, expand=True)

        ttk.Button(
            self.right,
            text="📅 VYPUJČIT",
            style="Big.TButton",
            command=self._show_rent_form
        ).pack(pady=20, fill=tk.BOTH, expand=True)


    # loading

    def _start_loading_invoice(self):
        for w in self.right.winfo_children():
            w.destroy()

        ttk.Label(self.right, text="Zpracovávám nákup...", font=("Segoe UI", 12)).pack(pady=15)
        bar = ttk.Progressbar(self.right, mode="indeterminate")
        bar.pack(fill=tk.X, padx=40)
        bar.start()

        self.root.after(5000, self._show_invoice)

    # faktura

    def _show_invoice(self):
        for w in self.right.winfo_children():
            w.destroy()

        car = self.selected_car
        self.invoice_text = f"""
AUTO SEDA s.r.o.
ICO: 12345678 | DIC: CZ12345678
Praha 1, Ceska republika

FAKTURA – DANOVY DOKLAD
CIslo faktury: 2026-{car[0]:04d}
Datum vystaveni: {datetime.now().strftime('%d.%m.%Y')}

--------------------------------------------
Vozidlo:
Znacka: {car[1]}
Model: {car[2]}
Rok: {car[3]}
Barva: {car[5]}
Najeto: {car[6]} km

Cena bez DPH: {car[4]} Kc
DPH 21 %: {int(car[4]*0.21)} Kc
CELKEM K UHRADE: {int(car[4]*1.21)} Kc
--------------------------------------------

Dekujeme za vas nákup.
"""

        text = tk.Text(self.right, font=("Courier New", 10))
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, self.invoice_text)
        text.config(state=tk.DISABLED)

        ttk.Button(
            self.right,
            text="Stáhnout fakturu (PDF)",
            command=self._generate_pdf
        ).pack(pady=10)

    def _generate_pdf(self):
        os.makedirs("invoices", exist_ok=True)
        car_id = self.selected_car[0]
        file_path = f"invoices/faktura_{car_id}.pdf"

        c = canvas.Canvas(file_path, pagesize=A4)
        text = c.beginText(40, 800)

        for line in self.invoice_text.split("\n"):
            text.textLine(line)

        c.drawText(text)
        c.showPage()
        c.save()

        messagebox.showinfo("Hotovo", f"Faktura uložena:\n{file_path}")

    # pujčka

    def _show_rent_form(self):
        for w in self.right.winfo_children():
            w.destroy()

        ttk.Label(self.right, text="Vypůjčení vozidla", font=("Segoe UI", 14, "bold")).pack(pady=10)

        ttk.Label(self.right, text="Od (DD.MM.RRRR HH:MM)").pack()
        self.start_entry = ttk.Entry(self.right)
        self.start_entry.pack(pady=5)

        ttk.Label(self.right, text="Do (DD.MM.RRRR HH:MM)").pack()
        self.end_entry = ttk.Entry(self.right)
        self.end_entry.pack(pady=5)

        ttk.Button(self.right, text="Potvrdit půjčení", command=self._confirm_rent).pack(pady=15)

    def _confirm_rent(self):
        messagebox.showinfo(
            "Vypůjčení úspěšné",
            "Vypůjčení bylo úspěšné.\nVozidlo si vyzvedněte na pobočce."
        )
        self._render_actions()

    # data

    def _load_data(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/cars.json", "r", encoding="utf-8") as f:
                self.cars = json.load(f)
        except FileNotFoundError:
            self.cars = []

    def _open_add_form(self):
        AddCarForm(self.root, self._reload)

    def _reload(self):
        self._load_data()
        self._create_table_view()

    def _delete_selected(self):
        selected = self.table.tree.selection()
        if not selected:
            return

        car_id = self.table.tree.item(selected)["values"][0]
        self.cars = [c for c in self.cars if c["id"] != car_id]

        with open("data/cars.json", "w", encoding="utf-8") as f:
            json.dump(self.cars, f, indent=4, ensure_ascii=False)

        self._reload()

    def _clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def run(self):
        self.root.mainloop()
