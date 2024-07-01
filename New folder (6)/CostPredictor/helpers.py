import customtkinter

def get_current_fg_color():
    current_mode = customtkinter.get_appearance_mode()
    return customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][0 if current_mode == "Light" else 1]