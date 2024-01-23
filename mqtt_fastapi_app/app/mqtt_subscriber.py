import paho.mqtt.client as mqtt
import time
import traceback
import logging
from datetime import datetime

from database_manager import DatabaseManager
from constants import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_TOPIC,
    SAMPLE_PAYLOAD,
)

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


# Create an instance of DatabaseManager
db_manager = DatabaseManager(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        LOGGER.info("Connected to MQTT broker.")
        client.subscribe(MQTT_TOPIC)
    else:
        LOGGER.info(f"Failed to connect to MQTT broker with result code {rc}")
        # You may choose to exit the script or take other actions on connection failure


def on_message(client, userdata, msg):
    try:
        timestamp = datetime.now().isoformat()
        payload = msg.payload.decode("utf-8")
        LOGGER.info(
            f"Received message - Topic: {msg.topic}, Payload: {payload}, Timestamp: {timestamp}"
        )

        # Store the received message in the database
        db_manager.store_message(payload)
    except Exception as e:
        LOGGER.info(f"Error handling message: {str(e)}")
        traceback.LOGGER.info_exc()


def on_disconnect(client, userdata, rc):
    if rc != 0:
        LOGGER.info("Unexpected disconnection.")
    else:
        LOGGER.info("Disconnected.")


def on_log(client, userdata, level, buf):
    LOGGER.info(f"Log: {buf}")


def start_subscriber():
    try:
        client = mqtt.Client()
        LOGGER.info("Starting subscriber...")
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        client.on_log = on_log

        LOGGER.info(
            f"Connecting to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}"
        )

        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
        # Loop in the background to handle MQTT events
        client.loop_start()
        # Publish new sessions every 1 minute
        while True:
            try:
                client.publish(MQTT_TOPIC, payload=str(SAMPLE_PAYLOAD))
                time.sleep(60)
                LOGGER.info("Published new session.")
            except Exception as e:
                LOGGER.info(f"Error publishing message: {str(e)}")
                traceback.LOGGER.info_exc()
    except Exception as e:
        LOGGER.info(f"Unexpected error: {str(e)}")
        traceback.LOGGER.info_exc()
    finally:
        # Ensure a graceful shutdown
        client.disconnect()
        client.loop_stop()
