import uuid

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class ChatRoomMessageModel(Base):
  __tablename__ = "chat_room_messages"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  chat_room_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "chat_rooms.id",
          ondelete="CASCADE"),
      nullable=False)
  username = Column(String, nullable=False)
  message = Column(Text, nullable=False)
  created_at = Column(
      TIMESTAMP(
          timezone=True),
      server_default=func.now(),
      nullable=False)
