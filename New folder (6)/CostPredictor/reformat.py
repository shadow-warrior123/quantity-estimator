import pandas as pd
import numpy as np


def find_level_column(df, params):
    for param in params:
        if param in df.columns:
            return param
    return None


def reformat_and_split_excel(input_file_path, output_file_path, level_params):
    workbook = pd.ExcelFile(input_file_path)
    sheets_data = []

    for sheet_name in workbook.sheet_names:
        df = pd.read_excel(workbook, sheet_name=sheet_name, header=0)
        sheets_data.append((sheet_name, df))

    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        for sheet_name, df in sheets_data:
            level_col = find_level_column(df, level_params)
            if level_col is not None:
                grouped = df.groupby(level_col)
                for level, group in grouped:
                    # Initialize an empty DataFrame for reformatted data
                    reformatted_data = pd.DataFrame()

                    # Add level information
                    level_info = pd.DataFrame([[f"{level_col}: {level}"] + [pd.NA] * (len(group.columns) - 1)],
                                              columns=group.columns)
                    reformatted_data = pd.concat([reformatted_data, level_info], ignore_index=True)

                    # Add sheet name with a 2-row gap
                    name_df = pd.DataFrame([[sheet_name] + [pd.NA] * (len(group.columns) - 1)], columns=group.columns)
                    reformatted_data = pd.concat([reformatted_data, name_df], ignore_index=True)

                    # Add headers for the subsection
                    reformatted_data = pd.concat(
                        [reformatted_data, pd.DataFrame([group.columns], columns=group.columns)], ignore_index=True)

                    # Concatenate the grouped data
                    reformatted_data = pd.concat([reformatted_data, group], ignore_index=True)

                    # Truncate sheet name to <= 31 characters
                    level_sheet_name = f"{sheet_name}_Level_{level}"[:31]
                    reformatted_data.to_excel(writer, sheet_name=level_sheet_name, index=False, header=False)
            else:
                # Initialize an empty DataFrame for reformatted data
                reformatted_data = pd.DataFrame()

                # Add sheet name
                name_df = pd.DataFrame([[sheet_name] + [pd.NA] * (len(df.columns) - 1)], columns=df.columns)
                reformatted_data = pd.concat([reformatted_data, name_df], ignore_index=True)

                # Add headers for the subsection
                reformatted_data = pd.concat([reformatted_data, pd.DataFrame([df.columns], columns=df.columns)],
                                             ignore_index=True)

                # Concatenate the entire data
                reformatted_data = pd.concat([reformatted_data, df], ignore_index=True)

                reformatted_data.to_excel(writer, sheet_name=sheet_name[:31], index=False, header=False)

    print(f"Reformatted and split data saved to: {output_file_path}")


level_params = ['Level', 'Base Level', 'Base Constraint', 'Work plane']
