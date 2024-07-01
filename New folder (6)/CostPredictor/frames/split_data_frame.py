import os
from tkinter import filedialog, messagebox
import pandas as pd
import customtkinter
from helpers import get_current_fg_color

def create_split_data_frame(root):
    frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(8, weight=1)

    input_file_var = customtkinter.StringVar()
    output_folder_var = customtkinter.StringVar()
    category_vars = {}

    def select_input_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            input_file_var.set(file_path)
            input_file_label.configure(text=f"Selected file: {os.path.basename(file_path)}")

    def select_output_path():
        folder_path = filedialog.askdirectory()
        if folder_path:
            output_folder_var.set(folder_path)
            output_folder_label.configure(text=f"Selected folder: {os.path.basename(folder_path)}")

    def scan_and_create():
        nonlocal category_vars
        category_vars = scan_and_create_checkboxes(frame, input_file_var, categories_frame)

    customtkinter.CTkLabel(frame, text="Select input Excel file:").grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")
    input_file_button = customtkinter.CTkButton(frame, text="Browse...", command=select_input_file, width=100)
    input_file_button.grid(row=1, column=0, padx=20, pady=5, sticky="w")
    input_file_label = customtkinter.CTkLabel(frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
    input_file_label.grid(row=1, column=1, padx=20, pady=5, sticky="w")

    customtkinter.CTkLabel(frame, text="Select output folder:").grid(row=2, column=0, padx=20, pady=(20, 5), sticky="ew")
    output_folder_button = customtkinter.CTkButton(frame, text="Browse...", command=select_output_path, width=100)
    output_folder_button.grid(row=3, column=0, padx=20, pady=5, sticky="w")
    output_folder_label = customtkinter.CTkLabel(frame, text="No folder selected", text_color=("gray50", "gray50"), wraplength=400)
    output_folder_label.grid(row=3, column=1, padx=20, pady=5, sticky="w")

    categories_frame = customtkinter.CTkScrollableFrame(frame)
    categories_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    scan_button = customtkinter.CTkButton(frame, text="Scan and Create Checkboxes", command=scan_and_create, width=150)
    scan_button.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="sew")

    sort_button = customtkinter.CTkButton(frame, text="Sort Selected Categories",
                                          command=lambda: sort_selected_categories(input_file_var.get(), output_folder_var.get(), category_vars), width=150)
    sort_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="sew")

    return frame

def scan_and_create_checkboxes(frame, input_file_var, categories_frame):
    input_file = input_file_var.get()
    if not input_file:
        messagebox.showerror("Error", "Please select an input file first")
        return

    try:
        data = pd.read_excel(input_file)
        categories = data['Category'].unique()

        for widget in categories_frame.winfo_children():
            widget.destroy()

        category_vars = {}
        row, col = 0, 0
        for category in categories:
            var = customtkinter.StringVar(value="0")
            checkbox = customtkinter.CTkCheckBox(categories_frame, text=category, variable=var)
            checkbox.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            category_vars[category] = var

            col += 1
            if col == 2:
                col = 0
                row += 1

        return category_vars

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while scanning the file: {e}")

def sort_selected_categories(input_file, output_folder, category_vars):
    if not input_file or not output_folder:
        messagebox.showerror("Error", "Please select both input file and output folder")
        return

    try:
        sorted_output_path = os.path.join(output_folder, "Sorted_Data.xlsx")
        cleaned_output_path = os.path.join(output_folder, "Cleaned_Sorted_Data.xlsx")

        data = pd.read_excel(input_file)
        selected_categories = [category for category, var in category_vars.items() if var.get() == "1"]
        category_data = {category: data[data['Category'].str.contains(category, case=False, na=False)] for category in selected_categories}

        with pd.ExcelWriter(sorted_output_path, engine='xlsxwriter') as writer:
            for category, df in category_data.items():
                df.to_excel(writer, sheet_name=category, index=False)

        sorted_excel_data = pd.ExcelFile(sorted_output_path)
        cleaned_data = {}
        for sheet_name in sorted_excel_data.sheet_names:
            df = pd.read_excel(sorted_output_path, sheet_name=sheet_name)
            cleaned_df = df.dropna(axis=1, how='all')
            cleaned_data[sheet_name] = cleaned_df

        with pd.ExcelWriter(cleaned_output_path, engine='xlsxwriter') as writer:
            for sheet_name, df in cleaned_data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        messagebox.showinfo("Success", f"Sorted data has been saved to {sorted_output_path}\nCleaned data has been saved to {cleaned_output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
