import customtkinter

def get_user_inputs():
    inputs = {}

    def submit():
        inputs['grade'] = grade_var.get()
        inputs['concrete_type'] = concrete_type_var.get()
        inputs['exposure_condition'] = exposure_condition_var.get()
        inputs['cement_type'] = cement_type_var.get()
        inputs['coarse_aggregate_size'] = int(coarse_aggregate_size_var.get())
        inputs['target_slump'] = int(target_slump_var.get())
        inputs['admixture_used'] = admixture_used_var.get().lower() == 'yes'
        inputs['fine_aggregate_zone'] = fine_aggregate_zone_var.get()
        inputs['pump_required'] = pump_required_var.get().lower() == 'yes'
        inputs['admixture_dosage'] = float(admixture_dosage_var.get())
        inputs['specific_gravity_cement'] = float(specific_gravity_cement_var.get())
        inputs['specific_gravity_water'] = 1  # Specific gravity of water is generally 1
        inputs['specific_gravity_admixture'] = float(specific_gravity_admixture_var.get())
        inputs['specific_gravity_coarse_aggregate'] = float(specific_gravity_coarse_aggregate_var.get())
        inputs['specific_gravity_fine_aggregate'] = float(specific_gravity_fine_aggregate_var.get())
        window.quit()
        window.destroy()

    window = customtkinter.CTk()
    window.title("Concrete Mix Design Inputs")
    window.geometry("400x600")

    grade_var = customtkinter.StringVar()
    concrete_type_var = customtkinter.StringVar()
    exposure_condition_var = customtkinter.StringVar()
    cement_type_var = customtkinter.StringVar()
    coarse_aggregate_size_var = customtkinter.StringVar()
    target_slump_var = customtkinter.StringVar()
    admixture_used_var = customtkinter.StringVar()
    fine_aggregate_zone_var = customtkinter.StringVar()
    pump_required_var = customtkinter.StringVar()
    admixture_dosage_var = customtkinter.StringVar()
    specific_gravity_cement_var = customtkinter.StringVar()
    specific_gravity_admixture_var = customtkinter.StringVar()
    specific_gravity_coarse_aggregate_var = customtkinter.StringVar()
    specific_gravity_fine_aggregate_var = customtkinter.StringVar()

    customtkinter.CTkLabel(window, text="Enter the grade of concrete (e.g., 'M20')").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=grade_var).pack()

    customtkinter.CTkLabel(window, text="Enter the type of concrete (PCC for Plain, RCC for Reinforced)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=concrete_type_var).pack()

    customtkinter.CTkLabel(window, text="Enter the exposure condition (Mild, Moderate, Severe, Very Severe, Extreme)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=exposure_condition_var).pack()

    customtkinter.CTkLabel(window, text="Enter the type of cement (OPC 33, OPC 43, OPC 53, PPC, PSC)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=cement_type_var).pack()

    customtkinter.CTkLabel(window, text="Enter the size of the coarse aggregate (10, 20, or 40 mm)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=coarse_aggregate_size_var).pack()

    customtkinter.CTkLabel(window, text="Enter the target slump value (in mm)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=target_slump_var).pack()

    customtkinter.CTkLabel(window, text="Is an admixture used? (yes/no)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=admixture_used_var).pack()

    customtkinter.CTkLabel(window, text="Enter the zone of the fine aggregate (Zone I, Zone II, Zone III, Zone IV)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=fine_aggregate_zone_var).pack()

    customtkinter.CTkLabel(window, text="Is concrete pumping required? (yes/no)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=pump_required_var).pack()

    customtkinter.CTkLabel(window, text="Enter the admixture dosage as a percentage of cement content (e.g., 1.2)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=admixture_dosage_var).pack()

    customtkinter.CTkLabel(window, text="Enter the specific gravity of cement (e.g., 3.15)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=specific_gravity_cement_var).pack()

    customtkinter.CTkLabel(window, text="Enter the specific gravity of admixture (e.g., 1.2)").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=specific_gravity_admixture_var).pack()

    customtkinter.CTkLabel(window, text="Enter the specific gravity of coarse aggregate").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=specific_gravity_coarse_aggregate_var).pack()

    customtkinter.CTkLabel(window, text="Enter the specific gravity of fine aggregate").pack(pady=5)
    customtkinter.CTkEntry(window, textvariable=specific_gravity_fine_aggregate_var).pack()

    customtkinter.CTkButton(window, text="Submit", command=submit).pack(pady=20)

    window.mainloop()

    return (
        inputs['grade'], inputs['concrete_type'], inputs['exposure_condition'],
        inputs['cement_type'], inputs['coarse_aggregate_size'], inputs['target_slump'],
        inputs['admixture_used'], inputs['fine_aggregate_zone'], inputs['pump_required'],
        inputs['admixture_dosage'], inputs['specific_gravity_cement'], inputs['specific_gravity_water'],
        inputs['specific_gravity_admixture'], inputs['specific_gravity_coarse_aggregate'],
        inputs['specific_gravity_fine_aggregate']
    )
