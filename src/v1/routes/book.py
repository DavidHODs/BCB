from fastapi import APIRouter

from v1.controllers import BookController
from v1.docs import get_responses
from v1.type_defs import BaseResponse, CreateData


class BookRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = BookController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/books",
        endpoint=self.controller.create_book,
        methods=["POST"],
        description="Create new book",
        responses=get_responses(200, 400, 500),
        response_model=BaseResponse[CreateData]
    )
