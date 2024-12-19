from pydantic import EmailStr
from sqlalchemy import select
from fastapi import HTTPException


from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import User, UserWithHashPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    # schema = User
    mapper = UserDataMapper


    async def get_user_with_hash_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if not model:
            return None

        return UserWithHashPassword.model_validate(model)

