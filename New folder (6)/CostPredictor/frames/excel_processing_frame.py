import os
import pandas as pd
from tkinter import filedialog, messagebox
import customtkinter
from helpers import get_current_fg_color

def categorize_sheets(sheet_names):
    categories = {
        'Structural Columns': [],
        'Walls': [],
        'Floors': [],
        'Doors': [],
        'Railings': [],
        'Ceilings': [],
        'Structural Framing': [],
        'Structural Foundations': [],
        'Stairs': []
    }

    for sheet in sheet_names:
        for category in categories.keys():
            if category.lower() in sheet.lower():
                categories[category].append(sheet)
                break

    return categories

def find_closest_column_match(available_columns, desired_column):
    available_lower = [col.lower() for col in available_columns]
    desired_lower = desired_column.lower()

    if desired_lower in available_lower:
        return available_columns[available_lower.index(desired_lower)]

    for col in available_columns:
        if desired_lower in col.lower() or col.lower() in desired_lower:
            return col

    return None

def update_sheet(file_path, sheet_name, columns_to_keep, new_columns):
    try:
        sheet_data = pd.read_excel(file_path, sheet_name=sheet_name)
        available_columns = sheet_data.columns.tolist()

        matched_columns = []
        for col in columns_to_keep:
            matched_col = find_closest_column_match(available_columns, col)
            if matched_col:
                matched_columns.append(matched_col)
            else:
                print(f"Warning: Column '{col}' not found in sheet '{sheet_name}'. Skipping this column.")

        sheet_data_filtered = sheet_data[matched_columns]

        if len(sheet_data_filtered.columns) == len(new_columns):
            sheet_data_filtered.columns = new_columns
        else:
            print(f"Warning: Number of columns in sheet '{sheet_name}' does not match expected number. Using original column names.")

        return sheet_data_filtered
    except Exception as e:
        print(f"Error processing sheet '{sheet_name}': {str(e)}")
        return pd.DataFrame()

def save_updated_sheets(output_file_path, updated_sheets_data):
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        for sheet_name, data in updated_sheets_data.items():
            if not data.empty:
                data.to_excel(writer, sheet_name=sheet_name, index=False)

def list_sheet_names(file_path):
    excel_file = pd.ExcelFile(file_path)
    return excel_file.sheet_names

def process_file(input_file_path, output_file_path):
    updated_sheets_data = {}
    sheet_names = list_sheet_names(input_file_path)
    categories = categorize_sheets(sheet_names)

    column_mappings = {
        'Structural Columns': {
            'columns': ['Category', 'Base Level', 'Element Name', 'Element ID', 'Volume', 'Family', 'Type'],
            'new_columns': ['category', 'level', 'Element name', 'Element Id', 'volume', 'family', 'type']
        },
        'Walls': {
            'columns': ['Category', 'Base Constraint', 'Element Name', 'Element ID', 'Area', 'Volume', 'Type'],
            'new_columns': ['category', 'level', 'Element name', 'Element Id', 'area', 'volume', 'family', 'type']
        },
        'Floors': {
            'columns': ['Category', 'Element Name', 'Element ID', 'Area', 'Volume', 'Type', 'Core Thickness'],
            'new_columns': ['category', 'Element name', 'Element Id', 'area', 'volume', 'type', 'thickness']
        },
        'Doors': {
            'columns': ['Category', 'Element ID', 'Element Name', 'Head Height', 'Family', 'Type'],
            'new_columns': ['category', 'Element Id', 'Element name', 'head height', 'family', 'type']
        },
        'Railings': {
            'columns': ['Category', 'Base Level', 'Element ID', 'Element Name', 'Family', 'Type', 'Length'],
            'new_columns': ['category', 'level', 'Element Id', 'Element name', 'family', 'type', 'length']
        },
        'Ceilings': {
            'columns': ['Category', 'Level', 'Element ID', 'Element Name', 'Family', 'Type', 'Volume', 'Area'],
            'new_columns': ['category', 'level', 'Element Id', 'Element name', 'family', 'type', 'volume', 'area']
        },
        'Structural Framing': {
            'columns': ['Category', 'Element ID', 'Element Name', 'Family', 'Type', 'Work Plane', 'Volume'],
            'new_columns': ['category', 'Element Id', 'Element name', 'family', 'type', 'level', 'volume']
        },
        'Structural Foundations': {
            'columns': ['Category', 'Element ID', 'Element Name', 'Family', 'Type', 'Level', 'Volume', 'Elevation at Top', 'Elevation at Bottom'],
            'new_columns': ['category', 'Element Id', 'Element name', 'family', 'type', 'level', 'volume', 'elevation at top', 'elevation at bottom']
        },
        'Stairs': {
            'columns': ['Category', 'Element Name', 'Element ID', 'Number of Risers', 'Actual Riser Height', 'Actual Tread Depth', 'Base Level', 'Desired Number of Risers', 'Desired Stair Height', 'Family', 'Mark', 'Top Level', 'Type'],
            'new_columns': ['category', 'Element name', 'Element Id', 'number of risers', 'actual riser height', 'actual tread depth', 'base level', 'desired number of risers', 'desired stair height', 'family', 'mark', 'top level', 'type']
        }
    }

    for category, sheets in categories.items():
        for sheet in sheets:
            if sheet in sheet_names:
                columns = column_mappings[category]['columns']
                new_columns = column_mappings[category]['new_columns']
                updated_sheet = update_sheet(input_file_path, sheet, columns, new_columns)
                if not updated_sheet.empty:
                    updated_sheets_data[sheet] = updated_sheet

    save_updated_sheets(output_file_path, updated_sheets_data)

def create_excel_processing_frame(root):
    frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0)

    # Header
    header_label = customtkinter.CTkLabel(frame, text="Excel Sheet Processor", font=customtkinter.CTkFont(size=18, weight="bold"), text_color=("black", "white"))
    header_label.grid(row=0, column=0, padx=20, pady=30, sticky="ew")

    input_file_var = customtkinter.StringVar()
    output_folder_var = customtkinter.StringVar()

    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            input_file_var.set(file_path)
            input_file_display.configure(text=f"Selected file: {file_path}")

    def select_output_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            output_folder_var.set(folder_path)
            output_folder_display.configure(text=f"Selected folder: {folder_path}")

    def start_processing():
        input_file_path = input_file_var.get()
        output_folder_path = output_folder_var.get()
        if input_file_path and output_folder_path:
            output_file_path = os.path.join(output_folder_path, "output_file.xlsx")
            process_file(input_file_path, output_file_path)
            messagebox.showinfo("Success", f"Processed file saved to {output_file_path}")
        else:
            messagebox.showerror("Error", "Please select both input file and output folder")

    # Input file selection
    input_file_label = customtkinter.CTkLabel(frame, text="Select Input Excel File:")
    input_file_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")
    input_file_button = customtkinter.CTkButton(frame, text="Browse...", command=select_file, width=100)
    input_file_button.grid(row=2, column=0, padx=20, pady=5, sticky="w")
    input_file_display = customtkinter.CTkLabel(frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
    input_file_display.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

    # Output folder selection
    output_folder_label = customtkinter.CTkLabel(frame, text="Select Output Folder:")
    output_folder_label.grid(row=4, column=0, padx=20, pady=(10, 5), sticky="w")
    output_folder_button = customtkinter.CTkButton(frame, text="Browse...", command=select_output_folder, width=100)
    output_folder_button.grid(row=5, column=0, padx=20, pady=5, sticky="w")
    output_folder_display = customtkinter.CTkLabel(frame, text="No folder selected", text_color=("gray50", "gray50"), wraplength=400)
    output_folder_display.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

    # Start processing button
    start_button = customtkinter.CTkButton(frame, text="Start Processing", command=start_processing, width=150)
    start_button.grid(row=7, column=0, padx=20, pady=20, sticky="ew")

    return frame
