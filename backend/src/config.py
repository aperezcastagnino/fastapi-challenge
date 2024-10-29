from enum import Enum

from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class Settings(BaseSettings):
    database_url: str = "sqlite:///./database.db"
    log_level: LogLevel = LogLevel.info
    server_url: str

    access_token_expire_minutes: float
    jwt_signing_key: str


settings = Settings()
