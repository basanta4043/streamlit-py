import streamlit as st
import json
import paho.mqtt.client as mqtt
import time
from typing import Any, Dict, Set
import logging
from dataclasses import dataclass

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MQTTConfig:
    host: str
    port: int = 1883
    keepalive: int = 60
    qos: int = 1


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


def on_publish(client, userdata: Set[int], mid: int):
    if isinstance(userdata, set):
        userdata.discard(mid)
        logger.info(f"Message {mid} published successfully.")


def publish_message(config: MQTTConfig, topic: str, message: Dict[str, Any], username: str, password: str) -> bool:
    mqttc = mqtt.Client()
    mqttc.username_pw_set(username, password)
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    unacked_publish = set()
    mqttc.user_data_set(unacked_publish)

    try:
        mqttc.connect(config.host, port=config.port, keepalive=config.keepalive)
        mqttc.loop_start()

        start_time = time.time()
        while not mqttc.is_connected() and (time.time() - start_time) < 5:
            time.sleep(0.1)

        if not mqttc.is_connected():
            st.error("Failed to connect to MQTT broker.")
            return False

        msg_info = mqttc.publish(topic, json.dumps(message), qos=config.qos)
        if not msg_info.is_published():
            unacked_publish.add(msg_info.mid)

        start_time = time.time()
        while unacked_publish and (time.time() - start_time) < 10:
            time.sleep(0.1)

        if len(unacked_publish) == 0:
            st.success("Message published successfully.")
            return True
        else:
            st.error("Failed to publish message.")
            return False

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        st.error(f"Error: {str(e)}")
        return False
    finally:
        mqttc.disconnect()
        mqttc.loop_stop()


def mqtt_publisher_ui():
    st.title("📡 MQTT Publisher")

    # MQTT Config
    host = st.text_input("MQTT Host", value="mqttuat.instantpaygateway.com")
    port = st.number_input("MQTT Port", value=1883)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    topic = st.text_input("Topic", value="terminal/txn/sgr-card/sale/request")

    # Message
    payment_mode = st.selectbox("Payment Mode", ["CASH", "MNO", "PREPAID_CARD"])
    amount = st.number_input("Amount", value=5000)
    serial_number = st.text_input("Serial Number", value="F20MP1106001795")
    tenant_id = st.text_input("Tenant ID", value="institution_000")

    payload = {
        "amount": amount,
        "serialNumber": serial_number,
        "tenantId": tenant_id,
        "paymentMode": payment_mode
    }

    if st.button("Publish Message"):
        config = MQTTConfig(host=host, port=port)
        publish_message(config, topic, payload, username, password)
