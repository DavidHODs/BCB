from sqlalchemy.exc import SQLAlchemyError
from typing_extensions import Any, Optional

from v1.type_defs import ERROR_TYPE_DEFAULTS, ErrorTypeEnum


class AppException(Exception):
  def __init__(self, type: ErrorTypeEnum, detail: Optional[str] = None) -> None:
    self.type = type
    self.detail = detail or ERROR_TYPE_DEFAULTS[type]

  @staticmethod
  def classify_error(error: Any) -> "AppException":
    if isinstance(error, SQLAlchemyError):
      return AppException(type=ErrorTypeEnum.DATABASE_ERROR, detail=str(error))

    if isinstance(error, AppException):
      return error

    return AppException(
        type=ErrorTypeEnum.INTERNAL_SERVER_ERROR,
        detail=str(error),
    )
