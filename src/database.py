from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


from src.config import settings

# для быстрого дебага хватит (settings.DB_URL, echo = True)
engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

# session = async_session_maker()
# await session.execute()