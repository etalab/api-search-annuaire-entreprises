from pathlib import Path
from typing import Any, Dict

from pydantic import AnyHttpUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ElasticConfig(BaseSettings):
    password: SecretStr = Field(...)
    user: str = Field(...)
    url: AnyHttpUrl = Field(...)


class SentryConfig(BaseSettings):
    dsn: str = Field(...)


class APMConfig(BaseSettings):
    url: AnyHttpUrl = Field(...)
    service_name: str = Field("SEARCH APM")


class DocsConfig(BaseSettings):
    path: Path = Field(
        default_factory=lambda: Path(__file__).parent / "doc" / "open-api.yml"
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="_",
    )

    elastic: ElasticConfig
    sentry: SentryConfig
    apm: APMConfig
    openapi: DocsConfig = DocsConfig()
    env: str = Field(...)

    @property
    def apm_config(self) -> Dict[str, Any]:
        return {
            "SERVICE_NAME": self.apm.service_name,
            "SERVER_URL": self.apm.url,
            "ENVIRONMENT": self.env,
        }


settings = Settings()
