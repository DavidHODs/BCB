import uuid
from fastapi.websockets import WebSocketState
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.database import get_db
from sqlalchemy.future import select
from fastapi import WebSocket
from v1.models import ChatRoomMessageModel, ChatRoomModel
from v1.schemas import ChatRoomSchema, ChatRoomMessageSchema
from v1.type_defs import APIResponse, CreateData
from v1.errors import AppException
from typing_extensions import Dict

class ChatService:
  def __init__(self) -> None:
    self.active_connections: Dict[str, set[WebSocket]] = {}

  def create_room(self, db: Session, chat_data: ChatRoomSchema) -> APIResponse[CreateData]:
    try: 
      room = ChatRoomModel(name=chat_data.name)
      db.add(room)
      db.commit()
      db.refresh(room)
      
      return {
        "data": {
          "id":  uuid.UUID(str(room.id)),
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
      
  async def disconnect(self, chat_room_id: str, websocket: WebSocket) -> APIResponse[str]:
    try:
      if chat_room_id in self.active_connections:
        await self.active_connections[chat_room_id].discard(websocket)
        
        if not self.active_connections[chat_room_id]:
          del self.active_connections[chat_room_id]
          
      return {
        "data": "Disconnected"
      }
    except Exception as exc:
        raise AppException.classify_error(exc)
      
  async def broadcast(self, db: Session, chat_room_id: str, message_data: ChatRoomMessageSchema) -> APIResponse[str]:
    try:
      connections: set[WebSocket] = self.active_connections.get(chat_room_id, set())
      
      message = ChatRoomMessageModel(**message_data.model_dump())
      message.chat_room_id = chat_room_id
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
      await db.rollback()
      raise AppException.classify_error(exc)
    