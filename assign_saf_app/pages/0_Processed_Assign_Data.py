import streamlit as st
import pandas as pd
import plotly.express as px

st.title("IAF File Analysis")

df = None
if "dataframe" in st.session_state:
    df = st.session_state["dataframe"]
if isinstance(df, pd.DataFrame):
    
    df = st.session_state["dataframe"]
    IAF_name = st.session_state["IAF_name"]

    # transform the dataframe
    processed_df = df.loc[:,["ShortName", "Date", "Time", "SubType", "BlockIdx", "GPSYCoord", "GPSXCoord",
                "BlockNo", "RouteNo", "TripIdx", "BlockNoString", "BFCDriverID", "OperationDay"]]
    # get lat/longweihaweiha
    processed_df["Lat"] = processed_df["GPSYCoord"]/3600000
    processed_df["Long"] = processed_df["GPSXCoord"]/3600000

    # remove substype 15, 233, 254, 255
    subtypes_ignore = [15, 252, 253, 254, 255]
    processed_df = processed_df[~processed_df["SubType"].isin(subtypes_ignore)]


    # mapped subtype to strings for easy reference
    subtypes_mapping = {1:"BC Logon", 2:"BC Logon", 3: "BC Logoff", 4:"CC Logon", 10:"Sys Start Trip",
                    11: "Sys End Trip", 13: "Off Route", 23:"On Route"}

    processed_df["SubType"] = processed_df["SubType"].map(subtypes_mapping)

    st.header(f"Processed Assign Data {IAF_name}")
    st.write(processed_df) 

    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label="Total Records ",
                value=f"{len(df)} 🗒️")
    kpi2.metric(label="Total Records after filtering ",
                value=f"{len(processed_df)} 📃")
    # st.write(f"Filtering away SubType={subtypes_ignore}, left {len(processed_df)} records")

    st.header("Map View of Assign Events")

    fig = px.scatter_mapbox(processed_df, lat="Lat", lon="Long", hover_name="SubType", hover_data=["Lat", "Long", processed_df.index], 
                        zoom=10, center={"lat":1.35, "lon":103.8})

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(marker={"size":20, "color":"DarkBlue"}, line=dict(width=3,
                                        color='DarkSlateGrey'))

    st.plotly_chart(fig)


