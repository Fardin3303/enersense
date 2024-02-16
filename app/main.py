import mqtt_subscriber
import uvicorn
import logging
import threading

from rest_api import APP

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def start_mqtt_subscriber() -> None:
    """
    Start MQTT subscriber to listen to messages.
    """
    mqtt_subscriber.start_subscriber()


if __name__ == "__main__":
    # Create a separate thread for the MQTT subscriber
    # so that it doesn't block the main thread
    try:
        mqtt_thread = threading.Thread(target=start_mqtt_subscriber)
        mqtt_thread.start()
    except Exception as e:
        LOGGER.error("Error starting MQTT subscriber: %s", str(e))
        raise e

    # Start FastAPI application
    LOGGER.info("Starting FastAPI server")
    try:
        uvicorn.run(APP, host="0.0.0.0", port=8000)
    except Exception as e:
        LOGGER.error("Error starting FastAPI server: %s", str(e))
        raise e
