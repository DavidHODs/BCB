import uuid

from sqlalchemy import JSON, TIMESTAMP, Column, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class BookModel(Base):
  __tablename__ = "books"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  title = Column(String, nullable=False)
  authors = Column(JSON, nullable=False)
  summaries = Column(JSON, nullable=True)
  translators = Column(JSON, nullable=True)
  subjects = Column(JSON, nullable=True)
  bookshelves = Column(JSON, nullable=True)
  languages = Column(JSON, nullable=False)
  created_at = Column(
      TIMESTAMP(
          timezone=True),
      server_default=func.now(),
      nullable=False)
  updated_at = Column(
      TIMESTAMP(
          timezone=True),
      server_default=func.now(),
      onupdate=func.now(),
      nullable=True)
  deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
  
  __table_args__ = (
    UniqueConstraint("title", "authors", name="uq_books_title_authors"),
  )
