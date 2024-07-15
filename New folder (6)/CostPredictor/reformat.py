import pandas as pd

def find_level_column(df, params):
    for param in params:
        if param in df.columns:
            return param
    return None

def sanitize_sheet_name(sheet_name):
    invalid_chars = '[]:*?/\''
    for char in invalid_chars:
        sheet_name = sheet_name.replace(char, "")
    return sheet_name[:31]  # Excel sheet names must be <= 31 characters

def combine_entries_by_floor(df, level_col):
    combined_df = df.groupby(level_col).apply(lambda x: x.drop(columns=[level_col]).reset_index(drop=True)).reset_index(level=0)
    return combined_df

def reformat_and_split_excel(input_file_path, output_file_path, level_params):
    workbook = pd.ExcelFile(input_file_path)
    all_data = pd.DataFrame()

    # Combine all sheets into one DataFrame
    for sheet_name in workbook.sheet_names:
        df = pd.read_excel(workbook, sheet_name=sheet_name, header=0)
        df['Sheet Name'] = sheet_name
        all_data = pd.concat([all_data, df], ignore_index=True)

    # Find the level column
    level_col = find_level_column(all_data, level_params)
    if not level_col:
        print("No level column found in any sheet.")
        return

    # Combine entries by floor
    combined_data = combine_entries_by_floor(all_data, level_col)

    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        for level, group in combined_data.groupby(level_col):
            sanitized_sheet_name = sanitize_sheet_name(f'{level}')
            group.to_excel(writer, sheet_name=sanitized_sheet_name, index=False)

    print(f"Reformatted data saved to: {output_file_path}")

level_params = ['Level', 'Base Level', 'Base Constraint', 'Work plane']
