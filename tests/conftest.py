import json

import pytest

from httpx import AsyncClient, ASGITransport

from src.config import settings
from src.database import Base, engine_null_pull, async_session_maker_null_pull
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


# scope="session" - чтобы фикстура выполнялась один раз за всю сессию. Если параметр не указывать, фикстура будет выполняться каждую функцию. дефолтное значение = function
@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"



@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    # функция check_test_mode в аргументах означает, что async_main будет выполнена после check_test_mode
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pull) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def add_hotels_and_rooms(setup_database):

    with open("tests/mock_hotels.json") as file:
        hotels_data = json.load(file)

    with open("tests/mock_rooms.json") as file:
        rooms_data = json.load(file)

    pydantic_hotels_data = [HotelAdd(**hotel) for hotel in hotels_data]
    # pydantic_hotels_data = [HotelAdd.model_validate(hotel) for hotel in hotels_data]

    pydantic_rooms_data = [RoomAdd(**room) for room in rooms_data]
    # pydantic_rooms_data = [RoomAdd.model_validate(room) for room in rooms_data]
    async with DBManager(session_factory=async_session_maker_null_pull) as db_:

        await db_.hotels.add_bulk(data=pydantic_hotels_data)
        await db_.rooms.add_bulk(data=pydantic_rooms_data)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def register_user(add_hotels_and_rooms, ac):
    await ac.post(
        '/auth/register',
        json={
            "email":"koskin@sup.ru",
            "password": "124345"
        }
    )