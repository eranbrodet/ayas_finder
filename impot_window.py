from os.path import basename
from Tkconstants import END, INSERT
from Tkinter import Toplevel, StringVar, IntVar
from ttk import Radiobutton, Label, Entry, Button, OptionMenu
from logic import get_from_excel, get_excel_sheets
from tkFileDialog import askopenfilename

#TODO Refactor this code

def excel_popup(field):
    sub_window = Toplevel(background="#333", padx=15, pady=15)
    sub_window.title("Aya's Finder: Import data from Excel file")
    sub_window.wm_iconbitmap(r"images\Dna-Helix.ico")
    row_col = StringVar()
    row_col.set("row")

    Radiobutton(sub_window, variable=row_col, value="row", text="Row").grid(row=0, column=0)
    Radiobutton(sub_window, variable=row_col, value="col", text="Column").grid(row=0, column=1)
    file_name_var = StringVar()
    sheet_name_var = StringVar()
    num_var = IntVar()

    Label(sub_window, justify="left", width="17", text="File name").grid(row=1, column=0)
    Label(sub_window, justify="left", width="17", text="Sheet name").grid(row=2, column=0)
    Label(sub_window, justify="left", width="17", text="Row/Column number").grid(row=3, column=0)
    Entry(sub_window, width="32", textvariable=file_name_var).grid(row=1, column=1)
    Entry(sub_window, width="7", textvariable=num_var).grid(row=3, column=1)
    sheets = OptionMenu(sub_window, sheet_name_var, '')
    sheets.config(width=32)
    sheets.grid(row=2, column=1)

    def get():
        file_name = file_name_var.get()
        sheet_name = sheet_name_var.get()
        num = num_var.get()
        try:
            if row_col.get() == "row":
                field.delete(1.0, END)
                field.insert(INSERT, get_from_excel(file_name, sheet_name, row_num=num))
            else:
                field.delete(1.0, END)
                field.insert(INSERT, get_from_excel(file_name, sheet_name, col_num=num))
            sub_window.destroy()
        except Exception:
            pass

    def browser():
        try:
            name = askopenfilename(parent=sub_window)
            file_name_var.set(name)
            sheets.set_menu('---', *get_excel_sheets(file_name_var.get()))
            sub_window.focus()
        except IOError:
            pass

    Button(sub_window, text="OK", command=get).grid(row=5, column=0)
    Button(sub_window, text="Cancel", command=lambda: sub_window.destroy()).grid(row=5, column=1)
    Button(sub_window, text="browse", command=browser).grid(row=1, column=3)