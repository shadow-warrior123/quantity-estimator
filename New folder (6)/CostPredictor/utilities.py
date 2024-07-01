import os
import requests
from PIL import Image
import pandas as pd
import numpy as np
import customtkinter
from tkinter import filedialog, messagebox

def get_current_fg_color():
    current_mode = customtkinter.get_appearance_mode()
    return customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][0 if current_mode == "Light" else 1]

def setup_images():
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
    logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(30, 30))
    return logo_image

def process_data(input_file, output_file):
    # Implement the data processing logic
    pass

def browse_file(entry_var):
    filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    entry_var.set(filename)

def save_file(save_var):
    filename = filedialog.asksaveasfilename


def save_file(save_var):
    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    save_var.set(filename)


def merge_files(file1, file2, output_file):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    merged_df = pd.merge(df1, df2, on='common_column')
    merged_df.to_excel(output_file, index=False)


def upload_to_power_bi(file, sheet):
    df = pd.read_excel(file, sheet_name=sheet)
    # Implement the Power BI upload logic


def get_unit_price(material_name):
    url = f"https://api.example.com/materials/{material_name}/price"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['unit_price']
    else:
        return None


def scan_and_create_checkboxes(frame, input_file_var, categories_frame):
    input_file = input_file_var.get()
    if not input_file:
        messagebox.showerror("Error", "Please select an input file first")
        return

    try:
        # Read all sheet names from the Excel file
        excel_file = pd.ExcelFile(input_file)
        sheet_names = excel_file.sheet_names

        # Clear previous checkboxes
        for widget in categories_frame.winfo_children():
            widget.destroy()

        # Create checkboxes for each sheet
        sheet_vars = {}
        row, col = 0, 0
        for sheet_name in sheet_names:
            var = customtkinter.StringVar(value="0")
            checkbox = customtkinter.CTkCheckBox(categories_frame, text=sheet_name, variable=var)
            checkbox.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            sheet_vars[sheet_name] = var

            col += 1
            if col == 2:
                col = 0
                row += 1

        return sheet_vars

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while scanning the file: {e}")


def sort_selected_categories(input_file, output_folder, sheet_vars):
    if not input_file or not output_folder:
        messagebox.showerror("Error", "Please select both input file and output folder")
        return

    try:
        output_file = os.path.join(output_folder, "Selected_Sheets.xlsx")

        # Read the selected sheets from the input file
        selected_sheets = [sheet for sheet, var in sheet_vars.items() if var.get() == "1"]

        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            for sheet in selected_sheets:
                df = pd.read_excel(input_file, sheet_name=sheet)
                df.to_excel(writer, sheet_name=sheet, index=False)

        messagebox.showinfo("Success", f"Selected sheets have been saved to {output_file}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def automate_data_processing(raw_data_path, sample_data_path, output_path):
    # Load the raw data
    df = pd.read_excel(raw_data_path, sheet_name='Revit Data')

    # List of categories to keep
    categories_to_keep = [
        'Ceilings', 'Doors', 'Floors', 'Railings', 'Stairs',
        'Structural Columns', 'Structural Framing', 'Structural Foundations',
        'Walls', 'Windows'
    ]

    # Initialize a dictionary to hold DataFrames for each category
    category_dfs = {category: df[df['Category'] == category].copy() for category in categories_to_keep}

    # Remove N/A values and replace with NaN
    for category, category_df in category_dfs.items():
        category_dfs[category] = category_df.replace('N/A', np.nan)

    # Remove categories that don't contain any parameter values
    category_dfs = {category: category_df for category, category_df in category_dfs.items() if
                    not category_df.dropna(axis=1, how='all').empty}

    # Load the sample data to determine which parameters to keep
    sample_excel_data = pd.ExcelFile(sample_data_path)
    sample_data = {sheet: pd.read_excel(sample_data_path, sheet_name=sheet) for sheet in sample_excel_data.sheet_names}
    sample_parameters = {sheet: set(df.columns) for sheet, df in sample_data.items()}

    # Remove columns that are not present in the sample data for each corresponding sheet in the cleaned data
    for category, category_df in category_dfs.items():
        if category in sample_parameters:
            params_to_keep = sample_parameters[category]
            category_dfs[category] = category_df[category_df.columns.intersection(params_to_keep)]

    # Sort each sheet by 'Level' in ascending order, if 'Level' column exists
    for category, category_df in category_dfs.items():
        if 'Level' in category_df.columns:
            category_dfs[category] = category_df.sort_values(by='Level')

    # Save the updated cleaned data
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for category, category_df in category_dfs.items():
            category_df.to_excel(writer, sheet_name=category, index=False)
