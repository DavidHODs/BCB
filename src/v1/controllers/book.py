import uuid
from fastapi import Depends, Response
from sqlalchemy.orm import Session

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.models import BookModel
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
    
  async def get_book(self, book_id: uuid.UUID, db: Session = Depends(get_db)) -> APIResponse[BookModel] | Response:
    try:
      return self.book_service.get_book_by_id(book_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def list_books(self, page: int = 1, limit: int = 15, db: Session = Depends(get_db)) -> APIResponse[list[BookModel]] | Response:
    try:
      return self.book_service.list_books(page, limit, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def soft_delete_book(self, book_id: uuid.UUID, db: Session = Depends(get_db)) -> APIResponse[str] | Response:
    try:
      return self.book_service.soft_delete_book(book_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def restore_book(self, book_id: uuid.UUID, db: Session = Depends(get_db)) -> APIResponse[str] | Response:
    try:
      return self.book_service.restore_book(book_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
