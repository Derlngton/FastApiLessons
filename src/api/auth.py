from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router_auth = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])



@router_auth.post("/register")
async def register(
        db: DBDep,
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
    try:
        hashed_password = AuthService().hash_password(data.password)
        new_user_data= UserAdd(email=data.email, hashed_password = hashed_password)
        await db.users.add(data=new_user_data)
        await db.commit()
    except:
        raise HTTPException(status_code=400)

    return {"status": "ok"}




@router_auth.post("/login")
async def login_user(
        db: DBDep,
        response: Response,
        data: UserRequestAdd
        = Body(
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
    user = await db.users.get_user_with_hash_password(email=data.email)

    if not user:
        return HTTPException(status_code=401,detail="Пользователь с таким имейлом не зарегистрирован")
    if not AuthService().verify_password(data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Пароль неверный")

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}


@router_auth.get("/me")
async def get_me(
        db: DBDep,
        user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user