from typing import TypedDict


class UvicornKwargs(TypedDict):
  host: str
  port: int
  reload: bool
