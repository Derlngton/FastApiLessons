from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.database import engine


class BaseRepository:
    model = None


    def __init__(self, session):
        # на случай, если будет использоваться несколько методов класса подряд, чтобы все были в рамках одной сессии
        self.session = session


    async def get_all(self,*args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        # hotels = result.all()
        # возвращает список кортежей из одного элемента (в кортеже объект HotelsOrm)
        # hotels = result.scalars().all()
        # возвращает так же список, но из каждого кортежа берет по первому элементу
        # т.е получаем список объектов HotelsOrm

        return result.scalars().all()




    async def get_one_or_none(self,**filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()



    async def add(self, data: BaseModel):
        # model_dump - преобразует модель в словарь
        add_hotel_stmt = insert(self.model).values(data.model_dump()).returning(self.model)

        # для более коректного дебага (вместо echo=True):
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))

        # в уроке полученный словарь еще распаковывают ** в словарь
        # зачем? если мы уже получаем словарь
        # add_hotel_stat = insert(HotelsOrm).values(**hotel_data.model_dump())
        result = await self.session.execute(add_hotel_stmt)
        return result.scalars().one()


    async def full_update(self, id:int, data:BaseModel, **filter_by) -> None:

        full_update_stmt = update(self.model).where(self.model.id == id).values(data.model_dump()).returning(self.model)
        print(full_update_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(full_update_stmt)
        return result.scalars().one()


    async def delete(self,id:int, **filter_by) -> None:

        delete_stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        print(delete_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(delete_stmt)
        return result.scalars().one()
