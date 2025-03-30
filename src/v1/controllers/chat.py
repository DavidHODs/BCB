import uuid
from fastapi import Depends, Response, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.schemas import ChatRoomSchema, ChatRoomMessageSchema, ChatMessagePayloadSchema
from v1.services import ChatService
from v1.type_defs import APIResponse, CreateData
from v1.models import ChatRoomMessageModel


class ChatController:
  def __init__(self) -> None:
    self.chat_service = ChatService()

  async def create_room(self, chat_data: ChatRoomSchema, db: AsyncSession = Depends(get_db)) -> APIResponse[CreateData] | Response:
    try:
      return await self.chat_service.create_room(db, chat_data)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def save_message(self, message_data: ChatRoomMessageSchema, db: AsyncSession = Depends(get_db)) -> APIResponse[ChatRoomMessageModel] | Response:
    try:
      return await self.chat_service.save_message(db, message_data)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def get_previous_messages(self, chat_room_id: str, page: int = 1, limit: int = 15, db: AsyncSession = Depends(get_db)) -> APIResponse[list[ChatRoomMessageModel]] | Response:
    try:
      return await self.chat_service.get_previous_messages(db, chat_room_id, limit, page)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def connect(self, room_id: str, websocket: WebSocket) -> APIResponse[None] | Response:
    try:
      return await self.chat_service.connect(room_id, websocket)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def disconnect(self, room_id: str, websocket: WebSocket) -> APIResponse[None] | Response:
    try:
      return await self.chat_service.disconnect(room_id, websocket)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def broadcast(self, room_id: str, payload: ChatMessagePayloadSchema) -> APIResponse[None] | Response:
    try:
      return await self.chat_service.broadcast(room_id, payload)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
