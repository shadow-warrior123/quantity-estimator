import customtkinter

def get_current_fg_color():
    current_mode = customtkinter.get_appearance_mode()
    return customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][0 if current_mode == "Light" else 1]

def toggle_theme(frames, theme_toggle_switch):
    current_mode = customtkinter.get_appearance_mode()
    new_mode = "Dark" if current_mode == "Light" else "Light"
    customtkinter.set_appearance_mode(new_mode)

    new_bg_color = get_current_fg_color()
    for frame in frames.values():
        frame.configure(fg_color=new_bg_color)

    theme_toggle_switch.select() if new_mode == "Dark" else theme_toggle_switch.deselect()

def select_frame(frame_name, frames, buttons):
    for frame in frames.values():
        frame.grid_forget()
    frames[frame_name].grid(row=0, column=1, sticky="nsew")
    for button_name, button in buttons.items():
        button.configure(fg_color=("gray75", "gray25") if button_name == frame_name else "transparent")
