from typing_extensions import Optional
import uuid
from pydantic import BaseModel

class ChatRoomMessageSchema(BaseModel):
  id: Optional[uuid.UUID]
  chat_room_id: uuid.UUID
  username: str
  message: str
