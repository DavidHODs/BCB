from typing_extensions import Optional
import uuid
from pydantic import BaseModel

class ChatRoomMessageSchema(BaseModel):
  username: str
  message: str

