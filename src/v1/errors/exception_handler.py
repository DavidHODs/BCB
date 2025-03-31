import json

from fastapi import Response

from v1.type_defs import ERROR_STATUS_CODES, ErrorResponse
from src.settings import Config
from v1.type_defs import ErrorTypeEnum, ERROR_TYPE_DEFAULTS

from .exception import AppException


class ExceptionHandler:

  @staticmethod
  def handle_error(exc: AppException) -> Response:
    status_code = ERROR_STATUS_CODES.get(exc.type, 500)
    
    if Config.isProd and exc.type in { ErrorTypeEnum.INTERNAL_SERVER_ERROR, ErrorTypeEnum.DATABASE_ERROR }:
      exc.detail = ERROR_TYPE_DEFAULTS.get(exc.type, "An unexpected error occurred.")
    else:
      exc.detail = exc.detail
            
    error_response = ErrorResponse(
        error={
            "type": exc.type.name,
            "detail": exc.detail})

    return Response(
        content=json.dumps(error_response),
        media_type="application/json",
        status_code=status_code
    )
