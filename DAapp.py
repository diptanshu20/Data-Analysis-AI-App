# DAapp.py

import streamlit as st
import pandas as pd
import re

from app.uploader import load_file
from app.state_manager import save_dataframe, get_all_dataframes
from app.gemini_api import get_code_from_query
from app.code_executor import execute_user_code
from utils.plot_utils import render_all_matplotlib_plots

# --- Page config ---
st.set_page_config(page_title="Gemini Data Analyst", layout="wide")
st.title("📊 Gemini-Powered Data Analysis")

# --- Layout ---
left, right = st.columns([1, 2])

# --- LEFT PANEL: Upload + Prompt ---
with left:
    st.header("🤖 Chat with Gemini")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])

    if uploaded_file:
        try:
            df = load_file(uploaded_file)
            save_dataframe("df", df, st.session_state)
            save_dataframe("df_original", df.copy(deep=True), st.session_state)
            st.success("✅ File uploaded successfully!")

            st.markdown("#### 🧾 Columns:")
            st.write(df.columns.tolist())
        except Exception as e:
            st.error(str(e))

    user_query = st.text_area("Ask a data question", placeholder="e.g. Replace missing values and save to df1")

    if st.button("Generate & Run Code"):
        if "df" not in st.session_state:
            st.warning("Please upload a file first.")
        elif not user_query.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("🧠 Thinking..."):
                from app.state_manager import get_active_dataframe
                active_df = get_active_dataframe(st.session_state)
                df_columns = active_df.columns.tolist() if active_df is not None else []

                code = get_code_from_query(user_query, df_columns)

                code = code.strip()
                code = code.replace("```python", "").replace("```", "").strip()
                code = re.sub(r'^[`]+|[`]+$', '', code).strip()
                code = code.replace("plt.show()", "")  # Strip plt.show()

                st.subheader("🧾 Generated Code")
                st.code(code, language="python")

                result = execute_user_code(code, st.session_state)
                st.session_state["last_code"] = code
                st.session_state["last_result"] = result

# --- RIGHT PANEL: Outputs ---
with right:
    st.header("📤 Output")

    if "last_result" in st.session_state:
        st.subheader("Console Output")
        st.text(st.session_state["last_result"])

        st.subheader("Matplotlib Plots")
        if "last_figures" in st.session_state:
            for fig in st.session_state["last_figures"]:
                st.pyplot(fig)
        else:
            render_all_matplotlib_plots()

    # 🔍 Show original uploaded data
    if "df_original" in st.session_state:
        with st.expander("📁 Show Original Data"):
            if st.button("Show Original Data"):
                st.dataframe(st.session_state["df_original"])

    # 📂 Show all available DataFrames
    all_dfs = get_all_dataframes(st.session_state)

    if all_dfs:
        with st.expander("📊 Show DataFrames"):
            selected_df_name = st.selectbox("Select a DataFrame to work with:", list(all_dfs.keys()))
            st.session_state["selected_df_name"] = selected_df_name
            st.dataframe(st.session_state[selected_df_name])
