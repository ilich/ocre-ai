from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import jwt
from argon2 import PasswordHasher
from beanie import PydanticObjectId
from fastapi.testclient import TestClient

from app.core.settings import Settings, get_settings
from app.main import app
from app.services.authentication import ALGORITHM
from app.services.user_repository import UserRepository, get_user_repository

client = TestClient(app, raise_server_exceptions=False)

VALID_PASSWORD = "SecureP@ss1"
TEST_SECRET_KEY = "test-secret-key-with-at-least-32-bytes"
FAKE_USER_ID = PydanticObjectId("507f1f77bcf86cd799439011")


def _settings() -> Settings:
    return Settings(
        mongodb_uri="mongodb://localhost:27017",
        mongodb_database="ocre-ai-test",
        secret_key=TEST_SECRET_KEY,
    )


def _user(email: str = "user@example.com", full_name: str = "Jane Doe", password: str | None = None) -> SimpleNamespace:
    return SimpleNamespace(id=FAKE_USER_ID, email=email, full_name=full_name, password=password)


def _mock_user_repository(current_user: object | None = None) -> MagicMock:
    repository = MagicMock(spec=UserRepository)
    repository.get_user_by_id = AsyncMock(return_value=current_user)
    repository.update_user = AsyncMock(return_value=None)
    return repository


def _override_user_repository(repository: object) -> None:
    app.dependency_overrides[get_user_repository] = lambda: repository
    app.dependency_overrides[get_settings] = _settings


def _access_token(user_id: str = str(FAKE_USER_ID)) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=30)
    return jwt.encode({"user_id": user_id, "exp": expiration}, TEST_SECRET_KEY, algorithm=ALGORITHM)


# --- GET /user/me ---
# Requirements:
#   - An authenticated user receives 200 with their id, email, and full_name
#   - An unauthenticated request returns 401


def test_get_me_returns_user_details() -> None:
    repository = _mock_user_repository(current_user=_user())
    _override_user_repository(repository)
    try:
        response = client.get("/user/me", headers={"Authorization": f"Bearer {_access_token()}"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "id": str(FAKE_USER_ID),
        "email": "user@example.com",
        "full_name": "Jane Doe",
    }
    repository.get_user_by_id.assert_awaited_once_with(str(FAKE_USER_ID))


def test_get_me_unauthenticated_returns_401() -> None:
    response = client.get("/user/me")
    assert response.status_code == 401


def test_get_me_unknown_user_returns_401() -> None:
    repository = _mock_user_repository(current_user=None)
    _override_user_repository(repository)
    try:
        response = client.get("/user/me", headers={"Authorization": f"Bearer {_access_token()}"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    repository.get_user_by_id.assert_awaited_once_with(str(FAKE_USER_ID))


def test_get_me_invalid_token_returns_401() -> None:
    repository = _mock_user_repository(current_user=_user())
    _override_user_repository(repository)
    try:
        response = client.get("/user/me", headers={"Authorization": "Bearer invalid-token"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    repository.get_user_by_id.assert_not_called()


# --- POST /user/change-password ---
# Requirements:
#   - Correct old password and a strong new password return 200 with success=True
#   - A wrong old password returns 400
#   - New password must satisfy the password policy (422)
#   - An unauthenticated request returns 401
#   - old_password and new_password are required fields (422)


def test_change_password_returns_ok() -> None:
    ph = PasswordHasher()
    user = _user(password=ph.hash("OldP@ssw0rd"))
    repository = _mock_user_repository(current_user=user)
    _override_user_repository(repository)
    try:
        response = client.post(
            "/user/change-password",
            json={"old_password": "OldP@ssw0rd", "new_password": VALID_PASSWORD},
            headers={"Authorization": f"Bearer {_access_token()}"},
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_change_password_wrong_old_password_returns_400() -> None:
    ph = PasswordHasher()
    user = _user(password=ph.hash("OldP@ssw0rd"))
    repository = _mock_user_repository(current_user=user)
    _override_user_repository(repository)
    try:
        response = client.post(
            "/user/change-password",
            json={"old_password": "WrongP@ssw0rd", "new_password": VALID_PASSWORD},
            headers={"Authorization": f"Bearer {_access_token()}"},
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 400


def test_change_password_weak_new_password_returns_422() -> None:
    repository = _mock_user_repository(current_user=_user())
    _override_user_repository(repository)
    try:
        response = client.post(
            "/user/change-password",
            json={"old_password": "OldP@ssw0rd", "new_password": "weak"},
            headers={"Authorization": f"Bearer {_access_token()}"},
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 422


def test_change_password_unauthenticated_returns_401() -> None:
    response = client.post(
        "/user/change-password",
        json={"old_password": "OldP@ssw0rd", "new_password": VALID_PASSWORD},
    )
    assert response.status_code == 401


def test_change_password_missing_old_password_returns_422() -> None:
    repository = _mock_user_repository(current_user=_user())
    _override_user_repository(repository)
    try:
        response = client.post(
            "/user/change-password",
            json={"new_password": VALID_PASSWORD},
            headers={"Authorization": f"Bearer {_access_token()}"},
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 422


def test_change_password_missing_new_password_returns_422() -> None:
    repository = _mock_user_repository(current_user=_user())
    _override_user_repository(repository)
    try:
        response = client.post(
            "/user/change-password",
            json={"old_password": "OldP@ssw0rd"},
            headers={"Authorization": f"Bearer {_access_token()}"},
        )
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 422
