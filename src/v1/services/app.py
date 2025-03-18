import time

from settings import INIT_START_TIME
from v1.errors import AppException
from v1.type_defs import APIResponse, HealthCheckData


class AppService:
  def __init__(self) -> None:
    self.init_start_time = INIT_START_TIME

  def _get_uptime(self) -> str:
    uptime_seconds = int(time.time() - self.init_start_time)
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

  def health_check(self) -> APIResponse[HealthCheckData]:
    try:
      uptime_str = self._get_uptime()

      return {
          "data": {
              "status": "OK",
              "uptime": uptime_str
          }
      }
    except Exception as exc:
      raise AppException.classify_error(error=exc)
