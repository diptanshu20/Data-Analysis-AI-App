# utils/plot_utils.py

import matplotlib.pyplot as plt
import streamlit as st

def render_all_matplotlib_plots():
    """
    Renders all active matplotlib plots in Streamlit and clears them.
    """
    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        st.pyplot(fig)
    plt.close("all")
