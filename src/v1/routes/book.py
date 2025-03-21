from fastapi import APIRouter

from v1.controllers import BookController
from v1.docs import get_responses
from v1.schemas import BookSchema
from v1.type_defs import BaseResponse, CreateData, APIResponse


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
    
    self.router.add_api_route(
      path="/books/{book_id}",
      endpoint=self.controller.get_book,
      methods=["GET"],
      description="Get a book by ID",
      responses=get_responses(200, 404),
      response_model=APIResponse[BookSchema]
    )

    self.router.add_api_route(
      path="/books",
      endpoint=self.controller.list_books,
      methods=["GET"],
      description="List books (paginated)",
      responses=get_responses(200, 400, 500),
      response_model=APIResponse[list[BookSchema]]
    )

    self.router.add_api_route(
      path="/books/{book_id}",
      endpoint=self.controller.soft_delete_book,
      methods=["DELETE"],
      description="Soft delete a book",
      responses=get_responses(200, 404, 500),
      response_model=BaseResponse[str]
    )

    self.router.add_api_route(
      path="/books/{book_id}/restore",
      endpoint=self.controller.restore_book,
      methods=["PATCH"],
      description="Restore a soft-deleted book",
      responses=get_responses(200, 404, 500),
      response_model=BaseResponse[str]
    )
