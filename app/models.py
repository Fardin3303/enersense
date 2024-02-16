from pydantic import BaseModel

# Define response model for messages
class Message(BaseModel):
    id: int
    content: str