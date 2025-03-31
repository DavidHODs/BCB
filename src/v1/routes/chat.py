from fastapi import APIRouter, WebSocket

from v1.controllers import ChatController
from v1.docs import get_responses
from v1.schemas import ChatRoomSchema, ChatRoomMessageSchema
from v1.type_defs import APIResponse, BaseResponse, CreateData
from v1.models import ChatRoomMessageModel


class ChatRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = ChatController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
      path="/chat/rooms",
      endpoint=self.controller.create_room,
      methods=["POST"],
      description="Create a new chat room",
      responses=get_responses(200, 400, 500),
      response_model=BaseResponse[CreateData]
    )

    self.router.add_api_websocket_route(
      path="/chat/rooms/{chat_room_id}/ws",
      endpoint=self.controller.connect
    )

    self.router.add_api_route(
      path="/chat/rooms/{chat_room_id}/disconnect",
      endpoint=self.controller.disconnect,
      methods=["DELETE"],
      description="Disconnect from a chat room",
      responses=get_responses(200, 400, 500),
      response_model=BaseResponse[str]
    )

    self.router.add_api_route(
      path="/chat/rooms/{chat_room_id}/broadcast",
      endpoint=self.controller.broadcast,
      methods=["POST"],
      description="Broadcast a message to all connected clients in a chat room",
      responses=get_responses(200, 400, 500),
      response_model=BaseResponse[str]
    )