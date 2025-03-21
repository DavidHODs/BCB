import datetime
import time
import uuid

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing_extensions import Any

from v1.errors import AppException
from v1.models import BookModel
from v1.type_defs import APIResponse, CreateData, ErrorTypeEnum


class BookService:
  def create(self, book_data: dict[str, Any],
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
    
  def getOne(self, id: uuid.UUID, db: Session) -> APIResponse[BookModel]:
    try: 
      book = db.query(BookModel).filter(
          BookModel.id == id,
          BookModel.deleted_at.is_(None)
      ).first()
      
      if not book:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)
      
      return {
        "data": book
      }
    except Exception as exc:
      raise AppException.classify_error(exc)
      

  def getAll(self, page: int, limit: int, db: Session) -> APIResponse[list[BookModel]]:
    try:
      query = db.query(BookModel).filter(BookModel.deleted_at.is_(None))
    
      total = query.count()
      books = query.offset((page - 1) * limit).limit(limit).all()

      return {
          "data": books,
          "metadata": {
            "total": total,
            "count": len(books),
            "page": page
          }
      }
    
    except Exception as exc:
      raise AppException.classify_error(exc)

  def delete(self, id: uuid.UUID, db: Session) -> APIResponse[str]:
    try: 
      book = db.query(BookModel).filter(
          BookModel.id == id,
          BookModel.deleted_at.is_(None)
      ).first()
      
      if not book:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      db.query(BookModel).filter(
          BookModel.id == id
      ).update({"deleted_at": datetime.datetime.now()})
      db.commit()
      
      return {
        "data": "Book soft deleted"
      }
    
    except Exception as exc:
      raise AppException.classify_error(exc)

  def restore(self, id: uuid.UUID, db: Session) -> APIResponse[str]:
    try:
      book = db.query(BookModel).filter(
          BookModel.id == id,
          BookModel.deleted_at.is_not(None)
      ).first()
      
      if not book:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      db.query(BookModel).filter(
          BookModel.id == id
      ).update({"deleted_at": None})
      db.commit()
      
      return {
        "data": "Book restored successfully"
      }
    except Exception as exc:
      raise AppException.classify_error(exc)
