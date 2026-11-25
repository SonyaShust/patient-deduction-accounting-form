
import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from storage import load_patients, save_patients
from stats import build_stats_figure
from dialog2 import patientdialog2         


class statswindow(tk.Toplevel):
    def __init__(self, master, patients):
        super().__init__(master)
        self.title("Сводная статистика")
        self.geometry("900x680")

        fig = build_stats_figure(patients)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()                     
        canvas.get_tk_widget().pack(fill="both", expand=True)

class patientapp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Учёт пациентов")
        self.geometry("1100x650")
        self.configure(bg="#F4F6F8")      
        self._apply_theme()                    
        self.patients = load_patients()
        self._build_ui()
        self._refresh_table()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _apply_theme(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
         pass

        base_font = ("DejaVu Sans", 11)
        style.configure(".", font=base_font, background="#F4F6F8")
        style.configure("TFrame", background="#F4F6F8")
        style.configure("TLabel", background="#F4F6F8", foreground="#1F2937")
  

        style.configure("Treeview.Heading",
                    font=("DejaVu Sans", 11, "bold"),
                    background="#26A316", foreground="white",
                    relief="flat", padding=6)
        style.map("Treeview.Heading",
              background=[("active", "#179306")])

        style.configure("Treeview",
                    font=("DejaVu Sans", 11),
                    rowheight=28,
                    background="white", fieldbackground="white")

        style.map("Treeview", background=[("selected", "#DBEAFE")],
              foreground=[("selected", "#0F172A")])


        style.configure("Accent.TButton",
                    font=("DejaVu Sans", 11, "bold"),
                    background="#40B93C", foreground="white",
                    padding=(14, 8), borderwidth=0)
        style.map("Accent.TButton",
              background=[("active","#40B93C", ), ("pressed", "#169312")])

        style.configure("Secondary.TButton",
                    font=("DejaVu Sans", 11),
                    padding=(14, 8))


    def _build_ui(self):
        toolbar = ttk.Frame(self, padding=(12, 10))
        toolbar.pack(fill="x")
 
        ttk.Button(toolbar, text="Добавить", style="Accent.TButton",
               command=self._add).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Редактировать", style="Secondary.TButton",
               command=self._edit).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Удалить", style="Secondary.TButton",
               command=self._delete).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Статистика", style="Accent.TButton",
               command=self._show_stats).pack(side="left", padx=4)

        columns = ("fio", "last", "first", "middle",
                   "age", "gender", "height", "weight", "bmi")
        headings = ("ФИО", "Фамилия", "Имя", "Отчество", "Возраст",
                    "Пол", "Рост, см", "Вес, кг", "ИМТ")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col, head in zip(columns, headings):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=90, anchor="center")
        self.tree.column("fio", width=220, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=8, pady=8)


        self.tree.bind("<Double-1>", lambda e: self._edit())

    def _refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        self.tree.tag_configure("odd", background="#F8FAFC")
        self.tree.tag_configure("even", background="white")
        for i, p in enumerate(self.patients):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", iid=str(i), tags=(tag,), values=(
                p.fio, p.last_name, p.first_name, p.middle_name or "—",
                p.age, p.gender, p.height, p.weight, p.bmi,
            ))
    def _add(self):
        dlg = patientdialog2(self, title="Новый пациент")
        self.wait_window(dlg)
        if dlg.result:
            self.patients.append(dlg.result)
            self._persist()

    def _edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Подсказка", "Выберите пациента")
            return
        idx = int(sel[0])            
        dlg = patientdialog2(self, title="Редактирование",
                            patient=self.patients[idx])
        self.wait_window(dlg)
        print("--- ВЕРНУЛОСЬ ИЗ ДИАЛОГА:", dlg.result)

        if dlg.result:
            self.patients[idx] = dlg.result
            self._persist()

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        if messagebox.askyesno("Удаление",
                               f"Удалить {self.patients[idx].fio}?"):
            self.patients.pop(idx)
            self._persist()

    def _persist(self):
        """Сохранить в data.json и перерисовать таблицу."""
        save_patients(self.patients)
        self._refresh_table()


    def _show_stats(self):
        if not self.patients:
            messagebox.showinfo("Статистика", "Нет данных для отображения")
            return
        statswindow(self, self.patients)


    def _on_close(self):
        save_patients(self.patients)
        self.destroy()


if __name__ == "__main__":
    app = patientapp()
    app.mainloop()