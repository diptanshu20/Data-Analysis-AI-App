# app/uploader.py


import pandas as pd

def load_file(file):
    """
    Loads a CSV or Excel file and returns it as a pandas DataFrame.

    Args:
        file: Streamlit-uploaded file object

    Returns:
        pd.DataFrame

    Raises:
        ValueError: If the file type is unsupported or if loading fails
    """
    filename = file.name.lower()

    try:
        if filename.endswith(".csv"):
            try:
                # Try default utf-8 first
                return pd.read_csv(file)
            except UnicodeDecodeError:
                # Fallback to Latin1 (ISO-8859-1)
                file.seek(0)  # Reset file pointer
                return pd.read_csv(file, encoding="ISO-8859-1")
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            return pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    except Exception as e:
        raise ValueError(f"Failed to load the file: {e}")

