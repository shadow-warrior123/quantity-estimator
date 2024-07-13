import customtkinter
from tkinter import messagebox
from concrete_mix_design.calculations import (
    calculate_target_mean_strength, get_max_w_c_ratio, get_w_c_ratio_from_chart,
    get_water_content, adjust_water_content_for_slump, adjust_water_content_for_admixture,
    calculate_cement_content, adjust_aggregate_proportions, plot_w_c_ratio_chart, design_mix_calculation,
    calculation_weight_material
)
from concrete_mix_design.data_storage import f_ck_values
from helpers import get_current_fg_color

def create_concrete_mix_frame(root):
    frame = customtkinter.CTkFrame(root, corner_radius=0, fg_color=get_current_fg_color())
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    def calculate_mix_design():
        try:
            grade = grade_var.get()
            concrete_type = concrete_type_var.get()
            exposure_condition = exposure_condition_var.get()
            cement_type = cement_type_var.get()
            coarse_aggregate_size = int(coarse_aggregate_size_var.get())
            target_slump = int(target_slump_var.get())
            admixture_used = admixture_used_var.get().lower() == 'yes'
            fine_aggregate_zone = fine_aggregate_zone_var.get()
            pump_required = pump_required_var.get().lower() == 'yes'
            admixture_dosage = float(admixture_dosage_var.get())
            specific_gravity_cement = float(specific_gravity_cement_var.get())
            specific_gravity_water = 1  # Specific gravity of water is generally 1
            specific_gravity_admixture = float(specific_gravity_admixture_var.get())
            specific_gravity_coarse_aggregate = float(specific_gravity_coarse_aggregate_var.get())
            specific_gravity_fine_aggregate = float(specific_gravity_fine_aggregate_var.get())

            f_ck = f_ck_values.get(grade, 0)

            if f_ck == 0:
                messagebox.showerror("Error", f"Invalid grade of concrete: {grade}")
                return

            target_mean_strength = calculate_target_mean_strength(f_ck, grade)
            max_w_c_ratio = get_max_w_c_ratio(exposure_condition, concrete_type)
            chart_w_c_ratio = get_w_c_ratio_from_chart(target_mean_strength, cement_type)

            if max_w_c_ratio == "Unknown exposure condition" or chart_w_c_ratio == "Compressive strength out of range" or max_w_c_ratio == "Unknown concrete type" or chart_w_c_ratio == "Unknown cement type":
                messagebox.showerror("Error", "Invalid input provided.")
                return

            final_w_c_ratio = min(max_w_c_ratio, chart_w_c_ratio)

            initial_water_content = get_water_content(coarse_aggregate_size)
            adjusted_water_content = adjust_water_content_for_slump(initial_water_content, target_slump)
            final_water_content = adjust_water_content_for_admixture(adjusted_water_content, admixture_used)

            cement_content, min_cement_content, max_cement_content = calculate_cement_content(final_water_content, final_w_c_ratio, exposure_condition, concrete_type)
            coarse_aggregate_ratio = adjust_aggregate_proportions(coarse_aggregate_size, fine_aggregate_zone, final_w_c_ratio, pump_required)
            fine_aggregate_ratio = 1 - coarse_aggregate_ratio

            plot_w_c_ratio_chart(cement_type)

            design_mix = design_mix_calculation(cement_content, final_water_content, admixture_dosage, specific_gravity_cement, specific_gravity_water, specific_gravity_admixture, coarse_aggregate_size)
            weight_of_material = calculation_weight_material(cement_content, final_water_content, coarse_aggregate_ratio, design_mix['volume of aggregate'], specific_gravity_coarse_aggregate, specific_gravity_fine_aggregate, design_mix['volume of admixture'], specific_gravity_admixture)

            result = (
                f"The target mean strength (f'ck) for grade {grade} is: {target_mean_strength:.2f} N/mm^2\n"
                f"The final water-cement ratio to be used is: {final_w_c_ratio}\n"
                f"The final water content to be used is: {final_water_content:.2f} kg/m³\n"
                f"The calculated cement content is: {cement_content:.2f} kg/m³\n"
                f"Minimum cement content for {exposure_condition} exposure condition and {concrete_type} is: {min_cement_content} kg/m³\n"
                f"Maximum cement content for {exposure_condition} exposure condition and {concrete_type} is: {max_cement_content} kg/m³\n"
                f"The adjusted coarse aggregate ratio is: {coarse_aggregate_ratio:.3f}\n"
                f"The adjusted fine aggregate ratio is: {fine_aggregate_ratio:.3f}\n\n"
                "Mix Design Volumes:\n" +
                "".join([f"{key}: {value:.5f} m³\n" for key, value in design_mix.items()]) + "\n"
                "Weight of different materials used:\n" +
                "".join([f"{key}: {value:.6f} kg\n" for key, value in weight_of_material.items()])
            )
            messagebox.showinfo("Mix Design Result", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    header_label = customtkinter.CTkLabel(frame, text="Concrete Mix Design", font=customtkinter.CTkFont(size=18, weight="bold"), text_color=("black", "white"))
    header_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

    # Input fields
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

    def create_input_row(label_text, variable, row):
        customtkinter.CTkLabel(frame, text=label_text, text_color=("black", "white")).grid(row=row, column=0, padx=20, pady=5, sticky="w")
        customtkinter.CTkEntry(frame, textvariable=variable).grid(row=row, column=1, padx=20, pady=5, sticky="ew")

    create_input_row("Enter the grade of concrete (e.g., 'M20'):", grade_var, 1)
    create_input_row("Enter the type of concrete (PCC for Plain, RCC for Reinforced):", concrete_type_var, 2)
    create_input_row("Enter the exposure condition (Mild, Moderate, Severe, Very Severe, Extreme):", exposure_condition_var, 3)
    create_input_row("Enter the type of cement (OPC 33, OPC 43, OPC 53, PPC, PSC):", cement_type_var, 4)
    create_input_row("Enter the size of the coarse aggregate (10, 20, or 40 mm):", coarse_aggregate_size_var, 5)
    create_input_row("Enter the target slump value (in mm):", target_slump_var, 6)
    create_input_row("Is an admixture used? (yes/no):", admixture_used_var, 7)
    create_input_row("Enter the zone of the fine aggregate (Zone I, Zone II, Zone III, Zone IV):", fine_aggregate_zone_var, 8)
    create_input_row("Is concrete pumping required? (yes/no):", pump_required_var, 9)
    create_input_row("Enter the admixture dosage as a percentage of cement content (e.g., 1.2):", admixture_dosage_var, 10)
    create_input_row("Enter the specific gravity of cement (e.g., 3.15):", specific_gravity_cement_var, 11)
    create_input_row("Enter the specific gravity of admixture (e.g., 1.2):", specific_gravity_admixture_var, 12)
    create_input_row("Enter the specific gravity of coarse aggregate:", specific_gravity_coarse_aggregate_var, 13)
    create_input_row("Enter the specific gravity of fine aggregate:", specific_gravity_fine_aggregate_var, 14)

    calculate_button = customtkinter.CTkButton(frame, text="Calculate Mix Design", command=calculate_mix_design, width=200)
    calculate_button.grid(row=15, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

    return frame
