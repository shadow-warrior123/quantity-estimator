import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def calculate_material_totals(input_file, output_folder):
    # Load the Excel file
    excel_data = pd.ExcelFile(input_file)
    sheet_names = excel_data.sheet_names

    # Initialize a dictionary to hold the data for each sheet
    sheets_data = {}

    # Iterate through each sheet and process the data
    for sheet in sheet_names:
        sheet_data = pd.read_excel(input_file, sheet_name=sheet)
        if 'Element ID' in sheet_data.columns:
            sheet_data = sheet_data.drop(columns=['Element ID'])
        material_totals = sheet_data.select_dtypes(include='number').sum()
        sheets_data[sheet] = material_totals

    # Create a new Excel writer object
    output_file_path = os.path.join(output_folder, 'Detailed_Total_Material_Used_No_Element_ID.xlsx')
    with pd.ExcelWriter(output_file_path) as writer:
        for sheet, data in sheets_data.items():
            # Convert the Series to DataFrame for better formatting
            material_totals_df = data.reset_index()
            material_totals_df.columns = ['Material', 'Total Quantity Used']
            # Write each sheet's data to the Excel file
            material_totals_df.to_excel(writer, sheet_name=sheet, index=False)

    messagebox.showinfo("Success", f"Processed file saved to {output_file_path}")


def select_input_file():
    input_file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file)


def select_output_folder():
    output_folder = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_folder)


def process_file():
    input_file = input_entry.get()
    output_folder = output_entry.get()
    if not input_file or not output_folder:
        messagebox.showerror("Error", "Please select both input file and output folder")
        return
    calculate_material_totals(input_file, output_folder)


# Create the GUI
root = tk.Tk()
root.title("Material Totals Calculator")

tk.Label(root, text="Select Input Excel File:").grid(row=0, column=0, padx=10, pady=10)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Select Output Folder:").grid(row=1, column=0, padx=10, pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=10)

tk.Button(root, text="Process File", command=process_file).grid(row=2, column=0, columnspan=3, padx=10, pady=20)

root.mainloop()
