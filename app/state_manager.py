# app/state_manager.py

import pandas as pd

def save_dataframe(name: str, df: pd.DataFrame, session_state: dict):
    """
    Saves a DataFrame to Streamlit session state.
    """
    session_state[name] = df

def get_dataframe(name: str, session_state: dict) -> pd.DataFrame:
    """
    Retrieves a DataFrame from session state.
    """
    return session_state.get(name, pd.DataFrame())

def get_all_dataframes(session_state: dict) -> dict:
    """
    Returns all dataframes in session_state with names like df, df1, df2, etc.
    """
    return {
        name: df for name, df in session_state.items()
        if name.startswith("df") and isinstance(df, pd.DataFrame)
    }

def get_active_dataframe(session_state: dict) -> pd.DataFrame:
    """
    Returns the currently selected DataFrame to use as 'df'.
    Defaults to 'df' if none is selected.
    """
    selected_name = session_state.get("selected_df_name", "df")
    return session_state.get(selected_name, pd.DataFrame())
