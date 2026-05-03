from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import jwt
from argon2 import PasswordHasher
from beanie import PydanticObjectId
from fastapi.testclient import TestClient

from app.core.settings import Settings, get_settings
from app.main import app
from app.models.domain import ResetPasswordToken
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
        public_url="https://app.example.com",
        email_from="no-reply@example.com",
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_username="smtp-user",
        smtp_password="smtp-password",
        smtp_use_tls=True,
    )


def _user(
    email: str = "new@example.com",
    full_name: str = "Jane Doe",
    password: str = "hashed-password",
    reset_password_tokens: list[ResetPasswordToken] | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id=FAKE_USER_ID,
        email=email,
        full_name=full_name,
        password=password,
        reset_password_tokens=reset_password_tokens or [],
    )


def _mock_user_repository(
    existing_user: object | None = None,
    created_user: object | None = None,
    reset_token_user: object | None = None,
) -> MagicMock:
    repository = MagicMock(spec=UserRepository)
    repository.get_user_by_email = AsyncMock(return_value=existing_user)
    repository.get_user_by_reset_token = AsyncMock(return_value=reset_token_user)
    repository.create_user = AsyncMock(return_value=created_user or _user())
    repository.update_user = AsyncMock(return_value=None)
    return repository


def _override_user_repository(repository: object) -> None:
    app.dependency_overrides[get_user_repository] = lambda: repository
    app.dependency_overrides[get_settings] = _settings


def _hashed_password(password: str = VALID_PASSWORD) -> str:
    return PasswordHasher().hash(password)


# --- POST /auth/sign-in ---
# Requirements:
#   - Valid credentials return 200 with access_token and token_type "bearer"
#   - Wrong credentials return 401
#   - Email must be a valid email address (422)
#   - login and password are required fields (422)


def test_sign_in_returns_access_token() -> None:
    repository = _mock_user_repository(existing_user=_user(email="user@example.com", password=_hashed_password()))
    _override_user_repository(repository)
    try:
        response = client.post("/auth/sign-in", json={"login": "user@example.com", "password": VALID_PASSWORD})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    token_payload = jwt.decode(body["access_token"], TEST_SECRET_KEY, algorithms=["HS256"])
    assert token_payload["user_id"] == str(FAKE_USER_ID)
    repository.get_user_by_email.assert_awaited_once_with("user@example.com")


def test_sign_in_wrong_credentials_returns_401() -> None:
    repository = _mock_user_repository(existing_user=_user(email="user@example.com", password=_hashed_password()))
    _override_user_repository(repository)
    try:
        response = client.post("/auth/sign-in", json={"login": "user@example.com", "password": "wrongpass"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    repository.get_user_by_email.assert_awaited_once_with("user@example.com")


def test_sign_in_unknown_user_returns_401() -> None:
    repository = _mock_user_repository(existing_user=None)
    _override_user_repository(repository)
    try:
        response = client.post("/auth/sign-in", json={"login": "ghost@example.com", "password": VALID_PASSWORD})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    repository.get_user_by_email.assert_awaited_once_with("ghost@example.com")


def test_sign_in_normalizes_login_before_lookup() -> None:
    repository = _mock_user_repository(existing_user=_user(email="user@example.com", password=_hashed_password()))
    _override_user_repository(repository)
    try:
        response = client.post("/auth/sign-in", json={"login": "USER@example.com", "password": VALID_PASSWORD})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    repository.get_user_by_email.assert_awaited_once_with("user@example.com")


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


# --- POST /auth/forgot-password ---
# Requirements:
#   - A known email returns 200, stores a reset token, and sends an email
#   - An unknown email returns 404
#   - Invalid email format returns 422


def test_forgot_password_returns_ok_and_sends_email() -> None:
    user = _user(email="user@example.com")
    repository = _mock_user_repository(existing_user=user)
    _override_user_repository(repository)
    smtp_server = MagicMock()
    smtp = MagicMock()
    smtp.return_value.__enter__.return_value = smtp_server

    try:
        with patch("app.services.email.smtplib.SMTP", new=smtp):
            response = client.post("/auth/forgot-password", json={"email": "user@example.com"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Password reset email sent"}
    repository.get_user_by_email.assert_awaited_once_with("user@example.com")
    repository.update_user.assert_awaited_once_with(user)
    assert len(user.reset_password_tokens) == 1
    assert user.reset_password_tokens[0].token
    assert user.reset_password_tokens[0].expires_at > datetime.now(timezone.utc)
    smtp.assert_called_once_with("smtp.example.com", 587)
    smtp_server.starttls.assert_called_once()
    smtp_server.login.assert_called_once_with("smtp-user", "smtp-password")
    smtp_server.send_message.assert_called_once()
    message = smtp_server.send_message.call_args.args[0]
    assert message["To"] == "user@example.com"
    assert message["From"] == "no-reply@example.com"
    assert message["Subject"] == "Reset Your Password"


def test_forgot_password_unknown_email_returns_404_and_does_not_send_email() -> None:
    repository = _mock_user_repository(existing_user=None)
    _override_user_repository(repository)
    smtp = MagicMock()

    try:
        with patch("app.services.email.smtplib.SMTP", new=smtp):
            response = client.post("/auth/forgot-password", json={"email": "ghost@example.com"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    repository.get_user_by_email.assert_awaited_once_with("ghost@example.com")
    repository.update_user.assert_not_called()
    smtp.assert_not_called()


def test_forgot_password_invalid_email_returns_422() -> None:
    response = client.post("/auth/forgot-password", json={"email": "not-an-email"})
    assert response.status_code == 422


# --- POST /auth/reset-password ---
# Requirements:
#   - A valid token and strong password return 200 and update the password
#   - An invalid or expired token returns 404
#   - Password must satisfy the password policy (422)
#   - token and new_password are required fields (422)


def test_reset_password_returns_ok_and_updates_password() -> None:
    token = "valid-reset-token"
    old_token = ResetPasswordToken(token=token, expires_at=datetime.now(timezone.utc) + timedelta(minutes=10))
    user = _user(email="user@example.com", password=_hashed_password("OldP@ssw0rd"), reset_password_tokens=[old_token])
    repository = _mock_user_repository(reset_token_user=user)
    _override_user_repository(repository)

    try:
        response = client.post("/auth/reset-password", json={"token": token, "new_password": VALID_PASSWORD})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Password has been reset successfully"}
    repository.get_user_by_reset_token.assert_awaited_once_with(token)
    repository.update_user.assert_awaited_once_with(user)
    assert user.reset_password_tokens == []
    PasswordHasher().verify(user.password, VALID_PASSWORD)


def test_reset_password_invalid_token_returns_404() -> None:
    repository = _mock_user_repository(reset_token_user=None)
    _override_user_repository(repository)

    try:
        response = client.post("/auth/reset-password", json={"token": "invalid-token", "new_password": VALID_PASSWORD})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    repository.get_user_by_reset_token.assert_awaited_once_with("invalid-token")
    repository.update_user.assert_not_called()


def test_reset_password_invalid_email_returns_422() -> None:
    response = client.post("/auth/forgot-password", json={"email": "not-an-email"})
    assert response.status_code == 422


def test_reset_password_weak_password_returns_422() -> None:
    response = client.post("/auth/reset-password", json={"token": "valid-token", "new_password": "weak"})
    assert response.status_code == 422


def test_reset_password_missing_token_returns_422() -> None:
    response = client.post("/auth/reset-password", json={"new_password": VALID_PASSWORD})
    assert response.status_code == 422


def test_reset_password_missing_new_password_returns_422() -> None:
    response = client.post("/auth/reset-password", json={"token": "valid-token"})
    assert response.status_code == 422
