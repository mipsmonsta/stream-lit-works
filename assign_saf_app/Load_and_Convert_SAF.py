import streamlit as st
from io import StringIO
import pathlib
import pandas as pd

def getEvents(bytes_inputs:list[bytes], outputfile: str):
    with open(outputfile, 'w') as dest:
        start_comb = False
        for line in bytes_inputs:
            line = StringIO(line.decode("utf-8")).read()
            
            if line.startswith("$DATA"):
                start_comb = True
                
            if start_comb:
                if line.startswith("011"):
                    dest.write(line + "\n")
            
    
    return start_comb # using start comb to see if SAF file

st.set_page_config(layout="wide")
st.title("SAF Assign Explorer")

# Upload SAF file to convert
file_input = st.file_uploader("Upload SAF File", type="SAF")

base_IAF_dir = "./IAF/"

output_name = st.text_input("Enter intermediate SAF filename (without extension)")
if file_input and output_name:
    bytes_input = file_input.readlines()
    is_success = getEvents(bytes_input, base_IAF_dir + output_name + ".iaf")
    if is_success:
        st.success(f"Intermediate SAF file {output_name}.iaf created")
    else:
        st.error("Intermedate file failed to be created")

# list all the intermediate SAF file converted
list_IAFs = [f.name for f in pathlib.Path(base_IAF_dir).iterdir() if f.is_file() and f.name.endswith(".iaf")]

# Display first five rows of intermediate SAF file selected
selected_IAF = None
if list_IAFs:
    st.header("Select Converted IAF files")
    iafs_expander = st.expander("Converted Intermediate .iaf files")

    with iafs_expander:
        index = 0
        if "selection_index" in st.session_state: # restore selected IAF using session
            index = st.session_state["selection_index"] 
        selected_IAF = st.selectbox(f"{len(list_IAFs)} IAF files", options=list_IAFs, index=index)
        if selected_IAF: # remember selected IAF
            st.session_state["selection_index"] = list_IAFs.index(selected_IAF)

df = None # selected IAF Dataframe
if selected_IAF:
    columns= ["ID", "ShortName", "Date", "Time", "Miliseconds", "Meters", "GPSSpeed", "OdometerSpeed"
              ,"NavState", "GPSXCoord", "GPSYCoord", "GPSDir", "CoordQuality", "NoSatellites",
              "LatchedOdometer", "SubType", "BlockIdx", "BlockNo", "RouteNo",
              "RunNo", "DayType", "TripIdx", "PattIdx", "BlockNoString", "BFCDriverID",
              "BFCDutyID", "BFCTripType", "OperationDay"]
    df = pd.read_csv(base_IAF_dir + selected_IAF, names=columns, delimiter="\t")
    
    st.header(f"First 5 datapoint for {selected_IAF} out of {len(df)} records")
    st.write(df.head())

st.session_state["dataframe"] = df
if selected_IAF:
    st.session_state["IAF_name"] = selected_IAF
