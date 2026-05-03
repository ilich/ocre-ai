from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from beanie import PydanticObjectId
from fastapi.testclient import TestClient

from app.main import app
from app.services.user_repository import UserRepository, get_user_repository

client = TestClient(app, raise_server_exceptions=False)

VALID_PASSWORD = "SecureP@ss1"
FAKE_USER_ID = PydanticObjectId("507f1f77bcf86cd799439011")


def _user(email: str = "new@example.com", full_name: str = "Jane Doe") -> SimpleNamespace:
    return SimpleNamespace(id=FAKE_USER_ID, email=email, full_name=full_name)


def _mock_user_repository(existing_user: object | None = None, created_user: object | None = None) -> MagicMock:
    repository = MagicMock(spec=UserRepository)
    repository.get_user_by_email = AsyncMock(return_value=existing_user)
    repository.create_user = AsyncMock(return_value=created_user or _user())
    return repository


def _override_user_repository(repository: object) -> None:
    app.dependency_overrides[get_user_repository] = lambda: repository


# --- POST /auth/sign-in ---
# Requirements:
#   - Valid credentials return 200 with access_token and token_type "bearer"
#   - Wrong credentials return 401
#   - Email must be a valid email address (422)
#   - login and password are required fields (422)


def test_sign_in_returns_access_token() -> None:
    response = client.post("/auth/sign-in", json={"login": "user@example.com", "password": VALID_PASSWORD})
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_sign_in_wrong_credentials_returns_401() -> None:
    response = client.post("/auth/sign-in", json={"login": "user@example.com", "password": "wrongpass"})
    assert response.status_code == 401


def test_sign_in_invalid_email_returns_422() -> None:
    response = client.post("/auth/sign-in", json={"login": "not-an-email", "password": VALID_PASSWORD})
    assert response.status_code == 422


def test_sign_in_missing_login_returns_422() -> None:
    response = client.post("/auth/sign-in", json={"password": VALID_PASSWORD})
    assert response.status_code == 422


def test_sign_in_missing_password_returns_422() -> None:
    response = client.post("/auth/sign-in", json={"login": "user@example.com"})
    assert response.status_code == 422


# --- POST /auth/sign-up ---
# Requirements:
#   - Valid data returns 201 with id, email, and full_name
#   - Registering with an already-taken email returns 409
#   - Email must be a valid email address (422)
#   - Password must satisfy the password policy (422)
#   - full_name must be at least 2 characters (422)
#   - email, password, and full_name are required fields (422)


def test_sign_up_returns_created_user() -> None:
    repository = _mock_user_repository(created_user=_user())
    _override_user_repository(repository)
    try:
        response = client.post(
            "/auth/sign-up",
            json={"email": "new@example.com", "password": VALID_PASSWORD, "full_name": "Jane Doe"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["id"] == str(FAKE_USER_ID)
    assert body["email"] == "new@example.com"
    assert body["full_name"] == "Jane Doe"
    assert body["message"] == "User registered successfully"


def test_sign_up_get_user_by_email_called_once() -> None:
    repository = _mock_user_repository()
    _override_user_repository(repository)
    try:
        client.post(
            "/auth/sign-up",
            json={"email": "new@example.com", "password": VALID_PASSWORD, "full_name": "Jane Doe"},
        )
    finally:
        app.dependency_overrides.clear()

    repository.get_user_by_email.assert_awaited_once_with("new@example.com")


def test_sign_up_create_user_not_called_on_duplicate_email() -> None:
    repository = _mock_user_repository(existing_user=_user(email="existing@example.com"))
    _override_user_repository(repository)
    try:
        client.post(
            "/auth/sign-up",
            json={"email": "existing@example.com", "password": VALID_PASSWORD, "full_name": "Jane Doe"},
        )
    finally:
        app.dependency_overrides.clear()

    repository.create_user.assert_not_called()


def test_sign_up_duplicate_email_returns_409() -> None:
    repository = _mock_user_repository(existing_user=_user(email="existing@example.com"))
    _override_user_repository(repository)
    try:
        response = client.post(
            "/auth/sign-up",
            json={"email": "existing@example.com", "password": VALID_PASSWORD, "full_name": "Jane Doe"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 409


def test_sign_up_invalid_email_returns_422() -> None:
    response = client.post(
        "/auth/sign-up",
        json={"email": "not-an-email", "password": VALID_PASSWORD, "full_name": "Jane Doe"},
    )
    assert response.status_code == 422


def test_sign_up_weak_password_returns_422() -> None:
    response = client.post(
        "/auth/sign-up",
        json={"email": "user@example.com", "password": "weak", "full_name": "Jane Doe"},
    )
    assert response.status_code == 422


def test_sign_up_missing_email_returns_422() -> None:
    response = client.post(
        "/auth/sign-up",
        json={"password": VALID_PASSWORD, "full_name": "Jane Doe"},
    )
    assert response.status_code == 422


def test_sign_up_missing_full_name_returns_422() -> None:
    response = client.post(
        "/auth/sign-up",
        json={"email": "user@example.com", "password": VALID_PASSWORD},
    )
    assert response.status_code == 422


def test_sign_up_full_name_too_short_returns_422() -> None:
    response = client.post(
        "/auth/sign-up",
        json={"email": "user@example.com", "password": VALID_PASSWORD, "full_name": "A"},
    )
    assert response.status_code == 422


def test_sign_up_missing_password_returns_422() -> None:
    response = client.post(
        "/auth/sign-up",
        json={"email": "user@example.com", "full_name": "Jane Doe"},
    )
    assert response.status_code == 422


# --- POST /auth/reset-password ---
# Requirements:
#   - Any valid email returns 200 with success=True (intentionally does not reveal whether the email exists)
#   - Invalid email format returns 422


def test_reset_password_returns_ok() -> None:
    response = client.post("/auth/reset-password", json={"email": "user@example.com"})
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_reset_password_unknown_email_still_returns_ok() -> None:
    response = client.post("/auth/reset-password", json={"email": "ghost@example.com"})
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_reset_password_invalid_email_returns_422() -> None:
    response = client.post("/auth/reset-password", json={"email": "not-an-email"})
    assert response.status_code == 422


# --- POST /auth/set-new-password ---
# Requirements:
#   - Valid token and strong password return 200 with success=True
#   - An invalid or expired token returns 400
#   - Password must satisfy the password policy (422)
#   - token and new_password are required fields (422)


def test_set_new_password_returns_ok() -> None:
    response = client.post("/auth/set-new-password", json={"token": "valid-token", "new_password": VALID_PASSWORD})
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_set_new_password_invalid_token_returns_400() -> None:
    response = client.post("/auth/set-new-password", json={"token": "invalid-token", "new_password": VALID_PASSWORD})
    assert response.status_code == 400


def test_set_new_password_weak_password_returns_422() -> None:
    response = client.post("/auth/set-new-password", json={"token": "valid-token", "new_password": "weak"})
    assert response.status_code == 422


def test_set_new_password_missing_token_returns_422() -> None:
    response = client.post("/auth/set-new-password", json={"new_password": VALID_PASSWORD})
    assert response.status_code == 422


def test_set_new_password_missing_new_password_returns_422() -> None:
    response = client.post("/auth/set-new-password", json={"token": "valid-token"})
    assert response.status_code == 422
