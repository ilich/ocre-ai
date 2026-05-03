from datetime import datetime, timezone

from app.models.domain import User


class UserRepository:
    async def get_user_by_email(self, email: str) -> User:
        return await User.find_one(User.email == email)

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


def get_user_repository():
    return UserRepository()
