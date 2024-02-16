import paho.mqtt.client as mqtt
import time
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

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


# Create an instance of DatabaseManager
try:
    db_manager = DatabaseManager(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
except Exception as e:
    LOGGER.error("Error connecting to the database: %s", str(e))
    raise e


def on_connect(client: mqtt.Client, userdata: any, flags: dict, rc: int) -> None:
    """
    Callback function that is called when the MQTT client successfully connects to the broker.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata (any): User-defined data that can be passed to the callback function.
        flags (dict): Response flags sent by the broker.
        rc (int): Result code indicating the success or failure of the connection.

    Returns:
        None
    """
    if rc == 0:
        LOGGER.info("Connected to MQTT broker.")
        client.subscribe(MQTT_TOPIC)
    else:
        LOGGER.info(f"Failed to connect to MQTT broker with result code {rc}")
        # You may choose to exit the script or take other actions on connection failure


def on_message(client: mqtt.Client, userdata: any, msg: mqtt.MQTTMessage) -> None:
    """
    Callback function that is called when a message is received.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata (any): The user-defined data passed to the MQTT client.
        msg (mqtt.MQTTMessage): The received MQTT message.

    Returns:
        None
    """
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


def on_disconnect(client: mqtt.Client, userdata: any, rc: int) -> None:
    """
    Callback function called when the MQTT client is disconnected from the broker.

    Parameters:
        client (mqtt.Client): The MQTT client instance.
        userdata (any): The user-defined data passed to the MQTT client.
        rc (int): The disconnection result code.

    Returns:
        None
    """
    if rc != 0:
        LOGGER.info("Unexpected disconnection.")
    else:
        LOGGER.info("Disconnected.")


def on_log(client: mqtt.Client, userdata: any, level: int, buf: str) -> None:
    """
    Callback function for logging MQTT messages.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata (any): The user-defined data passed to the MQTT client.
        level (int): The severity level of the log message.
        buf (str): The log message.

    Returns:
        None
    """
    LOGGER.info(f"Log: {buf}")


def start_subscriber() -> None:
    """
    Starts the MQTT subscriber and publishes new sessions periodically.

    This function connects to an MQTT broker, sets up the necessary callbacks,
    and starts a loop to handle MQTT events. It publishes a new session every
    60 seconds until an exception occurs. After an exception or when the loop is
    interrupted, it gracefully disconnects from the MQTT broker.

    Raises:
        Exception: If an unexpected error occurs during the execution.
    """
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
        # Publish new sessions every 60 seconds
        while True:
            try:
                client.publish(MQTT_TOPIC, payload=str(SAMPLE_PAYLOAD))
                time.sleep(60)
                LOGGER.info("Published new session.")
            except Exception as e:
                LOGGER.exception(f"Error publishing message: {str(e)}")
    except Exception as e:
        LOGGER.exception(f"Unexpected error: {str(e)}")
        # Ensure a graceful shutdown
        client.disconnect()
        client.loop_stop()
