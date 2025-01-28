import streamlit as st

import tic_tac_toe
from encoder import password_encoder_ui
from mqtt_publisher import mqtt_client_ui
from deepseek_ollama import chat_bot

st.sidebar.title("Menu")
menu = st.sidebar.radio("Choose an option", ["Password Encoder", "MQTT Publisher", "TIC TAC TOE","Chat Bot"])

if menu == "Password Encoder":
    password_encoder_ui()
elif menu == "MQTT Publisher":
    mqtt_client_ui()
elif menu == "TIC TAC TOE":
    tic_tac_toe.main()
elif menu == "Chat Bot":
    chat_bot()
