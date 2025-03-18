from typing_extensions import Any, Dict, Union

from v1.type_defs import ERROR_STATUS_CODES, ErrorResponse

SUCCESS_RESPONSES: Dict[int, Dict[str, Any]] = {
    200: {"description": "OK"},
    201: {"description": "Resource Created"},
}

ERROR_RESPONSES: Dict[int, Dict[str, Any]] = {
    status_code: {
        "description": error_type,
        "model": ErrorResponse
    }
    for error_type, status_code in ERROR_STATUS_CODES.items()
}


def get_responses(*status_codes: int) -> Dict[Union[int, str], Dict[str, Any]]:
  responses: Dict[Union[int, str], Dict[str, Any]] = {}

  for code in status_codes:
    if code in SUCCESS_RESPONSES:
      responses[code] = SUCCESS_RESPONSES[code]

    if code in ERROR_RESPONSES:
      responses[code] = ERROR_RESPONSES[code]

  return responses
