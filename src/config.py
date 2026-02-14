from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

config = SettingsConfigDict(
    env_file="../.env", env_file_encoding="utf-8", extra="ignore"
)


class SMTPSettings(BaseSettings):
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_username: str = "user"
    smtp_password: str = "password"
    smtp_use_tls: bool = True

    model_config = config


class SecuritySettings(BaseSettings):
    """Security configuration for API authentication and rate limiting."""

    api_key: str = "changeme-generate-secure-key"
    cors_origins: list[str] = [""]
    rate_limit_requests: int = 10
    rate_limit_window: Literal["second", "minute", "hour", "day"] = "minute"
    enable_csrf: bool = True

    model_config = config


class Settings(BaseSettings):
    debug: bool = False
    smtp: SMTPSettings = SMTPSettings()
    security: SecuritySettings = SecuritySettings()

    email_recipient: str = ""
    email_sender: str = ""

    model_config = config


settings = Settings()
