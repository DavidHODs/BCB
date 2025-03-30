from typing_extensions import Optional
import uuid
from pydantic import BaseModel

class ChatRoomSchema(BaseModel):
  id: Optional[uuid.UUID]
  name: str
