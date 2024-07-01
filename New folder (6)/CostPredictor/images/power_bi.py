import customtkinter
from tkinter import filedialog
import pandas as pd

def browse_file(entry_var, sheet_var, sheet_menu):
    filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    entry_var.set(filename)
    update_sheet_options(filename, sheet_var, sheet_menu)

def update_sheet_options(filename, sheet_var, sheet_menu):
    excel_file = pd.ExcelFile(filename)
    sheet_var.set(excel_file.sheet_names[0])
    sheet_menu['menu'].delete(0, 'end')
    for sheet in excel_file.sheet_names:
        sheet_menu['menu'].add_command(label=sheet, command=tk._setit(sheet_var, sheet))

def upload_to_power_bi(file, sheet):
    df = pd.read_excel(file, sheet_name=sheet)
    # Implement the Power BI upload logic
