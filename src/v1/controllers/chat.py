import uuid
from fastapi import Depends, Response, WebSocket
from sqlalchemy.orm import Session

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.schemas import ChatRoomSchema, ChatRoomMessageSchema
from v1.services import ChatService
from v1.type_defs import APIResponse, CreateData
from v1.models import ChatRoomMessageModel


class ChatController:
  def __init__(self) -> None:
    self.chat_service = ChatService()

  def create_room(self, chat_data: ChatRoomSchema, db: Session = Depends(get_db)) -> APIResponse[CreateData] | Response:
    try:
      return self.chat_service.create_room(db, chat_data)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def connect(self, websocket: WebSocket, chat_room_id: str) -> str | Response:
    try:
      return await self.chat_service.connect(websocket, chat_room_id)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def disconnect(self, chat_room_id: str, websocket: WebSocket) -> APIResponse[str] | Response:
    try:
      return self.chat_service.disconnect(chat_room_id, websocket)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def broadcast(self, chat_room_id: str, payload: ChatRoomMessageSchema, db: Session = Depends(get_db)) -> APIResponse[str] | Response:
    try:
      return await self.chat_service.broadcast(db, chat_room_id, payload)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
