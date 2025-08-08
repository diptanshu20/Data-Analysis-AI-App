# app/output_handler.py

import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from state_manager import get_dataframe


def render_output(output_text: str, session_state: dict):
    """
    Renders the output from code execution.

    Args:
        output_text (str): The output or error string from code execution
        session_state (dict): Streamlit session state object
    """
    # Show the printed output (text or errors)
    if output_text:
        st.subheader("Execution Log / Output")
        st.code(output_text, language="python")

    # Show any available plots
    for i in plt.get_fignums():
        fig = plt.figure(i)
        st.pyplot(fig)

    # Show all available DataFrames in session state
    st.subheader("Available DataFrames")
    for key, value in session_state.items():
        if isinstance(value, pd.DataFrame):
            st.markdown(f"**{key}**")
            st.dataframe(value)