import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox


# Function to extract prefix (category) and suffix (level) from sheet name
def extract_prefix_suffix(sheet_name):
    parts = sheet_name.split('_')
    if len(parts) > 1:
        prefix = '_'.join(parts[:-1])
        suffix = parts[-1]
    else:
        prefix = parts[0]
        suffix = ""
    return prefix, suffix


# Function to process the Excel file
def process_excel_file(input_file, output_folder):
    # Load the provided Excel file to get the detailed data without 'Element ID' column
    excel_data = pd.ExcelFile(input_file)

    # Initialize a dictionary to hold data categorized by levels
    levels_data_formatted = {}

    # Iterate through each sheet and categorize the data by cleaned levels
    for sheet in excel_data.sheet_names:
        sheet_data = pd.read_excel(input_file, sheet_name=sheet)
        category, level = extract_prefix_suffix(sheet)

        if level not in levels_data_formatted:
            levels_data_formatted[level] = []

        levels_data_formatted[level].append((category, sheet_data))

    # Create a new Excel writer object for the updated file
    output_file_path = os.path.join(output_folder, 'Formatted_Combined_Levels_Data.xlsx')
    with pd.ExcelWriter(output_file_path) as writer:
        for level, data_list in levels_data_formatted.items():
            combined_data = pd.DataFrame()
            for category, data in data_list:
                # Add category name as a header
                category_header = pd.DataFrame([[category, '']], columns=['Material', 'Total Quantity Used'])
                # Add table header for materials table
                combined_data = pd.concat([combined_data, category_header], ignore_index=True)
                combined_data = pd.concat([combined_data, data], ignore_index=True)
                # Add three rows of gap
                combined_data = pd.concat(
                    [combined_data, pd.DataFrame([['', '']] * 3, columns=['Material', 'Total Quantity Used'])],
                    ignore_index=True)

            combined_data.to_excel(writer, sheet_name=level, index=False)

    messagebox.showinfo("Success", f"Processed file saved to {output_file_path}")


# GUI for selecting input file and output directory
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
    process_excel_file(input_file, output_folder)


# Create the GUI
root = tk.Tk()
root.title("Excel Data Formatter")

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
