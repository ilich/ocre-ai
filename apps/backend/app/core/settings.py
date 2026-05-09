from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cors_origins: str = "*"
    mongodb_uri: str
    mongodb_database: str
    secret_key: str
    public_url: str
    email_from: str
    smtp_host: str
    smtp_port: int
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = False
    openai_api_key: str
    ai_model: str
    ai_embedding_model: str

    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    return Settings()
