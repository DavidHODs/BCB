from typing import Generic, NotRequired, TypedDict, TypeVar

T = TypeVar("T")


class MetaData(TypedDict):
  total: int
  count: int
  page: int


class ServiceResponse(TypedDict, Generic[T]):
  data: T
  metadata: NotRequired[MetaData]
