import os
from tkinter import filedialog, messagebox
import customtkinter
from fetch_unit_prices import fetch_unit_prices
from helpers import get_current_fg_color

def create_unit_prices_frame(root):
    frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=0)

    # Header
    header_label = customtkinter.CTkLabel(frame, text="Fetch Unit Prices", font=customtkinter.CTkFont(size=18, weight="bold"), text_color=("black", "white"))
    header_label.grid(row=0, column=0, padx=20, pady=30, sticky="ew")

    state_var = customtkinter.StringVar()
    output_folder_var = customtkinter.StringVar()

    states = [
        "Andaman and Nicobar", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh",
        "Chhattisgarh", "Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana",
        "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Lakshadweep",
        "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha",
        "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
        "Uttarakhand", "West Bengal"
    ]

    def select_output_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            output_folder_var.set(folder_path)
            output_folder_display.configure(text=f"Selected folder: {folder_path}")

    def fetch_data():
        state = state_var.get()
        output_folder = output_folder_var.get()

        if not state:
            messagebox.showerror("Error", "Please select a state.")
            return

        if not output_folder:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        try:
            excel_file = fetch_unit_prices(state)
            output_path = os.path.join(output_folder, os.path.basename(excel_file))
            os.rename(excel_file, output_path)
            messagebox.showinfo("Success", f"Data has been saved to {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # State selection
    state_label = customtkinter.CTkLabel(frame, text="Select state:")
    state_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="w")
    state_combobox = customtkinter.CTkComboBox(frame, values=states, variable=state_var, width=300)
    state_combobox.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

    # Output folder selection
    output_folder_label = customtkinter.CTkLabel(frame, text="Select output folder:")
    output_folder_label.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="w")
    output_folder_button = customtkinter.CTkButton(frame, text="Browse...", command=select_output_folder, width=100)
    output_folder_button.grid(row=4, column=0, padx=20, pady=5, sticky="w")
    output_folder_display = customtkinter.CTkLabel(frame, text="No folder selected", text_color=("gray50", "gray50"), wraplength=400)
    output_folder_display.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

    # Fetch button
    fetch_button = customtkinter.CTkButton(frame, text="Get Unit Prices", command=fetch_data, width=150)
    fetch_button.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

    return frame
