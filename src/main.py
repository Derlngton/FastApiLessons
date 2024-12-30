from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Query, Body


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.backends.inmemory import InMemoryBackend


import sys
from pathlib import Path

from src.config import settings

sys.path.append(str(Path(__file__).parent.parent))

from src.setup import redis_manager

from src.api.hotels import router_hotels
from src.api.auth import router_auth
from src.api.rooms import router_rooms
from src.api.bookings import router_bookings
from src.api.facilities import router_facilities
from src.api.images import router_images

@asynccontextmanager
async def lifespan(app:FastAPI):
    # При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    # При выключении/перезагрузке проекта
    await redis_manager.close()

# # вместо написания заглушке для кэша(редис) можно использовать класс InMemoryBackend
# # но это не подходит для всех других сервисов. Во всех других случаях нужны моки
# if settings.MODE == "TEST":
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


app = FastAPI(lifespan=lifespan)
# app = FastAPI()


app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)