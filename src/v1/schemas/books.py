from typing import Optional

from pydantic import BaseModel


class BookSchema(BaseModel):
  title: str
  authors: list[str]
  summaries: Optional[list[str]]
  translators: Optional[list[str]]
  subjects: Optional[list[str]]
  bookshelves: Optional[list[str]]
  languages: list[str]
