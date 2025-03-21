from uuid import UUID

from typing_extensions import Generic, NotRequired, TypedDict, TypeVar

T = TypeVar("T")


class Metadata(TypedDict):
  total: int
  count: int
  page: int


class APIResponse(TypedDict, Generic[T]):
  data: T
  metadata: NotRequired[Metadata]


class BaseResponse(TypedDict, Generic[T]):
  data: T


class HealthCheckData(TypedDict):
  status: str
  uptime: str


class ErrorShape(TypedDict):
  type: str
  detail: str


class ErrorResponse(TypedDict):
  error: ErrorShape


class CreateData(TypedDict):
  id: UUID
  message: str
