import os
from typing import Dict

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from type_defs import UvicornKwargs

load_dotenv(dotenv_path=".env")

app: FastAPI = FastAPI(title="Book Club API")

port: int = int(os.getenv(key="PORT", default=9000))
host: str = os.getenv(key="HOST", default="localhost")
env: str = os.getenv(key="ENVIRONMENT", default="development")


@app.get("/")
def root() -> Dict[str, str]:
  return {
      "data": "Welcome to BCB API"
  }


if __name__ == "__main__":
  uvicorn_kwargs: UvicornKwargs = {
      "host": host,
      "port": port,
      "reload": env == "development"
  }

  print(f"app running at {host}:{port}")
  uvicorn.run("src.main:app", **uvicorn_kwargs)
