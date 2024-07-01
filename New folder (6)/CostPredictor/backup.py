# import os
# import tkinter as tk
# from tkinter import filedialog, messagebox
# import pandas as pd
# from PIL import Image
# import customtkinter
# from openpyxl.styles import Font, Border, Side, PatternFill
#
# # Helper functions
# def get_current_fg_color():
#     current_mode = customtkinter.get_appearance_mode()
#     return customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][0 if current_mode == "Light" else 1]
#
# def find_level_column(df, params):
#     for param in params:
#         if param in df.columns:
#             return param
#     return None
#
# def reformat_excel(input_file_path, output_file_path, level_params):
#     workbook = pd.ExcelFile(input_file_path)
#     sheets_data = []
#
#     for sheet_name in workbook.sheet_names:
#         df = pd.read_excel(workbook, sheet_name=sheet_name, header=0)
#         sheets_data.append((sheet_name, df))
#
#     reformatted_data = pd.DataFrame()
#     reformatted_data = pd.concat([reformatted_data, pd.DataFrame([[pd.NA] * len(sheets_data[0][1].columns)] * 5)], ignore_index=True)
#
#     for sheet_name, df in sheets_data:
#         level_col = find_level_column(df, level_params)
#         if level_col is not None:
#             grouped = df.groupby(level_col)
#             for level, group in grouped:
#                 level_info = pd.DataFrame([[f"{level_col}: {level}"] + [pd.NA] * (len(df.columns) - 1)], columns=df.columns)
#                 reformatted_data = pd.concat([reformatted_data, level_info], ignore_index=True)
#
#                 name_df = pd.DataFrame([[sheet_name]] + [[pd.NA] * len(df.columns)], columns=df.columns)
#                 reformatted_data = pd.concat([reformatted_data, name_df], ignore_index=True)
#
#                 reformatted_data = pd.concat([reformatted_data, pd.DataFrame([df.columns], columns=df.columns)], ignore_index=True)
#                 reformatted_data = pd.concat([reformatted_data, group], ignore_index=True)
#                 reformatted_data = pd.concat([reformatted_data, pd.DataFrame([[pd.NA] * len(df.columns)] * 5)], ignore_index=True)
#         else:
#             name_df = pd.DataFrame([[sheet_name]] + [[pd.NA] * len(df.columns)], columns=df.columns)
#             reformatted_data = pd.concat([reformatted_data, name_df], ignore_index=True)
#             reformatted_data = pd.concat([reformatted_data, pd.DataFrame([df.columns], columns=df.columns)], ignore_index=True)
#             reformatted_data = pd.concat([reformatted_data, df], ignore_index=True)
#             reformatted_data = pd.concat([reformatted_data, pd.DataFrame([[pd.NA] * len(df.columns)] * 5)], ignore_index=True)
#
#     reformatted_data.to_excel(output_file_path, index=False, header=False)
#     print(f"Reformatted data saved to: {output_file_path}")
#
# def setup_images():
#     image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
#     logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(30, 30))
#     return logo_image
#
# # GUI related functions
# def create_navigation_frame(root, logo_image, toggle_theme, select_frame):
#     navigation_frame = customtkinter.CTkFrame(root, corner_radius=0, width=200, fg_color=("#D4D4D4","#323232"))
#     navigation_frame.grid(row=0, column=0, sticky="nsew")
#     root.grid_rowconfigure(0, weight=1)
#
#     navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text="   Ladybug", image=logo_image,
#                                                     compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
#     navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
#
#     home_button = create_nav_button(navigation_frame, "Home", lambda: select_frame("home"))
#     sort_button = create_nav_button(navigation_frame, "Sort", lambda: select_frame("sort"))
#     split_data_button = create_nav_button(navigation_frame, "Split Data", lambda: select_frame("split_data"))
#     reformat_button = create_nav_button(navigation_frame, "Reformat", lambda: select_frame("reformat"))
#
#     home_button.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
#     sort_button.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
#     split_data_button.grid(row=3, column=0, sticky="ew", padx=20, pady=5)
#     reformat_button.grid(row=4, column=0, sticky="ew", padx=20, pady=5)
#
#     navigation_frame.grid_rowconfigure(97, weight=1)
#
#     def quit_app():
#         root.quit()
#
#     quit_button = customtkinter.CTkButton(navigation_frame, text="Quit", command=quit_app, fg_color="#BA0B13", hover_color="#94070D")
#     quit_button.grid(row=99, column=0, padx=20, pady=(10,30), sticky="ew")
#
#     theme_toggle_switch = customtkinter.CTkSwitch(navigation_frame, text="Dark Mode", command=toggle_theme)
#     theme_toggle_switch.grid(row=98, column=0, padx=20, pady=10, sticky="sew")
#
#     return home_button, sort_button, split_data_button, reformat_button, theme_toggle_switch
#
# def create_nav_button(parent, text, command):
#     button = customtkinter.CTkButton(parent, corner_radius=6, height=40, border_spacing=10, text=text,
#                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=command)
#     button.grid(sticky="ew")
#     return button
#
# def create_home_frame(root):
#     home_frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
#     home_frame.grid_columnconfigure(0, weight=1)
#     home_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
#
#     welcome_label = customtkinter.CTkLabel(home_frame, text="Welcome!", font=customtkinter.CTkFont(size=72),
#                                            text_color=("black", "white"))
#     welcome_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
#
#     home_frame_label = customtkinter.CTkLabel(home_frame,
#                                               text="This is a sample GUI created using customTkinter just for demonstration purposes.",
#                                               text_color=("black", "white"))
#     home_frame_label.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
#
#     developed_by_label = customtkinter.CTkLabel(home_frame, text="Developed by Ladybug",
#                                                 font=customtkinter.CTkFont(size=15), text_color=("black", "white"))
#     developed_by_label.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
#
#     return home_frame
#
# def create_frame(root, name):
#     frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
#     frame.grid_columnconfigure(0, weight=1)
#     label = customtkinter.CTkLabel(frame, text=name, text_color=("black", "white"))
#     label.grid(row=0, column=0, padx=20, pady=10)
#
#     if name == "Sort":
#         create_sort_section(frame)
#     elif name == "Reformat":
#         create_reformat_section(frame)
#     elif name == "Split Data":
#         create_split_data_frame(frame)
#
#     return frame
#
# def create_sort_section(frame):
#     input_file_var = customtkinter.StringVar()
#     sample_file_var = customtkinter.StringVar()
#     output_folder_var = customtkinter.StringVar()
#
#     def select_input_file():
#         file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
#         if file_path:
#             input_file_var.set(file_path)
#             input_file_label.configure(text=f"Selected file: {os.path.basename(file_path)}")
#
#     def select_sample_file():
#         file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
#         if file_path:
#             sample_file_var.set(file_path)
#             sample_file_label.configure(text=f"Selected file: {os.path.basename(file_path)}")
#
#     def select_output_folder():
#         folder_path = filedialog.askdirectory()
#         if folder_path:
#             output_folder_var.set(folder_path)
#             output_folder_label.configure(text=f"Selected folder: {os.path.basename(folder_path)}")
#
#     def process_data():
#         raw_data_path = input_file_var.get()
#         sample_data_path = sample_file_var.get()
#         output_folder = output_folder_var.get()
#
#         if not raw_data_path or not sample_data_path or not output_folder:
#             messagebox.showerror("Error", "Please select all the required files and folder.")
#             return
#
#         output_path = os.path.join(output_folder, "Processed_Data.xlsx")
#
#         try:
#             automate_data_processing(raw_data_path, sample_data_path, output_path)
#             messagebox.showinfo("Success", f"Data has been processed and saved to {output_path}")
#         except Exception as e:
#             messagebox.showerror("Error", f"An error occurred: {e}")
#
#     customtkinter.CTkLabel(frame, text="Select input Excel file:").grid(row=1, column=0, padx=20, pady=(20, 5), sticky="ew")
#     input_file_button = customtkinter.CTkButton(frame, text="Browse...", command=select_input_file, width=100)
#     input_file_button.grid(row=2, column=0, padx=20, pady=5, sticky="w")
#     input_file_label = customtkinter.CTkLabel(frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
#     input_file_label.grid(row=2, column=1, padx=20, pady=5, sticky="w")
#
#     customtkinter.CTkLabel(frame, text="Select sample Excel file:").grid(row=3, column=0, padx=20, pady=(20, 5), sticky="ew")
#     sample_file_button = customtkinter.CTkButton(frame, text="Browse...", command=select_sample_file, width=100)
#     sample_file_button.grid(row=4, column=0, padx=20, pady=5, sticky="w")
#     sample_file_label = customtkinter.CTkLabel(frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
#     sample_file_label.grid(row=4, column=1, padx=20, pady=5, sticky="w")
#
#     customtkinter.CTkLabel(frame, text="Select output folder:").grid(row=5, column=0, padx=20, pady=(20, 5), sticky="ew")
#     output_folder_button = customtkinter.CTkButton(frame, text="Browse...", command=select_output_folder, width=100)
#     output_folder_button.grid(row=6, column=0, padx=20, pady=5, sticky="w")
#     output_folder_label = customtkinter.CTkLabel(frame, text="No folder selected", text_color=("gray50", "gray50"), wraplength=400)
#     output_folder_label.grid(row=6, column=1, padx=20, pady=5, sticky="w")
#
#     process_button = customtkinter.CTkButton(frame, text="Process Data", command=process_data, width=150)
#     process_button.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky="sew")
#
# def create_reformat_section(frame):
#     input_file_var = customtkinter.StringVar()
#     output_folder_var = customtkinter.StringVar()
#
#     def select_input_file():
#         file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
#         if file_path:
#             input_file_var.set(file_path)
#             input_file_label.configure(text=f"Selected file: {os.path.basename(file_path)}")
#
#     def select_output_folder():
#         folder_path = filedialog.askdirectory()
#         if folder_path:
#             output_folder_var.set(folder_path)
#             output_folder_label.configure(text=f"Selected folder: {os.path.basename(folder_path)}")
#
#     def process_data():
#         raw_data_path = input_file_var.get()
#         output_folder = output_folder_var.get()
#
#         if not raw_data_path or not output_folder:
#             messagebox.showerror("Error", "Please select all the required files and folder.")
#             return
#
#         output_path = os.path.join(output_folder, "Reformatted_Data.xlsx")
#
#         try:
#             reformat_and_split_excel(raw_data_path, output_path, level_params)
#             messagebox.showinfo("Success", f"Data has been reformatted and saved to {output_path}")
#         except Exception as e:
#             messagebox.showerror("Error", f"An error occurred: {e}")
#
#     customtkinter.CTkLabel(frame, text="Select input Excel file:").grid(row=1, column=0, padx=20, pady=(20, 5), sticky="ew")
#     input_file_button = customtkinter.CTkButton(frame, text="Browse...", command=select_input_file, width=100)
#     input_file_button.grid(row=2, column=0, padx=20, pady=5, sticky="w")
#     input_file_label = customtkinter.CTkLabel(frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
#     input_file_label.grid(row=2, column=1, padx=20, pady=5, sticky="w")
#
#     customtkinter.CTkLabel(frame, text="Select output folder:").grid(row=3, column=0, padx=20, pady=(20, 5), sticky="ew")
#     output_folder_button = customtkinter.CTkButton(frame, text="Browse...", command=select_output_folder, width=100)
#     output_folder_button.grid(row=4, column=0, padx=20, pady=5, sticky="w")
#     output_folder_label = customtkinter.CTkLabel(frame, text="No folder selected", text_color=("gray50", "gray50"), wraplength=400)
#     output_folder_label.grid(row=4, column=1, padx=20, pady=5, sticky="w")
#
#     process_button = customtkinter.CTkButton(frame, text="Reformat Data", command=process_data, width=150)
#     process_button.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="sew")
#
# def create_split_data_frame(root):
#     split_data_frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
#     split_data_frame.grid_columnconfigure(0, weight=1)
#     split_data_frame.grid_rowconfigure(8, weight=1)
#
#     input_file_var = customtkinter.StringVar()
#     output_folder_var = customtkinter.StringVar()
#     category_vars = {}
#
#     def select_input_file():
#         file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
#         if file_path:
#             input_file_var.set(file_path)
#             input_file_label.configure(text=f"Selected file: {os.path.basename(file_path)}")
#
#     def select_output_path():
#         folder_path = filedialog.askdirectory()
#         if folder_path:
#             output_folder_var.set(folder_path)
#             output_folder_label.configure(text=f"Selected folder: {os.path.basename(folder_path)}")
#
#     def scan_and_create():
#         nonlocal category_vars
#         category_vars = scan_and_create_checkboxes(split_data_frame, input_file_var, categories_frame)
#
#     customtkinter.CTkLabel(split_data_frame, text="Select input Excel file:").grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")
#     input_file_button = customtkinter.CTkButton(split_data_frame, text="Browse...", command=select_input_file, width=100)
#     input_file_button.grid(row=1, column=0, padx=20, pady=5, sticky="w")
#     input_file_label = customtkinter.CTkLabel(split_data_frame, text="No file selected", text_color=("gray50", "gray50"), wraplength=400)
#     input_file_label.grid(row=1, column=1, padx=20, pady=5, sticky="w")
#
#     customtkinter.CTkLabel(split_data_frame, text="Select output folder:").grid(row=2, column=0, padx=20, pady=(20, 5), sticky="ew")
#     output_folder_button = customtkinter.CTkButton(split_data_frame, text="Browse...", command=select_output_path, width=100)
#     output_folder_button.grid(row=3, column=0, padx=20, pady=5, sticky="w")
#     output_folder_label = customtkinter.CTkLabel(split_data_frame, text="No folder selected", text_color=("gray50", "gray50"), wraplength=400)
#     output_folder_label.grid(row=3, column=1, padx=20, pady=5, sticky="w")
#
#     categories_frame = customtkinter.CTkScrollableFrame(split_data_frame)
#     categories_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
#
#     scan_button = customtkinter.CTkButton(split_data_frame, text="Scan and Create Checkboxes", command=scan_and_create, width=150)
#     scan_button.grid(row=5, column=0, columnspan=2, padx=20, pady=20, sticky="sew")
#
#     sort_button = customtkinter.CTkButton(split_data_frame, text="Sort Selected Categories",
#                                           command=lambda: sort_selected_categories(input_file_var.get(), output_folder_var.get(), category_vars), width=150)
#     sort_button.grid(row=6, column=0, columnspan=2, padx=20, pady=20, sticky="sew")
#
#     return split_data_frame
#
# def scan_and_create_checkboxes(split_data_frame, input_file_var, categories_frame):
#     input_file = input_file_var.get()
#     if not input_file:
#         messagebox.showerror("Error", "Please select an input file first")
#         return
#
#     try:
#         data = pd.read_excel(input_file)
#         categories = data['Category'].unique()
#
#         for widget in categories_frame.winfo_children():
#             widget.destroy()
#
#         category_vars = {}
#         row, col = 0, 0
#         for category in categories:
#             var = customtkinter.StringVar(value="0")
#             checkbox = customtkinter.CTkCheckBox(categories_frame, text=category, variable=var)
#             checkbox.grid(row=row, column=col, padx=10, pady=5, sticky="w")
#             category_vars[category] = var
#
#             col += 1
#             if col == 2:
#                 col = 0
#                 row += 1
#
#         return category_vars
#
#     except Exception as e:
#         messagebox.showerror("Error", f"An error occurred while scanning the file: {e}")
#
# def sort_selected_categories(input_file, output_folder, category_vars):
#     if not input_file or not output_folder:
#         messagebox.showerror("Error", "Please select both input file and output folder")
#         return
#
#     try:
#         sorted_output_path = os.path.join(output_folder, "Sorted_Data.xlsx")
#         cleaned_output_path = os.path.join(output_folder, "Cleaned_Sorted_Data.xlsx")
#
#         data = pd.read_excel(input_file)
#         selected_categories = [category for category, var in category_vars.items() if var.get() == "1"]
#         category_data = {category: data[data['Category'].str.contains(category, case=False, na=False)] for category in selected_categories}
#
#         with pd.ExcelWriter(sorted_output_path, engine='xlsxwriter') as writer:
#             for category, df in category_data.items():
#                 df.to_excel(writer, sheet_name=category, index=False)
#
#         sorted_excel_data = pd.ExcelFile(sorted_output_path)
#         cleaned_data = {}
#         for sheet_name in sorted_excel_data.sheet_names:
#             df = pd.read_excel(sorted_output_path, sheet_name=sheet_name)
#             cleaned_df = df.dropna(axis=1, how='all')
#             cleaned_data[sheet_name] = cleaned_df
#
#         with pd.ExcelWriter(cleaned_output_path, engine='xlsxwriter') as writer:
#             for sheet_name, df in cleaned_data.items():
#                 df.to_excel(writer, sheet_name=sheet_name, index=False)
#
#         messagebox.showinfo("Success", f"Sorted data has been saved to {sorted_output_path}\nCleaned data has been saved to {cleaned_output_path}")
#
#     except Exception as e:
#         messagebox.showerror("Error", f"An error occurred: {e}")
#
# def select_frame(frame_name, frames, buttons):
#     for frame in frames.values():
#         frame.grid_forget()
#     frames[frame_name].grid(row=0, column=1, sticky="nsew")
#     for button_name, button in buttons.items():
#         button.configure(fg_color=("gray75", "gray25") if button_name == frame_name else "transparent")
#
# def toggle_theme(frames, theme_toggle_switch):
#     current_mode = customtkinter.get_appearance_mode()
#     new_mode = "Dark" if current_mode == "Light" else "Light"
#     customtkinter.set_appearance_mode(new_mode)
#
#     new_bg_color = get_current_fg_color()
#     for frame in frames.values():
#         frame.configure(fg_color=new_bg_color)
#
#     theme_toggle_switch.select() if new_mode == "Dark" else theme_toggle_switch.deselect()
#
# # Main
# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Cost Predictor and Smart Decision App")
#     root.geometry("900x650")
#     root.resizable(False, False)
#
#     root.grid_columnconfigure(0, weight=0)
#     root.grid_columnconfigure(1, weight=1)
#     root.grid_rowconfigure(0, weight=1)
#
#     logo_image = setup_images()
#
#     frames = {
#         "home": create_home_frame(root),
#         "sort": create_frame(root, "Sort"),
#         "split_data": create_split_data_frame(root),
#         "reformat": create_frame(root, "Reformat")
#     }
#
#     home_button, sort_button, split_data_button, reformat_button, theme_toggle_switch = create_navigation_frame(
#         root, logo_image, lambda: toggle_theme(frames, theme_toggle_switch), lambda name: select_frame(name, frames, buttons)
#     )
#
#     buttons = {
#         "home": home_button,
#         "sort": sort_button,
#         "split_data": split_data_button,
#         "reformat": reformat_button
#     }
#
#     select_frame("home", frames, buttons)
#
#     current_mode = customtkinter.get_appearance_mode()
#     theme_toggle_switch.select() if current_mode == "Dark" else theme_toggle_switch.deselect()
#
#     root.mainloop()
