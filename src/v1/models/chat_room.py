import uuid
from sqlalchemy import Column, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class ChatRoomModel(Base):
  __tablename__ = "chat_rooms"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = Column(String, nullable=False, unique=True)
  created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
