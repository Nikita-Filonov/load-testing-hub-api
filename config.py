from functools import lru_cache

from pydantic import Field, SecretStr, HttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseClientConfig(BaseModel):
    port: int = Field(default=5432)
    host: str = Field(default="")
    driver: str = Field(default="postgresql+asyncpg")
    database: str = Field(default="")
    username: str = Field(default="")
    password: SecretStr = Field(default="")

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

    app_name: str = Field(default="Load testing hub API")
    app_logo_path: str = Field(default="/static/logo.png")

    postgres: DatabaseClientConfig = DatabaseClientConfig()

    kibana_url: HttpUrl | None = Field(default=None)
    grafana_url: HttpUrl | None = Field(default=None)
    kubernetes_url: HttpUrl | None = Field(default=None)


@lru_cache
def get_settings() -> Settings:
    return Settings()
