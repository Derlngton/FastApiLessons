from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.database import engine


class BaseRepository:
    model = None
    schema: BaseModel = None


    def __init__(self, session):
        # на случай, если будет использоваться несколько методов класса подряд, чтобы все были в рамках одной сессии
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by))
        result = await self.session.execute(query)

        # hotels = result.all()
        # возвращает список кортежей из одного элемента (в кортеже объект HotelsOrm)
        # hotels = result.scalars().all()
        # возвращает так же список, но из каждого кортежа берет по первому элементу
        # т.е получаем список объектов HotelsOrm

        return [self.schema.model_validate(model) for model in result.scalars().all()]
        # return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self,*args, **kwargs):
        return await self.get_filtered()


    async def get_one_or_none(self,**filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        model = result.scalars().one_or_none()

        if model is None:
            return None

        return self.schema.model_validate(model)
        # return result.scalars().one_or_none()
        # return self.schema.model_validate(model, from_attributes=True)



    async def add(self, data: BaseModel):
        # model_dump - преобразует модель в словарь
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)

        # для более коректного дебага (вместо echo=True):
        # print(stmt.compile(engine, compile_kwargs={"literal_binds": True}))

        # в уроке полученный словарь еще распаковывают ** в словарь
        # зачем? если мы уже получаем словарь
        # add_hotel_stat = insert(HotelsOrm).values(**hotel_data.model_dump())
        result = await self.session.execute(stmt)
        # return result.scalars().one()
        model = result.scalars().one()
        # return self.schema.model_validate(model, from_attributes=True)
        return self.schema.model_validate(model)

    async def add_bulk(self, data: list[BaseModel]):
        stmt = insert(self.model).values([item.model_dump() for item in data])
        # print(stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(stmt)



    async def update(self, data:BaseModel, is_patch: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(data.model_dump(exclude_unset=is_patch))
            .returning(self.model)
        )

        # вынести отдельно, сделать декоратор для дебага запросов
        print(update_stmt.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(update_stmt)

        # return result.scalars().one()
        model = result.scalars().one()

        # return self.schema.model_validate(model, from_attributes=True)
        return self.schema.model_validate(model)


    async def delete(self, **filter_by) -> None:

        # delete_stmt = delete(self.model).where(self.model.id == id)
        delete_stmt = delete(self.model).filter_by(**filter_by)
        print(delete_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_stmt)
