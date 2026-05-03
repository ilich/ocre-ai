import pytest

from app.core.settings import Settings


def test_cors_origins_default() -> None:
    settings = Settings()
    assert settings.cors_origins == "*"


def test_cors_origins_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "https://example.com")
    settings = Settings()
    assert settings.cors_origins == "https://example.com"


def test_cors_origins_env_overrides_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "https://a.com,https://b.com")
    settings = Settings()
    assert settings.cors_origins == "https://a.com,https://b.com"
