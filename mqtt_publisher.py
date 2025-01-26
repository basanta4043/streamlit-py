import json
import logging
from dataclasses import dataclass
from queue import Queue
from threading import Thread

import paho.mqtt.client as mqtt
import streamlit as st

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Queue to store received messages
message_queue = Queue()

@dataclass
class MQTTConfig:
    host: str
    port: int = 1883
    keepalive: int = 60
    qos: int = 1


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    connection_codes = {
        0: "Connected successfully",
        1: "Incorrect protocol version",
        2: "Invalid client identifier",
        3: "Server unavailable",
        4: "Bad username or password",
        5: "Not authorized"
    }
    logger.info(f"Connection status: {connection_codes.get(rc, 'Unknown error')}")


def on_message(client, userdata, msg):
    logger.info(f"Received message on topic {msg.topic}: {msg.payload.decode('utf-8')}")
    message_queue.put({
        "topic": msg.topic,
        "message": msg.payload.decode('utf-8')
    })


def on_publish(client, userdata, mid):
    logger.info(f"Message {mid} published successfully.")


def mqtt_client_ui():
    st.title("📡 MQTT Client")

    # Initialize session state
    if "received_messages" not in st.session_state:
        st.session_state["received_messages"] = []

    # MQTT Config
    host = st.text_input("MQTT Host", value="mqttuat.instantpaygateway.com")
    port = st.number_input("MQTT Port", value=1883)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Sender
    sender_topic = st.text_input("Sender Topic", value="terminal/txn/sgr-card/sale/request")
    message = st.text_area("Sender Message", value=json.dumps({
        "amount": 5000,
        "serialNumber": "F20MP1106001795",
        "tenantId": "institution_000",
        "paymentMode": "CASH"
    }, indent=4))

    # Receiver
    receiver_topic = st.text_input("Receiver Topic", value="terminal/txn/sgr-card/sale/response")

    # Connect MQTT Client
    mqttc = mqtt.Client()
    mqttc.username_pw_set(username, password)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_publish = on_publish

    if st.button("Start MQTT Client"):
        try:
            mqttc.connect(host, port=int(port))
            mqttc.loop_start()
            mqttc.subscribe(receiver_topic)
            st.success("MQTT Client started successfully.")
        except Exception as e:
            st.error(f"Error starting MQTT Client: {str(e)}")

    # Periodically update received messages from the queue
    while not message_queue.empty():
        message = message_queue.get()
        st.session_state["received_messages"].append(message)

    # Publish Message
    if st.button("Publish Message"):
        try:
            mqttc.publish(sender_topic, message)
            st.success("Message published successfully.")
        except Exception as e:
            st.error(f"Error publishing message: {str(e)}")

    # Display received messages
    st.subheader("Received Messages")
    for received in st.session_state["received_messages"]:
        st.write(f"**Topic:** {received['topic']}")
        st.write(f"**Message:** {received['message']}")
        st.markdown("---")

    # Stop MQTT Client
    if st.button("Stop MQTT Client"):
        try:
            mqttc.disconnect()
            mqttc.loop_stop()
            st.success("MQTT Client stopped successfully.")
        except Exception as e:
            st.error(f"Error stopping MQTT Client: {str(e)}")
