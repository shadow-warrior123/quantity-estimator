import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os


def clean_level_name(level_name):
    if isinstance(level_name, str):
        # Check if the level name contains "Level :" and remove it
        if "Level :" in level_name:
            return level_name.split("Level :")[1].strip()
        return level_name
    return level_name


def merge_and_format_excel_files(material_takeoff_path, other_data_extraction_path, output_folder):
    try:
        # Load the Excel files
        material_takeoff_df = pd.read_excel(material_takeoff_path)
        other_data_extraction_df = pd.read_excel(other_data_extraction_path)

        # Clean the 'Level' column in both DataFrames
        if 'Level' in material_takeoff_df.columns:
            material_takeoff_df['Level'] = material_takeoff_df['Level'].apply(clean_level_name)
        if 'Level' in other_data_extraction_df.columns:
            other_data_extraction_df['Level'] = other_data_extraction_df['Level'].apply(clean_level_name)

        # Merge the DataFrames on 'Element ID'
        merged_df = pd.merge(other_data_extraction_df, material_takeoff_df, on='Element ID', how='left')

        # Get unique material names
        unique_materials = merged_df['Material Name'].unique()

        # Create a dictionary to store the new columns for area and volume
        new_columns = {f'{material} Area': [] for material in unique_materials}
        new_columns.update({f'{material} Volume': [] for material in unique_materials})

        # Iterate through each element and populate the new columns
        for element_id in merged_df['Element ID'].unique():
            element_data = merged_df[merged_df['Element ID'] == element_id]
            for material in unique_materials:
                material_data = element_data[element_data['Material Name'] == material]
                new_columns[f'{material} Area'].append(
                    material_data['Material Area (m2)'].values[0] if not material_data.empty else None)
                new_columns[f'{material} Volume'].append(
                    material_data['Material Volume (m3)'].values[0] if not material_data.empty else None)

        # Create the final DataFrame
        final_df = other_data_extraction_df.copy()
        for column, values in new_columns.items():
            final_df[column] = values

        # Save the DataFrame to an Excel file
        output_path = os.path.join(output_folder, 'Final_Merged_Sorted_Excel_Sheet_with_Level.xlsx')

        # Check if file exists and remove it if necessary
        if os.path.exists(output_path):
            os.remove(output_path)

        final_df.to_excel(output_path, index=False)

        # Open the new Excel file
        os.system(f'start excel "{output_path}"')

        print(f"Excel file successfully saved at {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def select_files_and_merge():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    material_takeoff_path = filedialog.askopenfilename(title="Select Material Takeoff Excel File",
                                                       filetypes=[("Excel files", "*.xlsx")])
    if not material_takeoff_path:
        return

    other_data_extraction_path = filedialog.askopenfilename(title="Select Other Data Extraction Excel File",
                                                            filetypes=[("Excel files", "*.xlsx")])
    if not other_data_extraction_path:
        return

    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return

    merge_and_format_excel_files(material_takeoff_path, other_data_extraction_path, output_folder)


if __name__ == "__main__":
    select_files_and_merge()
