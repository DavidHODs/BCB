from uuid import UUID

from fastapi import WebSocket
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing_extensions import Dict

from v1.errors import AppException
from v1.models import ChatRoomMessageModel, ChatRoomModel
from v1.schemas import ChatRoomMessageSchema, ChatRoomSchema
from v1.type_defs import APIResponse, CreateData


class ChatService:
  def __init__(self) -> None:
    self.active_connections: Dict[str, set[WebSocket]] = {}

  def create_room(self, db: Session,
                  chat_data: ChatRoomSchema) -> APIResponse[CreateData]:
    try:
      room = ChatRoomModel(name=chat_data.name)
      db.add(room)
      db.commit()
      db.refresh(room)

      return {
          "data": {
              "id": UUID(str(room.id)),
              "message": f"{room.name} created successfully"
          }
      }

    except (SQLAlchemyError, Exception) as exc:
      db.rollback()
      raise AppException.classify_error(exc)

  async def connect(self, websocket: WebSocket, chat_room_id: str) -> str:
    try:
      await websocket.accept()

      if chat_room_id not in self.active_connections:
        self.active_connections[chat_room_id] = set()

      self.active_connections[chat_room_id].add(websocket)

      while True:
        await websocket.receive_json()

    except Exception as exc:
      raise AppException.classify_error(exc)

  async def disconnect(self, chat_room_id: str,
                       websocket: WebSocket) -> APIResponse[str]:
    try:
      if chat_room_id in self.active_connections:
        self.active_connections[chat_room_id].discard(websocket)

        if not self.active_connections[chat_room_id]:
          del self.active_connections[chat_room_id]

      return {
          "data": "Disconnected"
      }
    except Exception as exc:
      raise AppException.classify_error(exc)

  async def broadcast(self, db: Session, chat_room_id: str,
                      message_data: ChatRoomMessageSchema) -> APIResponse[str]:
    try:
      connections: set[WebSocket] = self.active_connections.get(
          chat_room_id, set())

      message = ChatRoomMessageModel(
          chat_room_id=UUID(chat_room_id),
          **message_data.model_dump()
      )

      db.add(message)
      db.commit()

      for connection in list(connections):
        try:
          await connection.send_json(message_data.model_dump())
        except Exception:
          connections.discard(connection)

      return {
          "data": "Message broadcasted"
      }

    except Exception as exc:
      db.rollback()
      raise AppException.classify_error(exc)
