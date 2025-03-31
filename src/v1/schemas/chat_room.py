import uuid

from pydantic import BaseModel
from typing_extensions import Optional


class ChatRoomSchema(BaseModel):
  id: Optional[uuid.UUID]
  name: str
