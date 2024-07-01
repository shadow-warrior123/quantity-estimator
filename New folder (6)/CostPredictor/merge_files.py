import pandas as pd
import customtkinter
from tkinter import filedialog, messagebox


def merge_files(file1, file2, output_file):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    merged_df = pd.merge(df1, df2, on='common_column')
    merged_df.to_excel(output_file, index=False)
