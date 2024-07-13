import tkinter as tk
import customtkinter
from images import setup_images
from navigation import create_navigation_frame
from frames.home_frame import create_home_frame
from frames.reformat_frame import create_reformat_frame
from frames.split_data_frame import create_split_data_frame
from frames.unit_prices_frame import create_unit_prices_frame
from frames.concrete_mix_frame import create_concrete_mix_frame
from frames.excel_processing_frame import create_excel_processing_frame
from helpers import toggle_theme, select_frame

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cost Predictor and Smart Decision App")
    root.geometry("900x650")
    root.resizable(False, False)

    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    logo_image = setup_images()

    frames = {
        "home": create_home_frame(root),
        "reformat": create_reformat_frame(root),
        "split_data": create_split_data_frame(root),
        "unit_prices": create_unit_prices_frame(root),
        "concrete_mix": create_concrete_mix_frame(root),
        "excel_processing": create_excel_processing_frame(root)
    }

    home_button, reformat_button, split_data_button, unit_prices_button, concrete_mix_button, excel_processing_button, theme_toggle_switch = create_navigation_frame(
        root, logo_image, lambda: toggle_theme(frames, theme_toggle_switch), lambda name: select_frame(name, frames, buttons)
    )

    buttons = {
        "home": home_button,
        "reformat": reformat_button,
        "split_data": split_data_button,
        "unit_prices": unit_prices_button,
        "concrete_mix": concrete_mix_button,
        "excel_processing": excel_processing_button
    }

    select_frame("home", frames, buttons)

    current_mode = customtkinter.get_appearance_mode()
    theme_toggle_switch.select() if current_mode == "Dark" else theme_toggle_switch.deselect()

    root.mainloop()
