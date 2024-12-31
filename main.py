import streamlit as st
from encoder import password_encoder_ui
from mqtt_publisher import mqtt_publisher_ui

st.sidebar.title("Menu")
menu = st.sidebar.radio("Choose an option", ["Password Encoder", "MQTT Publisher"])

if menu == "Password Encoder":
    password_encoder_ui()
elif menu == "MQTT Publisher":
    mqtt_publisher_ui()
