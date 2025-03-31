from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text
from typing_extensions import Generator

from settings import Config

DATABASE_URL = (
    f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}"
    f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_DATABASE}"
)

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(bind=engine, autoflush=True)


def get_db() -> Generator[Session, None, None]:
  db = session_local()
  try:
    yield db
  finally:
    db.close()


def check_database() -> None:
  try:
    db = next(get_db())
    db.execute(text("SELECT 1"))
    print("Database connection successful")
  except SQLAlchemyError as e:
    print(f"Database connection failed: {e}")
    exit(1)
  finally:
    db.close()


def close_database() -> None:
  session_local().close_all()
