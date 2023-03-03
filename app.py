import streamlit as st
import datetime
import requests
import folium
from streamlit_folium import folium_static
import numpy as np

if 'lat' not in st.session_state:
    st.session_state.lat = None

if 'lon' not in st.session_state:
    st.session_state.lat = None

'''
# TaxiFare NYC Model
#### Welcome
'''
with st.form('input_form'):
    col1, col2 = st.columns(2)
    with col1:
        pickup_date = st.date_input('Date', value=datetime.datetime.now())
        pickup_latitude = st.number_input('Pickup Latitude',
                                        min_value=float(st.secrets['location_range']['MIN_LAT']),
                                        max_value=float(st.secrets['location_range']['MAX_LAT']),
                                        value=float(st.secrets['default_trip']['START_LAT']),
                                        format="%f")
        pickup_longitude = st.number_input('Pickup Longitude',
                                        min_value=float(st.secrets['location_range']['MIN_LON']),
                                        max_value=float(st.secrets['location_range']['MAX_LON']),
                                        value=float(st.secrets['default_trip']['START_LON']),
                                        format="%f")
    with col2:
        pickup_time = st.time_input('Pickup Time', value=datetime.datetime.now())
        dropoff_latitude = st.number_input('Dropoff Latitude',
                                        min_value=float(st.secrets['location_range']['MIN_LAT']),
                                        max_value=float(st.secrets['location_range']['MAX_LAT']),
                                        value=float(st.secrets['default_trip']['END_LAT']),
                                        format="%f")
        dropoff_longitude = st.number_input('Dropoff Longitude',
                                            ## value = st.session_state.lat
                                            min_value=float(st.secrets['location_range']['MIN_LON']),
                                            max_value=float(st.secrets['location_range']['MAX_LON']),
                                            value=float(st.secrets['default_trip']['END_LON']),
                                            format="%f")
    passenger_count = st.slider('How many passengers?', 1, 8)
    button = st.form_submit_button('Calculate')


map = folium.Map(location=[float(st.secrets['default_trip']['START_LAT']), float(st.secrets['default_trip']['START_LON'])],
            tiles="OpenStreetMap",
            width="%100",
            height="%80",
            zoom_start=11.5)

folium.Marker(location=[pickup_latitude, pickup_longitude], popup='Start', draggable=False, icon=folium.Icon(color='green')).add_to(map)
folium.Marker(location=[dropoff_latitude, dropoff_longitude], popup='End', draggable=True, icon=folium.Icon(color='red')).add_to(map)

folium_static(map)

url = 'https://taxifare.lewagon.ai/predict'

if button:
    pickup_datetime = f'{pickup_date} {pickup_time}'
    params = {
        'pickup_datetime': pickup_datetime,
        'pickup_latitude': pickup_latitude,
        'pickup_longitude': pickup_longitude,
        'dropoff_latitude': dropoff_latitude,
        'dropoff_longitude': dropoff_longitude,
        'passenger_count': passenger_count
    }
    response = requests.get(url, params).json()
    st.write(f'Estimated Taxi fare amount: ${round(response["fare"], 2)}')
