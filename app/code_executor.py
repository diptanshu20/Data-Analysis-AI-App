# app/code_executor.py

import io
import matplotlib.pyplot as plt
import pandas as pd
import contextlib

from app.state_manager import get_active_dataframe, save_dataframe


def execute_user_code(code: str, session_state: dict) -> str:
    """
    Executes user-generated code and captures the output.
    Uses the currently selected DataFrame as 'df'.
    """
    active_df = get_active_dataframe(session_state)

    local_vars = {
        "df": active_df.copy(deep=True),
        "pd": pd,
        "plt": plt
    }

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {}, local_vars)

        # Save updated df if modified
        if "df" in local_vars and isinstance(local_vars["df"], pd.DataFrame):
            if not local_vars["df"].equals(active_df):
                save_dataframe("df", local_vars["df"], session_state)

        # Save any new DataFrames
        for var in local_vars:
            if var.startswith("df") and isinstance(local_vars[var], pd.DataFrame):
                save_dataframe(var, local_vars[var], session_state)

        # ✅ Save all figures (as a list) before closing
        figures = [plt.figure(num) for num in plt.get_fignums()]
        session_state["last_figures"] = figures

        plt.close("all")

        return "✅ Code executed successfully.\n\n" + stdout.getvalue()

    except Exception as e:
        return f"❌ Error during code execution:\n{str(e)}"
