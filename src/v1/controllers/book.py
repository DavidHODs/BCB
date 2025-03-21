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

  async def create(self, book_data: BookSchema, db: Session = Depends(
          get_db)) -> APIResponse[CreateData] | Response:
    try:
      payload = book_data.model_dump()
      return self.book_service.create(payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def getOne(self, id: uuid.UUID, db: Session = Depends(
          get_db)) -> APIResponse[BookModel] | Response:
    try:
      return self.book_service.getOne(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def getAll(self, page: int = 1, limit: int = 15, db: Session = Depends(
          get_db)) -> APIResponse[list[BookModel]] | Response:
    try:
      return self.book_service.getAll(page, limit, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def delete(self, id: uuid.UUID, db: Session = Depends(
          get_db)) -> APIResponse[str] | Response:
    try:
      return self.book_service.delete(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def restore(self, id: uuid.UUID, db: Session = Depends(
          get_db)) -> APIResponse[str] | Response:
    try:
      return self.book_service.restore(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  async def search(self, query: str, page: int = 1, limit: int = 15, gutendex: bool = False,
                   db: Session = Depends(get_db)) -> APIResponse[list[BookModel]] | Response:
    try:
      return await self.book_service.search(query, page, limit, db, gutendex)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
