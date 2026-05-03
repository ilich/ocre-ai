from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app, raise_server_exceptions=False)

VALID_PASSWORD = "SecureP@ss1"


# --- GET /user/me ---
# Requirements:
#   - An authenticated user receives 200 with their id, email, and full_name
#   - An unauthenticated request returns 401


def test_get_me_returns_user_details() -> None:
    response = client.get("/user/me", headers={"Authorization": "Bearer valid-token"})
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "email" in body
    assert "full_name" in body


def test_get_me_unauthenticated_returns_401() -> None:
    response = client.get("/user/me")
    assert response.status_code == 401


# --- POST /user/change-password ---
# Requirements:
#   - Correct old password and a strong new password return 200 with success=True
#   - A wrong old password returns 400
#   - New password must satisfy the password policy (422)
#   - An unauthenticated request returns 401
#   - old_password and new_password are required fields (422)


def test_change_password_returns_ok() -> None:
    response = client.post(
        "/user/change-password",
        json={"old_password": "OldP@ssw0rd", "new_password": VALID_PASSWORD},
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_change_password_wrong_old_password_returns_400() -> None:
    response = client.post(
        "/user/change-password",
        json={"old_password": "WrongP@ssw0rd", "new_password": VALID_PASSWORD},
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 400


def test_change_password_weak_new_password_returns_422() -> None:
    response = client.post(
        "/user/change-password",
        json={"old_password": "OldP@ssw0rd", "new_password": "weak"},
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 422


def test_change_password_unauthenticated_returns_401() -> None:
    response = client.post(
        "/user/change-password",
        json={"old_password": "OldP@ssw0rd", "new_password": VALID_PASSWORD},
    )
    assert response.status_code == 401


def test_change_password_missing_old_password_returns_422() -> None:
    response = client.post(
        "/user/change-password",
        json={"new_password": VALID_PASSWORD},
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 422


def test_change_password_missing_new_password_returns_422() -> None:
    response = client.post(
        "/user/change-password",
        json={"old_password": "OldP@ssw0rd"},
        headers={"Authorization": "Bearer valid-token"},
    )
    assert response.status_code == 422
