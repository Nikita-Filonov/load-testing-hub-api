from functools import lru_cache

from pydantic import Field, SecretStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseClientConfig(BaseSettings):
    port: int = Field(default=5432, env="PORT")
    host: str = Field(default="", env="HOST")
    driver: str = Field(default="postgresql+asyncpg", env="DRIVER")
    database: str = Field(default="", env="DATABASE")
    username: str = Field(default="", env="USERNAME")
    password: SecretStr = Field(default="", env="PASSWORD")

    @property
    def postgres_url(self) -> str:
        return f"{self.driver}://{self.username}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    app_name: str = Field(default="Load testing metrics API", env="APP_NAME")
    app_logo_path: str = Field(default="/static/logo.png", env="APP_LOGO_PATH")

    postgres: DatabaseClientConfig = DatabaseClientConfig()

    kibana_url: HttpUrl = Field(env="KIBANA_URL")
    grafana_url: HttpUrl = Field(env="GRAFANA_URL")


@lru_cache
def get_settings() -> Settings:
    return Settings()
