import matplotlib.pyplot as plt
from .data_storage import (
    standard_deviation_values, factor_values, exposure_conditions_plain,
    exposure_conditions_reinforced, chart_w_c_ratio_opc_33, chart_w_c_ratio_opc_43,
    chart_w_c_ratio_opc_53, chart_w_c_ratio_ppc, chart_w_c_ratio_psc,
    water_content_table, cement_content_table, coarse_aggregate_table,
    entrapped_air_table
)


def calculate_target_mean_strength(f_ck, grade):
    S = standard_deviation_values.get(grade, 0)
    X = factor_values.get(grade, 0)
    f_ck1 = f_ck + 1.65 * S
    f_ck2 = f_ck + X
    return max(f_ck1, f_ck2)


def get_max_w_c_ratio(exposure_condition, concrete_type):
    if concrete_type.lower() == 'pcc':
        return exposure_conditions_plain.get(exposure_condition, "Unknown exposure condition")
    elif concrete_type.lower() == 'rcc':
        return exposure_conditions_reinforced.get(exposure_condition, "Unknown exposure condition")
    else:
        return "Unknown concrete type"


def get_w_c_ratio_from_chart(compressive_strength, cement_type):
    if cement_type == 'OPC 33':
        chart_w_c_ratio = chart_w_c_ratio_opc_33
    elif cement_type == 'OPC 43':
        chart_w_c_ratio = chart_w_c_ratio_opc_43
    elif cement_type == 'OPC 53':
        chart_w_c_ratio = chart_w_c_ratio_opc_53
    elif cement_type == 'PPC':
        chart_w_c_ratio = chart_w_c_ratio_ppc
    elif cement_type == 'PSC':
        chart_w_c_ratio = chart_w_c_ratio_psc
    else:
        return "Unknown cement type"

    if compressive_strength in chart_w_c_ratio:
        return chart_w_c_ratio[compressive_strength]

    strengths = sorted(chart_w_c_ratio.keys())
    for i in range(len(strengths) - 1):
        if strengths[i] < compressive_strength < strengths[i + 1]:
            ratio1 = chart_w_c_ratio[strengths[i]]
            ratio2 = chart_w_c_ratio[strengths[i + 1]]
            interpolated_ratio = ratio1 + (ratio2 - ratio1) * (compressive_strength - strengths[i]) / (
                        strengths[i + 1] - strengths[i])
            return interpolated_ratio

    return "Compressive strength out of range"


def get_water_content(coarse_aggregate_size):
    if coarse_aggregate_size in water_content_table:
        return water_content_table[coarse_aggregate_size]
    else:
        raise ValueError("Coarse aggregate size not found in Table 4")


def adjust_water_content_for_slump(water_content, target_slump, actual_slump=50):
    slump_difference = target_slump - actual_slump
    percentage_increase = (slump_difference / 25) * 3
    adjusted_water_content = water_content + (water_content * percentage_increase / 100)
    return adjusted_water_content


def adjust_water_content_for_admixture(water_content, admixture_used):
    if admixture_used:
        return water_content * 0.75  # Reduce by 25% if admixture is used
    else:
        return water_content


def calculate_cement_content(water_content, w_c_ratio, exposure_condition, concrete_type):
    min_cement_content = cement_content_table[exposure_condition][concrete_type]['min']
    max_cement_content = cement_content_table[exposure_condition][concrete_type]['max']

    cement_content = water_content / w_c_ratio
    if cement_content < min_cement_content:
        cement_content = min_cement_content
    elif cement_content > max_cement_content:
        cement_content = max_cement_content

    return cement_content, min_cement_content, max_cement_content


def adjust_aggregate_proportions(coarse_aggregate_size, fine_aggregate_zone, w_c_ratio, pump_required):
    initial_coarse_aggregate_ratio = coarse_aggregate_table[coarse_aggregate_size][fine_aggregate_zone]

    w_c_difference = 0.50 - w_c_ratio
    adjustment_factor = (w_c_difference / 0.05) * 0.01

    coarse_aggregate_ratio = initial_coarse_aggregate_ratio + adjustment_factor

    if pump_required:
        coarse_aggregate_ratio *= 0.90  # Decrease by 10% for pumping

    return coarse_aggregate_ratio


def plot_w_c_ratio_chart(cement_type):
    if cement_type == 'OPC 33':
        chart_w_c_ratio = chart_w_c_ratio_opc_33
    elif cement_type == 'OPC 43':
        chart_w_c_ratio = chart_w_c_ratio_opc_43
    elif cement_type == 'OPC 53':
        chart_w_c_ratio = chart_w_c_ratio_opc_53
    elif cement_type == 'PPC':
        chart_w_c_ratio = chart_w_c_ratio_ppc
    elif cement_type == 'PSC':
        chart_w_c_ratio = chart_w_c_ratio_psc
    else:
        return "Unknown cement type"

    strengths = list(chart_w_c_ratio.keys())
    ratios = list(chart_w_c_ratio.values())

    plt.figure(figsize=(10, 6))
    plt.plot(strengths, ratios, marker='o')
    plt.title(f"W/C Ratio vs 28-Day Compressive Strength for {cement_type}")
    plt.xlabel("28-Day Compressive Strength (N/mm^2)")
    plt.ylabel("Water-Cement Ratio")
    plt.grid(True)


def calculate_volume_of_entrapped_air(coarse_aggregate_size):
    return entrapped_air_table.get(coarse_aggregate_size, 0) / 100


def design_mix_calculation(cement_content, water_content, admixture_dosage, specific_gravity_cement,
                           specific_gravity_water, specific_gravity_admixture, coarse_aggregate_size):
    volume_of_cementious_content = (cement_content / (specific_gravity_cement * 1000))
    volume_of_water = (water_content / (specific_gravity_water * 1000))
    volume_of_entrapped_air = (entrapped_air_table[coarse_aggregate_size] / 100)  # Convert percentage to decimal
    volume_of_admixture = ((admixture_dosage / 100) * cement_content) / (specific_gravity_admixture * 1000)

    volume_of_aggregate = 1 - (
                volume_of_admixture + volume_of_cementious_content + volume_of_water + volume_of_entrapped_air)

    return {
        'volume of cement': volume_of_cementious_content,
        'volume of water': volume_of_water,
        'volume of entrapped air': volume_of_entrapped_air,
        'volume of admixture': volume_of_admixture,
        'volume of aggregate': volume_of_aggregate
    }


def calculation_weight_material(cement_content, water_content, coarse_aggregate_ratio, volume_of_aggregate,
                                specific_gravity_coarse_aggregate, specific_gravity_fine_aggregate, volume_of_admixture,
                                specific_gravity_admixture):
    cement_weight = cement_content
    water_weight = water_content
    coarse_aggregate_weight = coarse_aggregate_ratio * volume_of_aggregate * specific_gravity_coarse_aggregate * 1000
    fine_aggregate_weight = ((
                                         1 - coarse_aggregate_ratio) * volume_of_aggregate * specific_gravity_fine_aggregate) * 1000
    admixture_weight = volume_of_admixture * specific_gravity_admixture * 1000

    return {
        'weight of cement used ': cement_weight,
        'weight of water used ': water_weight,
        'weight of gravel used ': coarse_aggregate_weight,
        'weight of sand used ': fine_aggregate_weight,
        'weight of admixture used ': admixture_weight
    }
