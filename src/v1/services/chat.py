import asyncio
import uuid
from fastapi.websockets import WebSocketState
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
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

  async def connect(self, db: AsyncSession, websocket: WebSocket, chat_room_id: str, limit: int, page: int) -> APIResponse[None]:
    try:
      print(f"Attempting to accept WebSocket connection for room: {chat_room_id}")
      await websocket.accept()
      await asyncio.sleep(3)
      
      print("here")
      await websocket.send_text("here")
      
      print("Before DB test query")
      # await db.execute("SELECT 1")  # Just to test DB connection
      # print("DB test query executed")  # Should print if query completes
      # result = await db.execute(
      #     select(ChatRoomMessageModel)
      #     .where(ChatRoomMessageModel.chat_room_id == chat_room_id)
      #     .offset((page - 1) * limit)
      #     .limit(limit)
      #     .order_by(ChatRoomMessageModel.created_at.asc())
      # )
      print("DB query executed")  # Should print if query completes

      # past_messages = result.scalars().all()
      print("another message")  
      await websocket.send_text("lllllllllbbbbbbbbbbbbb")
      past_messagesd = ["kkkkk", "lllllll"]
      
      for message in past_messagesd:
        await websocket.send_text(message)
        
      # for message in past_messages:
      #   await websocket.send_text(message)
                
      if chat_room_id not in self.active_connections:
        self.active_connections[chat_room_id] = set()
        
      self.active_connections[chat_room_id].add(websocket)
      while True:
        await websocket.receive_text()
    except Exception as exc:
      raise AppException.classify_error(exc)
      
  async def disconnect(self, room_id: str, websocket: WebSocket) -> APIResponse[None]:
    try:
      if room_id in self.active_connections:
        await self.active_connections[room_id].discard(websocket)
        
        if not self.active_connections[room_id]:
          del self.active_connections[room_id]
          
      return {
        "data": None
      }
    except Exception as exc:
        raise AppException.classify_error(exc)
      
  async def broadcast(self, chat_room_id: str, db: Session, message_data: ChatRoomMessageSchema) -> APIResponse[None]:
    try:
      print(self.active_connections.keys())
      print(self.active_connections.values())
      print("lkj")
      connections: set[WebSocket] = self.active_connections.get(chat_room_id, set())
      print(connections)
  
      # message = ChatRoomMessageModel(**message_data.model_dump())
      # message.chat_room_id = chat_room_id
      # db.add(message)
      # db.commit()
      
      for connection in list(connections):  # Copy list to avoid modification during iteration
        if connection.client_state == WebSocketState.CONNECTED: 
            print("yolo - sending message")
            try:
                await connection.send_text("test")
                await connection.send_json(message_data.model_dump())  
            except Exception as exc:
                print(f"Error sending message: {exc}")
                connections.remove(connection)  # Cleanup bad connection
        else:
            print(f"Removing stale WebSocket: {connection}")
            connections.remove(connection)  # Remove before attempting send

      
      return {
        "data": None
      }
    except Exception as exc:
      # await self.disconnect(chat_room_id, connection)
      raise AppException.classify_error(exc)