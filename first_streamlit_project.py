import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# crimeDf = pd.read_csv("UK_Police_Street_Crime_2018-10-01_to_2021_09_31.csv")
crimeDf_URL = ("/Volumes/Transcend/Projects/streamlit_first_project/UK_Police_Street_Crime_2018-10-01_to_2021_09_31.csv")


st.title("Uk Crime")
st.markdown("This application is a Streamlit Dashboard that can be used"
"to analyze crime locations in UK 💂‍♂️")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(crimeDf_URL, nrows=nrows) # parse_dates=[["Month"]]
    data.dropna(subset =["Latitude","Longitude"],inplace=True) #subset =["Latitude","Longitude"]
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace = True)

    return(data)

data = load_data(100000)

st.header("Where is crime highest in the UK?")
# crime_num = st.slider ...
st.map(data[["latitude","longitude"]])



st.header("How many crimes occur during a given month?")
month = st.selectbox("month to look at", range(1,12),1)
data = data[pd.to_datetime(data["month"],format="%Y-%m").dt.month==month]






#st.markdown("Crimes between %i and %i" %(month))
#
midpoint= (np.average(data["latitude"]), np.average(data["longitude"]))
#
st.write(pdk.Deck(
     map_style="mapbox://styles/mapbox/light/v9",
     initial_view_state= {"latitude":midpoint[0],"longitude":midpoint[1],
         "zoom":11, "pitch":50
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data = data[["month","latitude","longitude"]],
        get_position = ["longitude","latitude"],
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0, 1000],
        ),
    ],
))






if st.sidebar.checkbox("Show Raw Data", False): # False means: uncheck by default
    st.subheader("Raw Data")
    st.write(data)
