from app.models import User
from app.repositories import BaseRepository
from app.schemas.user import UserModel


class UserRepository(BaseRepository):
    __slots__ = ("session",)
    
    model = User
    schema = UserModel
    order_by = User.username
    limit = 10

    async def create(self, user: UserModel) -> UserModel:
        new_user = await super().create(user.to_db())
        return self.dump(new_user)

    async def get_by_id(
        self, id: int, tasks: bool = False, projects: bool = False
    ) -> UserModel:
        stmt = self.get(id)
        if tasks:
            stmt = self.add_relation(stmt, User.tasks)
        if projects:
            stmt = self.add_relation(stmt, User.projects)
        result = await self.execute(stmt)
        user: User | None = result.one_or_none()
        return self.dump(user)

    async def get_by_username(self, username: str) -> UserModel | None:
        result = await self.execute(self.get_by_field(User.username, username))
        user: User | None = result.one_or_none()
        return self.dump(user)

    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.execute(self.get_by_field(User.email, email))
        user: User | None = result.one_or_none()
        return self.dump(user)

    async def get_all(
        self,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int = None,
        ascending: bool = True,
    ) -> list[UserModel]:
        result = await self.execute(
            super().get_all(order_by, limit, offset, ascending)
        )
        users: list[User] = await result.all()
        return self.dump(users)

    async def update(self, user: UserModel) -> UserModel:
        updated_user: User = await super().update(user)
        return self.dump(updated_user)

    async def delete(self, id: int) -> UserModel | None:
        user: User = await super().delete_by_id(id)
        return self.dump(user)
