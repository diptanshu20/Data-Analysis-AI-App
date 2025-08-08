# utils/file_utils.py


import pandas as pd

def read_file(file) -> pd.DataFrame:
    """
    Reads a CSV or Excel file and returns a DataFrame.
    """
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith((".xls", ".xlsx")):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

def get_file_extension(file_name: str) -> str:
    """
    Returns the extension of the file (e.g., csv, xlsx).
    """
    return file_name.split(".")[-1].lower()