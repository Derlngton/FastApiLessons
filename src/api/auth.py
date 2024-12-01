from fastapi import APIRouter, Body
from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd


router_auth = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")



@router_auth.post("/register")
async def register(
        data: UserRequestAdd = Body(
    openapi_examples={
    "1":{"summary": "Пампкин", "value": {
        "email" : "pumkin@cat.ru",
        "password" : "love_with_fish"
    }},
    "2":{"summary": "Катенька", "value": {
        "email" : "katushka@xuxu.com",
        "password" : "1111"
    }}
    })
):

    hashed_password = pwd_context.hash(data.password)

    new_user_data= UserAdd(email=data.email, hashed_password = hashed_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(data=new_user_data)
        await session.commit()

    return {"status": "ok"}
