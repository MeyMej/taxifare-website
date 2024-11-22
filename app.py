import streamlit as st
import requests
import pandas as pd

# Input fields for user to provide data
date_and_time = st.text_input('Date and Time (YYYY-MM-DD HH:MM:SS)')
pickup_longitude = st.text_input('Pickup Longitude')
pickup_latitude = st.text_input('Pickup Latitude')
dropoff_longitude = st.text_input('Dropoff Longitude')
dropoff_latitude = st.text_input('Dropoff Latitude')
passenger_count = st.text_input('Passenger Count')

# If all inputs are provided
if date_and_time and pickup_longitude and pickup_latitude and dropoff_longitude and dropoff_latitude and passenger_count:
    # Convert text inputs to appropriate data types
    try:
        pickup_longitude = float(pickup_longitude)
        pickup_latitude = float(pickup_latitude)
        dropoff_longitude = float(dropoff_longitude)
        dropoff_latitude = float(dropoff_latitude)
        passenger_count = int(passenger_count)
        
        # URL for API request
        url = 'https://taxifare.lewagon.ai/predict'

        # Prepare parameters to send in the API request
        params = {
            'pickup_datetime': date_and_time,
            'pickup_latitude': pickup_latitude,
            'pickup_longitude': pickup_longitude,
            'dropoff_latitude': dropoff_latitude,
            'dropoff_longitude': dropoff_longitude,
            'passenger_count': passenger_count
        }

        # Call the API
        response = requests.get(url, params=params).json()

        # Display the fare prediction
        st.write("Predicted Fare:", response.get('fare', 'Error fetching fare'))

        # Prepare data for the map
        df = pd.DataFrame({
            'latitude': [pickup_latitude, dropoff_latitude],
            'longitude': [pickup_longitude, dropoff_longitude]
        })

        # Display the map with pickup and dropoff locations
        st.map(df)

    except ValueError:
        st.error("Please ensure all inputs are valid numbers for coordinates and passenger count.")
else:
    st.write("Please fill in all fields to get the prediction.")
