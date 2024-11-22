import streamlit as st
import requests
import pandas as pd

date_and_time = st.text_input('date and time')
pickup_longitude = st.text_input('pickup longitude')
pickup_latitude = st.text_input('pickup latitude')
dropoff_longitude = st.text_input('dropoff longitude')
dropoff_latitude = st.text_input('dropoff latitude')
passenger_count = st.text_input('passenger count')

url = 'https://taxifare.lewagon.ai/predict'

#Let's build a dictionary containing the parameters for our API...
params = {'pickup_datetime': date_and_time, 'pickup_latitude': pickup_latitude, 'pickup_longitude': pickup_longitude, 'dropoff_latitude': dropoff_latitude, 'dropoff_longitude': dropoff_longitude, 'passenger_count': passenger_count}

#Let's call our API using the `requests` package
response = requests.get(url, params=params).json()

#Let's retrieve the prediction from the **JSON** returned by the API...
st.write("Fare", response['fare'])

# df = {'latitude': [pickup_latitude, dropoff_latitude],
#         'longitude': [pickup_longitude, dropoff_longitude]}

# st.map(df)
