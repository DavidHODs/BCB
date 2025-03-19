import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing_extensions import Any

from v1.errors import AppException
from v1.models import BookModel
from v1.type_defs import APIResponse, CreateData


class BookService:
  def create_book(self, book_data: dict[str, Any],
                  db: Session) -> APIResponse[CreateData]:
    try:
      book = BookModel(**book_data)
      db.add(book)
      db.commit()
      db.refresh(book)

      return {
          "data": {
              "id": uuid.UUID(str(book.id)),
              "message": f"{book.title} created successfully"
          }
      }

    except (SQLAlchemyError, Exception) as exc:
      db.rollback()
      raise AppException.classify_error(exc)
