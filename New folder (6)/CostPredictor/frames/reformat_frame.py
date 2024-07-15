import os
import customtkinter
from tkinter import filedialog, messagebox
from helpers import get_current_fg_color
from reformat import reformat_and_split_excel, level_params

def create_reformat_frame(root):
    frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0)

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

    return frame
