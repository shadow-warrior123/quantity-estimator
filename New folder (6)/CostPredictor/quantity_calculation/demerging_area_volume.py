import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os


def load_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            process_data(df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the Excel file: {e}")


def process_data(df):
    # Ensure column names are correctly identified
    area_columns = [col for col in df.columns if col.lower().endswith('area')]
    volume_columns = [col for col in df.columns if col.lower().endswith('volume')]

    # Include Category column at first position
    area_data = df[['Category', 'Element ID', 'Family', 'Type', 'Mark', 'Level'] + area_columns]
    volume_data = df[['Category', 'Element ID', 'Family', 'Type', 'Mark', 'Level'] + volume_columns]

    # Remove rows with all NaN values in area columns
    area_data = area_data.dropna(subset=area_columns, how='all')

    # Remove rows with all NaN values in volume columns
    volume_data = volume_data.dropna(subset=volume_columns, how='all')

    # Remove completely empty columns (only header)
    area_data = area_data.dropna(axis=1, how='all')
    volume_data = volume_data.dropna(axis=1, how='all')

    save_excel(area_data, "Save Area Data", "area_data.xlsx")
    save_excel(volume_data, "Save Volume Data", "volume_data.xlsx")


def save_excel(df, dialog_title, default_filename):
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", title=dialog_title, initialfile=default_filename,
                                             filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"File saved successfully: {file_path}")
        except PermissionError:
            messagebox.showerror("Error",
                                 f"Permission denied: {file_path}. Please close the file if it's open and try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the Excel file: {e}")


app = ctk.CTk()
app.title("Excel to Excel Processor")

frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20)

label = ctk.CTkLabel(frame, text="Excel to Excel Processor", font=("Arial", 16))
label.pack(pady=10)

load_button = ctk.CTkButton(frame, text="Load Excel File", command=load_excel_file)
load_button.pack(pady=10)

app.mainloop()
