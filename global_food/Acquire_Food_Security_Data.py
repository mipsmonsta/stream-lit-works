import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.markdown("## UN Food security analysis")

file = st.file_uploader("Upload food security data file")
if file:
    df = pd.read_csv(file)
    st.session_state["dataframe"] = df
