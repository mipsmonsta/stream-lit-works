import streamlit as st

st.title("Sample data with Data Headers")
df = st.session_state["dataframe"]

st.markdown("### Data Head")
st.write(df.head())

st.markdown("### Data Tail")
st.write(df.tail())