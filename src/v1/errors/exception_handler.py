import json

from fastapi import Response

from v1.type_defs import ERROR_STATUS_CODES, ErrorResponse

from .exception import AppException


class ExceptionHandler:

  @staticmethod
  def handle_error(exc: AppException) -> Response:
    status_code = ERROR_STATUS_CODES.get(exc.type, 500)
    error_response = ErrorResponse(
        error={
            "type": exc.type.name,
            "detail": exc.detail})

    return Response(
        content=json.dumps(error_response),
        media_type="application/json",
        status_code=status_code
    )
