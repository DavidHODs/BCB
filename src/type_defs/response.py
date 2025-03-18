from typing_extensions import Generic, NotRequired, TypedDict, TypeVar

T = TypeVar("T")


class Metadata(TypedDict):
  total: int
  count: int
  page: int


class APIResponse(TypedDict, Generic[T]):
  data: T
  metadata: NotRequired[Metadata]


class HealthCheckData(TypedDict):
  status: str
  uptime: str
