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
