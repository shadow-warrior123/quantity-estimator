import pandas as pd
import openpyxl
from openpyxl.styles import Font, Border, Side, PatternFill


def find_level_column(df, params):
    for param in params:
        if param in df.columns:
            return param
    return None


def reformat_excel(input_file_path, output_file_path, level_params):
    workbook = pd.ExcelFile(input_file_path)
    sheets_data = []

    for sheet_name in workbook.sheet_names:
        df = pd.read_excel(workbook, sheet_name=sheet_name, header=0)
        sheets_data.append((sheet_name, df))

    reformatted_data = pd.DataFrame()
    reformatted_data = pd.concat([reformatted_data, pd.DataFrame([[pd.NA] * len(sheets_data[0][1].columns)] * 5)],
                                 ignore_index=True)

    for sheet_name, df in sheets_data:
        level_col = find_level_column(df, level_params)
        if level_col is not None:
            grouped = df.groupby(level_col)
            for level, group in grouped:
                level_info = pd.DataFrame([[f"{level_col}: {level}"] + [pd.NA] * (len(df.columns) - 1)],
                                          columns=df.columns)
                reformatted_data = pd.concat([reformatted_data, level_info], ignore_index=True)

                name_df = pd.DataFrame([[sheet_name]] + [[pd.NA] * len(df.columns)], columns=df.columns)
                reformatted_data = pd.concat([reformatted_data, name_df], ignore_index=True)

                reformatted_data = pd.concat([reformatted_data, pd.DataFrame([df.columns], columns=df.columns)],
                                             ignore_index=True)
                reformatted_data = pd.concat([reformatted_data, group], ignore_index=True)
                reformatted_data = pd.concat([reformatted_data, pd.DataFrame([[pd.NA] * len(df.columns)] * 5)],
                                             ignore_index=True)
        else:
            name_df = pd.DataFrame([[sheet_name]] + [[pd.NA] * len(df.columns)], columns=df.columns)
            reformatted_data = pd.concat([reformatted_data, name_df], ignore_index=True)
            reformatted_data = pd.concat([reformatted_data, pd.DataFrame([df.columns], columns=df.columns)],
                                         ignore_index=True)
            reformatted_data = pd.concat([reformatted_data, df], ignore_index=True)
            reformatted_data = pd.concat([reformatted_data, pd.DataFrame([[pd.NA] * len(df.columns)] * 5)],
                                         ignore_index=True)

    reformatted_data.to_excel(output_file_path, index=False, header=False)
    print(f"Reformatted data saved to: {output_file_path}")


level_params = ['Level', 'Base Level', 'Base Constraint', 'Work plane']
