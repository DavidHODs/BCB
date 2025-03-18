from fastapi import Response

from v1.errors import AppException, ExceptionHandler
from v1.services import AppService
from v1.type_defs import APIResponse, HealthCheckData


class AppController:
  def __init__(self) -> None:
    self.app_service: AppService = AppService()

  def health_check(self) -> APIResponse[HealthCheckData] | Response:
    try:
      return self.app_service.health_check()
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
