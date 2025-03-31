import uuid
from typing import List, Optional

from pydantic import BaseModel


class PersonSchema(BaseModel):
  name: str
  birth_year: Optional[int] = None
  death_year: Optional[int] = None


class BookSchema(BaseModel):
  id: Optional[uuid.UUID]
  title: str
  authors: List[PersonSchema]
  summaries: Optional[List[str]]
  translators: Optional[List[PersonSchema]]
  bookshelves: Optional[List[str]]
  languages: List[str]
