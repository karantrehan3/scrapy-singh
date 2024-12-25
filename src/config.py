from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH_TOKEN: str
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    SERVER_PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
