import os


class Config:
  PORT: int = int(os.getenv("PORT", 9000))
  HOST: str = os.getenv("HOST", "localhost")
  ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
