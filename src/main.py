from contextlib import asynccontextmanager
from psycopg import OperationalError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from typing_extensions import AsyncGenerator

from database import get_db
from settings import INIT_START_TIME, Config
from v1.routes import all_routes
from v1.type_defs import UvicornKwargs

load_dotenv(dotenv_path=".env")
INIT_START_TIME

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
  try:
      db = next(get_db())
      db.connection().execute(text("SELECT 1"))
      print("Database connection successful")
  except (OperationalError, SQLAlchemyError) as exc:
      print(f"Database connection failed: {exc}")
      exit(1)
  finally:
      db.close()
  yield  
  print("Shutting down application...")
  
app: FastAPI = FastAPI(lifespan=lifespan, title="Book Club API", version="1.0.0")

for router, tags in all_routes:
  app.include_router(router, prefix="/api/v1", tags=list(tags))

if __name__ == "__main__":
  uvicorn_kwargs: UvicornKwargs = {
      "host": Config.HOST,
      "port": Config.PORT,
      "reload": Config.ENVIRONMENT == "development"
  }

  print(f"app running at {Config.HOST}:{Config.PORT}")
  uvicorn.run("src.main:app", **uvicorn_kwargs)