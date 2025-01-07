from typing import Optional
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserCreateInternal, User as UserSchema, UserUpdate
from app.services.base import BaseService


class UserService(BaseService[User, UserCreateInternal, UserUpdate, UserSchema]):
    repository: UserRepository

    def __init__(self, repository: UserRepository):
        super().__init__(repository, UserSchema)

    async def get_by_email(self, email: str) -> Optional[UserSchema]:
        model = await self.repository.get_by_email(email)
        if model:
            return self.return_schema.model_validate(model)
        return None

    async def create(self, obj_in: UserCreate) -> UserSchema:
        hashed_password = get_password_hash(obj_in.password)
        user_data = obj_in.model_dump()
        user_data["hashed_password"] = hashed_password
        del user_data["password"]

        model = await self.repository.create(UserCreateInternal(**user_data))
        return self.return_schema.model_validate(model)

    async def authenticate(self, email: str, password: str) -> Optional[UserSchema]:
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def is_active(self, user: UserSchema) -> bool:
        return user.is_active
