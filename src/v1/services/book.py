import datetime
import uuid

import httpx
import sqlalchemy
from sqlalchemy import func, or_
from sqlalchemy.dialects.postgresql import insert
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

  def getAll(self, page: int, limit: int,
             db: Session) -> APIResponse[list[BookModel]]:
    try:
      query = db.query(BookModel).filter(BookModel.deleted_at.is_(None))

      total = query.count()
      books = query.offset((page - 1) * limit).limit(limit).all()

      return {
          "data": books if books else [],
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

  async def search(self, query: str, page: int, limit: int, db: Session,
                   gutendex: bool = False) -> APIResponse[list[BookModel]]:
    try:
      if gutendex:
        BASE_URL = "http://gutendex.com/books/"
        books_to_insert = []

        async with httpx.AsyncClient() as client:
          for page_num in range(1, 10):
            response = await client.get(BASE_URL, params={"page": page_num, "search": query})

            if response.status_code != 200:
              break

            data = response.json()
            results = data.get("results", [])

            for book in results:
              books_to_insert.append({
                  "title": book["title"],
                  "authors": book["authors"],
                  "summaries": book.get("summaries", []),
                  "translators": book.get("translators", []),
                  "subjects": book.get("subjects", []),
                  "bookshelves": book.get("bookshelves", []),
                  "languages": book.get("languages", []),
              })

            if not data.get("next"):
              break

        if books_to_insert:
          stmt = insert(BookModel).values(books_to_insert)
          stmt = stmt.on_conflict_do_nothing(
              index_elements=["title", "authors"])
          db.execute(stmt)
          db.commit()

      books_query = db.query(BookModel).filter(
          BookModel.deleted_at.is_(None),
          or_(
              BookModel.title.ilike(f"%{query}%"),
              func.cast(
                  BookModel.authors,
                  sqlalchemy.String).ilike(f"%{query}%")
          )
      )

      total = books_query.count()
      books = books_query.offset((page - 1) * limit).limit(limit).all()

      return {
          "data": books,
          "metadata": {
              "total": total,
              "count": len(books),
              "page": page
          }
      }

    except (SQLAlchemyError, Exception) as exc:
      db.rollback()
      raise AppException.classify_error(exc)