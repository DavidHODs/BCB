import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from fastapi import WebSocket
from v1.models import ChatRoomMessageModel, ChatRoomModel
from v1.schemas import ChatRoomSchema, ChatRoomMessageSchema, ChatMessagePayloadSchema
from v1.type_defs import APIResponse, CreateData
from v1.errors import AppException
from typing_extensions import Dict

class ChatService:
  def __init__(self) -> None:
    self.active_connections: Dict[str, set[WebSocket]] = {}

  async def create_room(self, db: AsyncSession, chat_data: ChatRoomSchema) -> APIResponse[CreateData]:
    try: 
      room = ChatRoomModel(names=chat_data.name)
      db.add(room)
      await db.commit()
      return {
        "data": {
          "id":  uuid.UUID(str(room.id)),
          "message": f"{room.name} created successfully"
        }
      }
      
    except (SQLAlchemyError, Exception) as exc:
      await db.rollback()
      raise AppException.classify_error(exc)

  async def save_message(self, db: AsyncSession, message_data: ChatRoomMessageSchema) -> APIResponse[ChatRoomMessageModel]:
    try:
      message = ChatRoomMessageModel(**message_data.model_dump())
      db.add(message)
      await db.commit()
      
      return {
        "data": message
      }
      
    except (SQLAlchemyError, AppException) as exc:
      await db.rollback()
      raise AppException.classify_error(exc)

  async def get_previous_messages(self, db: AsyncSession, chat_room_id: str, limit: int, page: int) -> APIResponse[list[ChatRoomMessageModel]]:
    try: 
      result = await db.execute(
        select(ChatRoomMessageModel).
        where(ChatRoomMessageModel.chat_room_id == chat_room_id)
        .offset((page - 1) * limit)
        .limit(limit)
        .order_by(ChatRoomMessageModel.created_at.desc())
      )
      
      return {
        "data": list(result.scalars().all())
      }
    except (SQLAlchemyError, Exception) as exc:
      raise AppException.classify_error(exc)

  async def connect(self, room_id: str, websocket: WebSocket) -> APIResponse[None]:
    try:
      await websocket.accept()
      if room_id not in self.active_connections:
        self.active_connections[room_id] = set()
        
      self.active_connections[room_id].add(websocket)
      return {
        "data": None
      }
    except Exception as exc:
        raise AppException.classify_error(exc)
      
  async def disconnect(self, room_id: str, websocket: WebSocket) -> APIResponse[None]:
    try:
      if room_id in self.active_connections:
        self.active_connections[room_id].discard(websocket)
        
        if not self.active_connections[room_id]:
          del self.active_connections[room_id]
          
      return {
        "data": None
      }
    except Exception as exc:
        raise AppException.classify_error(exc)
      
  async def broadcast(self, room_id: str, payload: ChatMessagePayloadSchema) -> APIResponse[None]:
    try:
      connections: set[WebSocket] = self.active_connections.get(room_id, set())
      for connection in connections.copy():
        await connection.send_json(payload.model_dump())
        
      return {
        "data": None
      }
    except Exception as exc:
      await self.disconnect(room_id, connection)
      raise AppException.classify_error(exc)