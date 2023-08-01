from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    __slots__ = ()

    ENV: Literal["dev", "prod"] = "dev"
    DEBUG: bool = True
    APP_TITLE: str = "Task Manager"
    APP_DESCRIPTION: str = "Task Manager API"
    APP_PORT: int = 5000
    SECRET_KEY: str = "secret"

    # JWT
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # DATABASE
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = 5432
    POSTGRES_DB: str = "task_manager"

    # DATABASE URL
    @property
    def DATABASE_URI(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def ALEMBIC_URI(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
