from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cors_origins: str = "*"
    mongodb_uri: str
    mongodb_database: str

    model_config = SettingsConfigDict(env_file=".env")
