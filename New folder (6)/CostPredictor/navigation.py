import customtkinter

def create_navigation_frame(root, logo_image, toggle_theme, select_frame):
    navigation_frame = customtkinter.CTkFrame(root, corner_radius=0, width=200, fg_color=("#D4D4D4","#323232"))
    navigation_frame.grid(row=0, column=0, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)

    navigation_frame_label = customtkinter.CTkLabel(navigation_frame, text="   Ladybug", image=logo_image,
                                                    compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
    navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

    home_button = create_nav_button(navigation_frame, "Home", lambda: select_frame("home"))
    reformat_button = create_nav_button(navigation_frame, "Reformat", lambda: select_frame("reformat"))
    split_data_button = create_nav_button(navigation_frame, "Split Data", lambda: select_frame("split_data"))
    unit_prices_button = create_nav_button(navigation_frame, "Unit Prices", lambda: select_frame("unit_prices"))
    excel_processing_button = create_nav_button(navigation_frame, "Excel Processing", lambda: select_frame("excel_processing"))

    home_button.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
    reformat_button.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
    split_data_button.grid(row=3, column=0, sticky="ew", padx=20, pady=5)
    unit_prices_button.grid(row=4, column=0, sticky="ew", padx=20, pady=5)
    excel_processing_button.grid(row=5, column=0, sticky="ew", padx=20, pady=5)

    navigation_frame.grid_rowconfigure(97, weight=1)

    def quit_app():
        root.quit()

    quit_button = customtkinter.CTkButton(navigation_frame, text="Quit", command=quit_app, fg_color="#BA0B13", hover_color="#94070D")
    quit_button.grid(row=99, column=0, padx=20, pady=(10,30), sticky="ew")

    theme_toggle_switch = customtkinter.CTkSwitch(navigation_frame, text="Dark Mode", command=toggle_theme)
    theme_toggle_switch.grid(row=98, column=0, padx=20, pady=10, sticky="sew")

    return home_button, reformat_button, split_data_button, unit_prices_button, excel_processing_button, theme_toggle_switch

def create_nav_button(parent, text, command):
    button = customtkinter.CTkButton(parent, corner_radius=6, height=40, border_spacing=10, text=text,
                                     fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=command)
    button.grid(sticky="ew")
    return button
