from enum import Enum

from typing_extensions import Dict


class ErrorTypeEnum(str, Enum):
  UNAUTHORIZED = "UNAUTHORIZED"
  NOT_FOUND = "NOT_FOUND"
  BAD_REQUEST = "BAD_REQUEST"
  INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
  DATABASE_ERROR = "DATABASE_ERROR"
  VALIDATION_ERROR = "VALIDATION_ERROR"
  RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
  REQUEST_TIMEOUT = "REQUEST_TIMEOUT"


ERROR_STATUS_CODES: Dict[ErrorTypeEnum, int] = {
    ErrorTypeEnum.BAD_REQUEST: 400,
    ErrorTypeEnum.UNAUTHORIZED: 401,
    ErrorTypeEnum.NOT_FOUND: 404,
    ErrorTypeEnum.REQUEST_TIMEOUT: 408,
    ErrorTypeEnum.RESOURCE_CONFLICT: 409,
    ErrorTypeEnum.VALIDATION_ERROR: 422,
    ErrorTypeEnum.DATABASE_ERROR: 500,
    ErrorTypeEnum.INTERNAL_SERVER_ERROR: 500,
}

ERROR_TYPE_DEFAULTS: Dict[ErrorTypeEnum, str] = {
    ErrorTypeEnum.VALIDATION_ERROR: "Validation failed for the provided data.",
    ErrorTypeEnum.BAD_REQUEST: "The request was missing required parameters.",
    ErrorTypeEnum.NOT_FOUND: "The requested resource could not be found.",
    ErrorTypeEnum.DATABASE_ERROR: "A database related error occurred.",
    ErrorTypeEnum.UNAUTHORIZED: "You do not have the necessary permissions.",
    ErrorTypeEnum.RESOURCE_CONFLICT: "A conflict occurred, preventing the operation.",
    ErrorTypeEnum.INTERNAL_SERVER_ERROR: "An unexpected error occurred. Please try again later.",
    ErrorTypeEnum.REQUEST_TIMEOUT: "The request timed out.",
}
