from typing import Optional
import uuid

from pydantic import BaseModel


class BookSchema(BaseModel):
  id: Optional[uuid.UUID]
  title: str
  authors: list[str]
  summaries: Optional[list[str]]
  translators: Optional[list[str]]
  subjects: Optional[list[str]]
  bookshelves: Optional[list[str]]
  languages: list[str]
