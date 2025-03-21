from fastapi import APIRouter

from v1.controllers import BookController
from v1.docs import get_responses
from v1.schemas import BookSchema
from v1.type_defs import APIResponse, BaseResponse, CreateData


class BookRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = BookController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/books",
        endpoint=self.controller.create,
        methods=["POST"],
        description="Create new book",
        responses=get_responses(200, 400, 500),
        response_model=BaseResponse[CreateData]
    )

    self.router.add_api_route(
        path="/books/search",
        endpoint=self.controller.search,
        methods=["GET"],
        description="Search books in DB (optionally fetch from Gutendex)",
        responses=get_responses(200, 400, 500),
        response_model=APIResponse[list[BookSchema]]
    )

    self.router.add_api_route(
        path="/books/{id}",
        endpoint=self.controller.getOne,
        methods=["GET"],
        description="Get a book by ID",
        responses=get_responses(200, 404, 500),
        response_model=APIResponse[BookSchema]
    )

    self.router.add_api_route(
        path="/books",
        endpoint=self.controller.getAll,
        methods=["GET"],
        description="List books (paginated)",
        responses=get_responses(200, 400, 500),
        response_model=APIResponse[list[BookSchema]]
    )

    self.router.add_api_route(
        path="/books/{id}",
        endpoint=self.controller.delete,
        methods=["DELETE"],
        description="Soft delete a book",
        responses=get_responses(200, 404, 500),
        response_model=BaseResponse[str]
    )

    self.router.add_api_route(
        path="/books/{id}/restore",
        endpoint=self.controller.restore,
        methods=["PATCH"],
        description="Restore a soft-deleted book",
        responses=get_responses(200, 404, 500),
        response_model=BaseResponse[str]
    )
