import pytest
from pydantic import BaseModel, ValidationError

from app.models.fields import Password, enforce_password_policy


class _Model(BaseModel):
    password: Password


def test_valid_password_passes() -> None:
    assert enforce_password_policy("SecureP@ss1") == "SecureP@ss1"


def test_password_too_short_raises() -> None:
    with pytest.raises(ValueError, match="at least 8 characters"):
        enforce_password_policy("Sh0rt!")


def test_password_missing_uppercase_raises() -> None:
    with pytest.raises(ValueError, match="uppercase"):
        enforce_password_policy("lowercase1!")


def test_password_missing_lowercase_raises() -> None:
    with pytest.raises(ValueError, match="lowercase"):
        enforce_password_policy("UPPERCASE1!")


def test_password_missing_digit_raises() -> None:
    with pytest.raises(ValueError, match="number"):
        enforce_password_policy("NoDigits!")


def test_password_missing_special_char_raises() -> None:
    with pytest.raises(ValueError, match="special character"):
        enforce_password_policy("NoSpecial1")


def test_password_type_rejects_weak_password() -> None:
    with pytest.raises(ValidationError):
        _Model(password="weak")


def test_password_type_accepts_strong_password() -> None:
    model = _Model(password="SecureP@ss1")
    assert model.password == "SecureP@ss1"
