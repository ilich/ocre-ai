from datetime import datetime, timezone

from app.models.domain import User


class UserRepository:
    async def get_user_by_email(self, email: str) -> User | None:
        return await User.find_one(User.email == email)

    async def get_user_by_id(self, user_id: str) -> User | None:
        return await User.get(user_id)

    async def get_user_by_reset_token(self, token: str) -> User | None:
        now = datetime.now(timezone.utc)
        return await User.find_one(
            {
                "reset_password_tokens": {
                    "$elemMatch": {
                        "token": token,
                        "expires_at": {"$gt": now},
                    }
                }
            }
        )

    async def create_user(self, email: str, password: str, full_name: str) -> User:
        new_user = User(
            email=email,
            password=password,
            full_name=full_name,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        await new_user.insert()
        return new_user

    async def update_user(self, user: User) -> None:
        user.updated_at = datetime.now(timezone.utc)
        await user.save()


def get_user_repository() -> UserRepository:
    return UserRepository()
