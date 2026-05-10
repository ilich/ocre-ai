from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.models.domain import Coin, User


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

    async def add_coin_to_collection(self, user: User, record_id: str) -> None:
        coin = await Coin.find_one(Coin.record_id == record_id)
        if not coin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coin not found")

        if record_id not in user.collection:
            user.collection.append(record_id)
            await self.update_user(user)

    async def remove_coin_from_collection(self, user: User, record_id: str) -> None:
        if record_id in user.collection:
            user.collection.remove(record_id)
            await self.update_user(user)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coin not in collection")


def get_user_repository() -> UserRepository:
    return UserRepository()
