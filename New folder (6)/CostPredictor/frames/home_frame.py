import customtkinter
from helpers import get_current_fg_color

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
