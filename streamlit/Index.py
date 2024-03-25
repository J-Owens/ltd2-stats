import streamlit as st

st.set_page_config(
    page_title="Hello",
)

st.sidebar.success("Select a chart to view.")

st.markdown(
    """
    **👈  Select a chart from the sidebar**
"""
)