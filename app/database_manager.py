import json
import psycopg2


class DatabaseManager:
    def __init__(self, host, port, database, user, password):
        self.conn = psycopg2.connect(
            host=host, port=port, database=database, user=user, password=password
        )
        self.cursor = self.conn.cursor()
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        # Create a table if it doesn't exist
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                payload JSONB,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """
        )
        self.conn.commit()

    def store_message(self, payload):
        # Store the received message in the database
        # Convert the payload to a JSON-formatted string
        payload_json = json.dumps(payload)
        query = "INSERT INTO messages (payload) VALUES (%s);"
        self.cursor.execute(query, (payload_json,))
        self.conn.commit()

    def get_all_messages(self):
        # Retrieve all messages from the database
        query = "SELECT * FROM messages;"
        self.cursor.execute(query)
        return self.cursor.fetchall()
