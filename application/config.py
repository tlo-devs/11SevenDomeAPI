from pathlib import Path

from pydantic import BaseSettings

from functools import lru_cache


class Config(BaseSettings):
    app_name: str = "11SevenPortfolio"
    app_version: str = "0.1.0"

    database_uri: str = "sqlite:///../data.db"

    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        allow_mutation = False


@lru_cache
def get_config() -> Config:
    return Config()


__all__ = ["Config", "get_config"]
