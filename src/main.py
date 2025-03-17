import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from type_defs import APIResponse, UvicornKwargs

load_dotenv(dotenv_path=".env")

app: FastAPI = FastAPI(title="Book Club API")

port: int = int(os.getenv(key="PORT", default=9000))
host: str = os.getenv(key="HOST", default="localhost")
env: str = os.getenv(key="ENVIRONMENT", default="development")


@app.get("/")
def root() -> APIResponse[str]:
  return {
      "data": "Welcome to book club api",
      "metadata": {
          "total": 50,
          "count": 15,
          "page": 1
      }
  }


if __name__ == "__main__":
  uvicorn_kwargs: UvicornKwargs = {
      "host": host,
      "port": port,
      "reload": env == "development"
  }

  print(f"app running at {host}:{port}")
  uvicorn.run("src.main:app", **uvicorn_kwargs)
