import customtkinter as ctk
import subprocess
import os

def create_quantity_calc_frame(root):
    frame = ctk.CTkFrame(root, corner_radius=0)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0)

    label = ctk.CTkLabel(frame, text="Quantity Calculation Functions", font=ctk.CTkFont(size=18, weight="bold"))
    label.grid(row=0, column=0, padx=20, pady=30, sticky="ew")

    def run_demerger():
        script_path = os.path.join(os.path.dirname(__file__), "demerging_area_volume.py")
        subprocess.Popen(["python", script_path])

    def run_chart_processor():
        script_path = os.path.join(os.path.dirname(__file__), "display_chart.py")
        subprocess.Popen(["python", script_path])

    def run_quantity_calculator():
        script_path = os.path.join(os.path.dirname(__file__), "quantity_calculator.py")
        subprocess.Popen(["python", script_path])

    def run_sorting_excel():
        script_path = os.path.join(os.path.dirname(__file__), "sorting_excel_data.py")
        subprocess.Popen(["python", script_path])

    demerger_button = ctk.CTkButton(frame, text="Demerging Area and Volume", command=run_demerger)
    demerger_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    chart_processor_button = ctk.CTkButton(frame, text="Display Chart", command=run_chart_processor)
    chart_processor_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    quantity_calculator_button = ctk.CTkButton(frame, text="Quantity Calculator", command=run_quantity_calculator)
    quantity_calculator_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

    sorting_excel_button = ctk.CTkButton(frame, text="Sorting Excel Data", command=run_sorting_excel)
    sorting_excel_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    return frame
