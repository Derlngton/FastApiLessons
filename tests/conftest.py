import pytest

from src.config import settings
from src.database import Base, engine_null_pull
from src.models import *

# scope="session" - чтобы фикстура выполнялась один раз за всю сессию. Если параметр не указывать, фикстура будет выполняться каждую функцию. дефолтное значение = function
@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"



@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test_mode):
    # функция check_test_mode в аргументах означает, что async_main будет выполнена после check_test_mode
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)