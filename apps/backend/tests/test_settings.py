import pytest

from app.core.settings import Settings, get_settings


def _settings() -> Settings:
    return Settings(
        mongodb_uri="mongodb://localhost:27017",
        mongodb_database="ocre-ai-test",
        secret_key="test-secret",
    )


def test_cors_origins_default() -> None:
    settings = _settings()
    assert settings.cors_origins == "*"


def test_cors_origins_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "https://example.com")
    monkeypatch.setenv("MONGODB_URI", "mongodb://localhost:27017")
    monkeypatch.setenv("MONGODB_DATABASE", "ocre-ai-test")
    monkeypatch.setenv("SECRET_KEY", "test-secret")

    settings = Settings()
    assert settings.cors_origins == "https://example.com"


def test_cors_origins_env_overrides_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "https://a.com,https://b.com")
    monkeypatch.setenv("MONGODB_URI", "mongodb://localhost:27017")
    monkeypatch.setenv("MONGODB_DATABASE", "ocre-ai-test")
    monkeypatch.setenv("SECRET_KEY", "test-secret")

    settings = Settings()
    assert settings.cors_origins == "https://a.com,https://b.com"


def test_get_settings_loads_dependency_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "https://api.example.com")
    monkeypatch.setenv("MONGODB_URI", "mongodb://localhost:27017")
    monkeypatch.setenv("MONGODB_DATABASE", "ocre-ai-test")
    monkeypatch.setenv("SECRET_KEY", "test-secret")

    settings = get_settings()

    assert settings.cors_origins == "https://api.example.com"
    assert settings.mongodb_uri == "mongodb://localhost:27017"
    assert settings.mongodb_database == "ocre-ai-test"
    assert settings.secret_key == "test-secret"
