import os


class Config:
  PORT: int = int(os.getenv("PORT", 9000))
  HOST: str = os.getenv("HOST", "localhost")
  ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

  DB_PORT: int = int(os.getenv("DB_PORT", 5432))
  DB_DATABASE: str = os.getenv("DB_DATABASE", "bcb")
  DB_USER: str = os.getenv("DB_USER", "")
  DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
  DB_HOST: str = os.getenv("DB_HOST", "localhost")

  SUPER_ADMIN_NAME: str = os.getenv("SUPER_ADMIN_NAME", "")
  SUPER_ADMIN_PASSWORD: str = os.getenv("SUPER_ADMIN_PASSWORD", "")
  SUPER_ADMIN_EMAIL: str = os.getenv("SUPER_ADMIN_EMAIL", "")
