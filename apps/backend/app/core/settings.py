from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cors_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env")
