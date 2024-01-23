"""
This module contains constants used in the application.

- DB_HOST: The hostname of the PostgreSQL database server.
- DB_PORT: The port number of the PostgreSQL database server.
- DB_NAME: The name of the database to connect to.
- DB_USER: The username to use for authentication.
- DB_PASSWORD: The password to use for authentication.

- MQTT_BROKER_HOST: The hostname of the MQTT broker.
- MQTT_BROKER_PORT: The port number of the MQTT broker.
- MQTT_TOPIC: The topic to subscribe to for MQTT messages.

- SAMPLE_PAYLOAD: A sample payload for testing purposes.
"""


# Database connection parameters
DB_HOST = "postgres-db"
DB_PORT = 5432
DB_NAME = "enersense"
DB_USER = "postgres_user"
DB_PASSWORD = "postgres_password"

# MQTT parameters
MQTT_BROKER_HOST = "host.docker.internal"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "charger/1/connector/1/session/1"

# Sample payload
SAMPLE_PAYLOAD = {
    "session_id": 1,
    "energy_delivered_in_kWh": 30,
    "duration_in_seconds": 45,
    "session_cost_in_cents": 70,
}
