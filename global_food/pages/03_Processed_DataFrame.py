import streamlit as st
import pandas as pd
import plotly.express as px

# load and preprocess dataframe
df = st.session_state["dataframe"]

def loadData(df):

    item_filter = "Prevalence of severe food insecurity in the total population (percent) (3-year average)"

    filtered_df = df[df['Item'] == item_filter]

    filtered_df["Year_Middle"] = filtered_df['Year'].apply(lambda x: int(x.split('-')[0])+1)

    filtered_df["Value_Clean"]=pd.to_numeric(
        filtered_df['Value'].str.replace("<", "")
        .replace(">", ""), errors="coerce")

    filtered_df.dropna(subset=['Value_Clean'], inplace=True)

    return filtered_df

processed_df = loadData(df)

st.title("Global Food Security Dashboard")

# create year dropdown menu
years = processed_df["Year_Middle"].unique()
selected_year = st.selectbox("Select Year", years)

processed_df_year = processed_df[processed_df["Year_Middle"]==selected_year] 

# Global Food Security for the selected year
fig_map = px.choropleth(processed_df_year,
                        locations="Area",
                        locationmode="country names",
                        color="Value_Clean",
                        hover_name="Area",
                        hover_data={"Year_Middle": False, "Value_Clean": True},
                        color_continuous_scale="YlOrRd",
                        title="Global Food Insecurity")
st.plotly_chart(fig_map, use_container_width=True)

# Horizontal bar chart on its own row, below the map
top_countries = processed_df_year.nlargest(10, 'Value_Clean')
fig_bar = px.bar(top_countries,
                 x='Value_Clean',
                 y='Area',
                 orientation='h',
                 color='Value_Clean',
                 color_continuous_scale="YlOrRd",
                 title="Top Countries by Food Insecurity Level")
fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig_bar, use_container_width=True)

