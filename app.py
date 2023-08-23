import streamlit as st
import pandas as pd
import numpy as np

st.title("This is my title")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows=12):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')

row_count = st.selectbox('rows',(10, 100, 1000), 2)
my_data = load_data(row_count)

#update the existing text control
data_load_state.text("Done! (using st.cache_data)")

st.dataframe(my_data)

#st.subheader('Raw data')
#st.write(my_data)

st.subheader('Number of pickups by hour')

hist_values = np.histogram(my_data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

#st.write(hist_values)

st.bar_chart(hist_values)

hour_to_filter = st.slider("Hour",0,23,17)
filtered_data = my_data[my_data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)