from fastapi import FastAPI
import logging

from database_manager import DatabaseManager
from constants import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


# Create an instance of DatabaseManager
db_manager = DatabaseManager(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)


APP = FastAPI()


@APP.get("/messages")
def get_all_messages():
    # Retrieve all messages from the database
    LOGGER.info("Retrieving all messages from the database...")
    messages = db_manager.get_all_messages()
    return {"messages": messages}
