from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Config

DATABASE_URL = (
  f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}"
  f"@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_DATABASE}"
)
 

# Create the engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

emgine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=True)


