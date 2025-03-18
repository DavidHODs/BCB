import time

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, status

from settings import INIT_TIME, Config
from type_defs import APIResponse, HealthCheckData, UvicornKwargs

load_dotenv(dotenv_path=".env")

app: FastAPI = FastAPI(title="Book Club API")


@app.get("/health-check", status_code=status.HTTP_200_OK)
def root() -> APIResponse[HealthCheckData]:
  uptime_seconds = int(time.time() - INIT_TIME)

  days = uptime_seconds // 86400
  hours = (uptime_seconds % 86400) // 3600
  minutes = (uptime_seconds % 3600) // 60
  seconds = uptime_seconds % 60

  uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"

  return {
      "data": {
          "status": "OK",
          "uptime": uptime_str
      }
  }


if __name__ == "__main__":
  uvicorn_kwargs: UvicornKwargs = {
      "host": Config.HOST,
      "port": Config.PORT,
      "reload": Config.ENVIRONMENT == "development"
  }

  print(f"app running at {Config.HOST}:{Config.PORT}")
  uvicorn.run("src.main:app", **uvicorn_kwargs)
