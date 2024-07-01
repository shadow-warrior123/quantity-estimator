import os
import pandas as pd
from tkinter import filedialog, messagebox
from PIL import Image
import customtkinter
from helpers import get_current_fg_color
import numpy as np
from reformat import reformat_and_split_excel, level_params

def create_home_frame(root):
    home_frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    home_frame.grid_columnconfigure(0, weight=1)
    home_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

    welcome_label = customtkinter.CTkLabel(home_frame, text="Welcome!", font=customtkinter.CTkFont(size=72),
                                           text_color=("black", "white"))
    welcome_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    home_frame_label = customtkinter.CTkLabel(home_frame,
                                              text="This is a sample GUI created using customTkinter just for demonstration purposes.",
                                              text_color=("black", "white"))
    home_frame_label.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    developed_by_label = customtkinter.CTkLabel(home_frame, text="Developed by Ladybug",
                                                font=customtkinter.CTkFont(size=15), text_color=("black", "white"))
    developed_by_label.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    return home_frame

def create_frame(root, name):
    frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    frame.grid_columnconfigure(0, weight=1)
    label = customtkinter.CTkLabel(frame, text=name, text_color=("black", "white"))
    label.grid(row=0, column=0, padx=20, pady=10)

    if name == "Sort":
        create_sort_section(frame)
    elif name == "Reformat":
        create_reformat_section(frame)
    elif name == "Split Data":
        create_split_data_frame(frame)

    return frame

def create_sort_section(frame):
    input_file_var = customtkinter.StringVar()
    sample_file_var = customtkinter.StringVar()
    output_folder_var = customtkinter.StringVar()

    def select_input_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            input_file_var.set(file_path)
            input_file_label.configure(text=f"Selected file: {os.path.basename(file_path)}")

    def select_sample_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            sample_file_var.set(file_path)
            sample_file_label.configure(text=f"Selected file: {os.path.basename(file_path)}")

    def select_output_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            output_folder_var.set(folder_path)
            output_folder_label.configure(text=f"Selected folder: {os.path.basename(folder_path)}")

    def process_data():
        raw_data_path = input_file_var.get()
        sample_data_path = sample_file_var.get()
        output_folder = output_folder_var.get()

        if not raw_data_path or not sample_data_path or not output_folder:
            messagebox.showerror("Error", "Please select all the required files and folder.")
            return

        output_path = os.path.join(output_folder, "Processed_Data.xlsx")

        try:
            automate_data_processing(raw_data_path, sample_data_path, output_path)
            messagebox.showinfo("Success", f"Data has been processed and saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    customtkinter.CTkLabel(frame, text="Select input Excel file:").grid(row=1, column=0, padx=20, pady=(20, 5), sticky="ew")
    input_file_button = customtkinter.CTkButton(frame, text="Browse...", command=select_input_file, width=100)
    input_file_button.grid(row=2, column=0, padx=20, pady=5, sticky="w")
    input_file_label = customtkinter.CTkLabel(frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
    input_file_label.grid(row=2, column=1, padx=20, pady=5, sticky="w")

    customtkinter.CTkLabel(frame, text="Select sample Excel file:").grid(row=3, column=0, padx=20, pady=(20, 5), sticky="ew")
    sample_file_button = customtkinter.CTkButton(frame, text="Browse...", command=select_sample_file, width=100)
    sample_file_button.grid(row=4, column=0, padx=20, pady=5, sticky="w")
    sample_file_label = customtkinter.CTkLabel(frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
    sample_file_label.grid(row=4, column=1, padx=20, pady=5, sticky="w")

    customtkinter.CTkLabel(frame, text="Select output folder:").grid(row=5, column=0, padx=20, pady=(20, 5), sticky="ew")
    output_folder_button = customtkinter.CTkButton(frame, text="Browse...", command=select_output_folder, width=100)
    output_folder_button.grid(row=6, column=0, padx=20, pady=5, sticky="w")
    output_folder_label = customtkinter.CTkLabel(frame, text="No folder selected", text_color=("gray50", "gray50"), wraplength=400)
    output_folder_label.grid(row=6, column=1, padx=20, pady=5, sticky="w")

    process_button = customtkinter.CTkButton(frame, text="Process Data", command=process_data, width=150)
    process_button.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky="sew")

def create_reformat_section(frame):
    input_file_var = customtkinter.StringVar()
    output_folder_var = customtkinter.StringVar()

    def select_input_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            input_file_var.set(file_path)
            input_file_label.configure(text=f"Selected file: {os.path.basename(file_path)}")

    def select_output_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            output_folder_var.set(folder_path)
            output_folder_label.configure(text=f"Selected folder: {os.path.basename(folder_path)}")

    def process_data():
        raw_data_path = input_file_var.get()
        output_folder = output_folder_var.get()

        if not raw_data_path or not output_folder:
            messagebox.showerror("Error", "Please select all the required files and folder.")
            return

        output_path = os.path.join(output_folder, "Reformatted_Data.xlsx")

        try:
            reformat_and_split_excel(raw_data_path, output_path, level_params)
            messagebox.showinfo("Success", f"Data has been reformatted and saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    customtkinter.CTkLabel(frame, text="Select input Excel file:").grid(row=1, column=0, padx=20, pady=(20, 5), sticky="ew")
    input_file_button = customtkinter.CTkButton(frame, text="Browse...", command=select_input_file, width=100)
    input_file_button.grid(row=2, column=0, padx=20, pady=5, sticky="w")
    input_file_label = customtkinter.CTkLabel(frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
    input_file_label.grid(row=2, column=1, padx=20, pady=5, sticky="w")

    customtkinter.CTkLabel(frame, text="Select output folder:").grid(row=3, column=0, padx=20, pady=(20, 5), sticky="ew")
    output_folder_button = customtkinter.CTkButton(frame, text="Browse...", command=select_output_folder, width=100)
    output_folder_button.grid(row=4, column=0, padx=20, pady=5, sticky="w")
    output_folder_label = customtkinter.CTkLabel(frame, text="No folder selected", text_color=("gray50", "gray50"), wraplength=400)
    output_folder_label.grid(row=4, column=1, padx=20, pady=5, sticky="w")

    process_button = customtkinter.CTkButton(frame, text="Reformat Data", command=process_data, width=150)
    process_button.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="sew")

def create_split_data_frame(root):
    split_data_frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    split_data_frame.grid_columnconfigure(0, weight=1)
    split_data_frame.grid_rowconfigure(8, weight=1)

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
        category_vars = scan_and_create_checkboxes(split_data_frame, input_file_var, categories_frame)

    customtkinter.CTkLabel(split_data_frame, text="Select input Excel file:").grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")
    input_file_button = customtkinter.CTkButton(split_data_frame, text="Browse...", command=select_input_file, width=100)
    input_file_button.grid(row=1, column=0, padx=20, pady=5, sticky="w")
    input_file_label = customtkinter.CTkLabel(split_data_frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
    input_file_label.grid(row=1, column=1, padx=20, pady=5, sticky="w")

    customtkinter.CTkLabel(split_data_frame, text="Select output folder:").grid(row=2, column=0, padx=20, pady=(20, 5), sticky="ew")
    output_folder_button = customtkinter.CTkButton(split_data_frame, text="Browse...", command=select_output_path, width=100)
    output_folder_button.grid(row=3, column=0, padx=20, pady=5, sticky="w")
    output_folder_label = customtkinter.CTkLabel(split_data_frame, text="No folder selected", text_color=("gray50", "gray50"), wraplength=400)
    output_folder_label.grid(row=3, column=1, padx=20, pady=5, sticky="w")

    categories_frame = customtkinter.CTkScrollableFrame(split_data_frame)
    categories_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    scan_button = customtkinter.CTkButton(split_data_frame, text="Scan and Create Checkboxes", command=scan_and_create, width=150)
    scan_button.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="sew")

    sort_button = customtkinter.CTkButton(split_data_frame, text="Sort Selected Categories",
                                          command=lambda: sort_selected_categories(input_file_var.get(), output_folder_var.get(), category_vars), width=150)
    sort_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="sew")

    return split_data_frame

def scan_and_create_checkboxes(split_data_frame, input_file_var, categories_frame):
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

def select_frame(frame_name, frames, buttons):
    for frame in frames.values():
        frame.grid_forget()
    frames[frame_name].grid(row=0, column=1, sticky="nsew")
    for button_name, button in buttons.items():
        button.configure(fg_color=("gray75", "gray25") if button_name == frame_name else "transparent")

def toggle_theme(frames, theme_toggle_switch):
    current_mode = customtkinter.get_appearance_mode()
    new_mode = "Dark" if current_mode == "Light" else "Light"
    customtkinter.set_appearance_mode(new_mode)

    new_bg_color = get_current_fg_color()
    for frame in frames.values():
        frame.configure(fg_color=new_bg_color)

    theme_toggle_switch.select() if new_mode == "Dark" else theme_toggle_switch.deselect()
