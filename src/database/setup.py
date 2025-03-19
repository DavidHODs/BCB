from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings.config import Config

DATABASE_URL = (
    f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}"
    f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_DATABASE}"
)

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(bind=engine, autoflush=True)
