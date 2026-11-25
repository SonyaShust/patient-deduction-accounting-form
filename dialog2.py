# dialog.py
import tkinter as tk
from tkinter import ttk, messagebox

from models import Patient


class patientdialog2(tk.Toplevel):
    BG        = "#FFFFFF"     # фон окна
    LABEL_FG  = "#374151"     # цвет подписи
    ENTRY_BG  = "#F9FAFB"     # фон поля ввода
    ACCENT    = "#169312"     # акцент
    ERROR_FG  = "#B21A1A"     # ошибка

    def __init__(self, master, title="Пациент", patient=None):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.configure(bg=self.BG)
        self.result = None
        self._patient = patient

        self._apply_style()
        self._build_form(patient)

        self.transient(master)
        self.update_idletasks() 
        self.grab_set()
        self._center_on_parent(master)
        self.grab_set()

    def _apply_style(self):
        style = ttk.Style(self)
        style.configure("Field.TLabel",
                        font=("DejaVu Sans", 11, "bold"),
                        foreground=self.LABEL_FG,
                        background=self.BG)
        style.configure("Hint.TLabel",
                        font=("DejaVu Sans", 9),
                        foreground="#9CA3AF",
                        background=self.BG)
        style.configure("Field.TEntry",
                        font=("DejaVu Sans", 11),
                        padding=6,
                        fieldbackground=self.ENTRY_BG)
        style.configure("Primary.TButton",
                        font=("DejaVu Sans", 11, "bold"),
                        background=self.ACCENT, foreground="white",
                        padding=(16, 8), borderwidth=0)
        style.map("Primary.TButton",
                  background=[("active", "#169312")])
        style.configure("Ghost.TButton",
                        font=("DejaVu Sans", 11),
                        padding=(16, 8))

    def _build_form(self, patient):
        digits_only = (self.register(self._digits_only), "%P")
        names_only  = (self.register(self._names_only),  "%P")


        fields = [
            ("Фамилия",                    "last_name",   names_only, None),
            ("Имя",                        "first_name",  names_only, None),
            ("Отчество",                   "middle_name", names_only, "необязательно"),
            ("Возраст (лет)",              "age",         digits_only, None),
            ("Рост (см)",                  "height",      digits_only, None),
            ("Вес (кг)",                   "weight",      digits_only, None),
        ]

        self.vars = {}
        row = 0
        for label, key, validate, hint in fields:
            label_text = label + (f"  ({hint})" if hint else "")
            ttk.Label(self, text=label_text, style="Field.TLabel").grid(
                row=row, column=0, sticky="w", padx=18, pady=(12, 2))
            row += 1

            var = tk.StringVar()
            entry = ttk.Entry(self, textvariable=var, width=34,
                              style="Field.TEntry")
            entry.configure(validate="key", validatecommand=validate)
            entry.grid(row=row, column=0, sticky="we", padx=18, pady=(0, 2))
            row += 1
            self.vars[key] = var

        ttk.Label(self, text="Пол", style="Field.TLabel").grid(
            row=row, column=0, sticky="w", padx=18, pady=(12, 2))
        row += 1

        self.vars["gender"] = tk.StringVar(value="М")
        gender_frame = tk.Frame(self, bg=self.BG)
        gender_frame.grid(row=row, column=0, sticky="w", padx=18, pady=(0, 6))
        row += 1
        for value, text in (("М", "Мужской"), ("Ж", "Женский"), ("Не определен", "Не определен")):
            tk.Radiobutton(
                gender_frame, text=text, value=value,
                variable=self.vars["gender"],
                font=("DejaVu Sans", 11),
                bg=self.BG, fg=self.LABEL_FG,
                activebackground=self.BG,
                selectcolor="white",
                cursor="hand2",
            ).pack(side="left", padx=(0, 16))

        btns = ttk.Frame(self)
        btns.grid(row=row, column=0, pady=(16, 18), padx=18, sticky="e")
        ttk.Button(btns, text="Сохранить", style="Primary.TButton",
                   command=self._on_save).pack(side="right", padx=(8, 0))
        ttk.Button(btns, text="Отмена", style="Ghost.TButton",
                   command=self.destroy).pack(side="right")

        if patient:
            for key in ("last_name", "first_name", "middle_name",
                        "age", "height", "weight"):
                val = getattr(patient, key)
                self.vars[key].set("" if val is None else str(val))
            self.vars["gender"].set(patient.gender)


        self.after(50, lambda: self.focus_get())

    def _center_on_parent(self, master):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        px, py = master.winfo_rootx(), master.winfo_rooty()
        pw, ph = master.winfo_width(), master.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    @staticmethod
    def _digits_only(proposed: str) -> bool:
        return proposed == "" or proposed.isdigit()

    @staticmethod
    def _names_only(proposed: str) -> bool:
        if proposed == "":
            return True
        return all(ch.isalpha() or ch == "-" for ch in proposed)


    def _on_save(self):
        try:
            data = {key: var.get().strip() for key, var in self.vars.items()}
            if not data["age"] or not data["height"] or not data["weight"]:
                raise ValueError("Заполните возраст, рост и вес")
            patient = Patient(
                last_name=data["last_name"],
                first_name=data["first_name"],
                middle_name=data["middle_name"],
                age=int(data["age"]),
                gender=data["gender"],
                height=float(data["height"]),
                weight=float(data["weight"]),
            )
            self.result = patient
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e), parent=self)
        