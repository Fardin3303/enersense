from fastapi import FastAPI, HTTPException
import logging

from database_manager import DatabaseManager
from constants import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


# Create an instance of DatabaseManager
try:
    db_manager = DatabaseManager(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
except Exception as e:
    LOGGER.error("Error connecting to the database: %s", str(e))
    raise e


APP = FastAPI()


@APP.get("/messages")
def get_all_messages() -> dict:
    """
    Retrieves all messages from the database.

    Returns:
        dict: A dictionary containing the retrieved messages.
    Raises:
        HTTPException: If there is an error retrieving messages from the database.
    """
    try:
        LOGGER.info("Retrieving all messages from the database")
        messages = db_manager.get_all_messages()
        LOGGER.debug("Retrieved messages: %s", messages)
        return {"messages": messages}
    except Exception as e:
        LOGGER.error("Error retrieving messages from the database: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
