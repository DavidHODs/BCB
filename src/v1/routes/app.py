from fastapi import APIRouter

from v1.controllers import AppController
from v1.docs import get_responses
from v1.type_defs import BaseResponse, HealthCheckData


class AppRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = AppController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/health-check",
        endpoint=self.controller.health_check,
        methods=["GET"],
        description="Tests server health",
        responses=get_responses(200, 500),
        response_model=BaseResponse[HealthCheckData]
    )
