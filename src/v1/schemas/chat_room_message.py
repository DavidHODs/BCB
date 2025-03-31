
from pydantic import BaseModel


class ChatRoomMessageSchema(BaseModel):
  username: str
  message: str
