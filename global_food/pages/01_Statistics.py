import streamlit as st
import pandas as pd

st.title("Statistics")

df = st.session_state["dataframe"]
st.write(df.describe())
