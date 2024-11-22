# import streamlit as st

# date_and_time = st.text_input('date and time')
# pickup_longitude = st.text_input('pickup longitude')
# pickup_latitude = st.text_input('pickup latitude')
# dropoff_longitude = st.text_input('dropoff longitude')
# dropoff_latitude = st.text_input('dropoff latitude')
# passenger_count = st.text_input('passenger count')

# import requests

# url = 'https://taxifare.lewagon.ai/predict'

# #Let's build a dictionary containing the parameters for our API...
# params = {'pickup_datetime': date_and_time, 'pickup_latitude': pickup_latitude, 'pickup_longitude': pickup_longitude, 'dropoff_latitude': dropoff_latitude, 'dropoff_longitude': dropoff_longitude, 'passenger_count': passenger_count}

# #Let's call our API using the `requests` package
# response = requests.get(url, params=params).json()

# #Let's retrieve the prediction from the **JSON** returned by the API...
# st.write("Fare", response['fare'])

## Finally, we can display the prediction to the user

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Function to get coordinates from address using a geocoding API
def get_coordinates(address, access_token):
    url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json'
    params = {
        'access_token': access_token
    }
    response = requests.get(url, params=params).json()

    try:
        coordinates = response['features'][0]['geometry']['coordinates']
        return coordinates
    except (IndexError, KeyError):
        st.error(f"Error retrieving coordinates for {address}.")
        return None

# Function to predict the taxi fare based on pickup and dropoff coordinates
def predict_fare(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon, passenger_count, pickup_datetime):
    taxi_fare_url = 'https://taxifare.lewagon.ai/predict'  # Your API URL
    params = {
        "pickup_latitude": pickup_lat,
        "pickup_longitude": pickup_lon,
        "dropoff_latitude": dropoff_lat,
        "dropoff_longitude": dropoff_lon,
        "passenger_count": passenger_count,
        "pickup_datetime": pickup_datetime
    }

    response = requests.get(taxi_fare_url, params=params)

    if response.status_code == 200:
        data = response.json()
        fare = round(data['fare'], 2)
        return fare
    else:
        st.error(f"Error fetching fare data: {response.text}")
        return None

# Streamlit widgets to take inputs
st.title('Taxi Fare Prediction')
date_and_time = st.text_input('Pickup date and time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
pickup_address = st.text_input('Pickup Address')
dropoff_address = st.text_input('Dropoff Address')
pickup_latitude = st.text_input('Pickup Latitude (optional)')
pickup_longitude = st.text_input('Pickup Longitude (optional)')
dropoff_latitude = st.text_input('Dropoff Latitude (optional)')
dropoff_longitude = st.text_input('Dropoff Longitude (optional)')
passenger_count = st.number_input('Passenger Count', min_value=1, value=1)

access_token = st.text_input('Mapbox Access Token')  # Add your Mapbox access token here

# Automatically get coordinates if user hasn't provided them
if not pickup_latitude or not pickup_longitude:
    if pickup_address:
        pickup_coords = get_coordinates(pickup_address, access_token)
        if pickup_coords:
            pickup_latitude, pickup_longitude = pickup_coords
else:
    pickup_coords = (pickup_latitude, pickup_longitude)

if not dropoff_latitude or not dropoff_longitude:
    if dropoff_address:
        dropoff_coords = get_coordinates(dropoff_address, access_token)
        if dropoff_coords:
            dropoff_latitude, dropoff_longitude = dropoff_coords
else:
    dropoff_coords = (dropoff_latitude, dropoff_longitude)

# Show map if coordinates are available
if pickup_coords and dropoff_coords:
    st.map(pd.DataFrame({
        'latitude': [pickup_latitude, dropoff_latitude],
        'longitude': [pickup_longitude, dropoff_longitude]
    }))

    # Display the fare prediction
    fare = predict_fare(
        float(pickup_latitude), float(pickup_longitude),
        float(dropoff_latitude), float(dropoff_longitude),
        passenger_count, date_and_time
    )

    if fare is not None:
        st.write(f"Predicted Taxi Fare: ${fare}")
else:
    st.warning("Please provide valid addresses or coordinates.")
