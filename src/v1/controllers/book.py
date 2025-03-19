from fastapi import Depends, Response
from sqlalchemy.orm import Session

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.schemas import BookSchema
from v1.services import BookService
from v1.type_defs import APIResponse, CreateData


class BookController:
  def __init__(self) -> None:
    self.book_service = BookService()

  async def create_book(self, book_data: BookSchema, db: Session = Depends(
          get_db)) -> APIResponse[CreateData] | Response:
    try:
      payload = book_data.model_dump()
      return self.book_service.create_book(payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
