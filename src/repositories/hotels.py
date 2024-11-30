from sqlalchemy import select, insert



from src.database import engine
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel



class HotelsRepository(BaseRepository):
    model = HotelsOrm


    async def get_all(
            self,
            location:str,
            title:str,
            limit:int,
            offset:int
    ):


        query = select(HotelsOrm)

        if title:
            query=query.filter(HotelsOrm.title.icontains(title))
        if location:
            query=query.filter(HotelsOrm.location.icontains(location))

        query=(
            query
            .limit(limit)
            .offset(offset)
        )

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)

        return result.scalars().all()

    # async def add(self, hotel_data: Hotel):
    #
    #
    #     # model_dump - преобразует модель в словарь
    #     add_hotel_stmt = insert(HotelsOrm).values(hotel_data.model_dump())
    #
    #
    #     # для более коректного дебага какого-то конкретного запроса (вместо echo=True):
    #     print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds" : True}))
    #
    #     # в уроке полученный словарь еще распаковывают ** в словарь
    #     # зачем? если мы уже получаем словарь
    #     # add_hotel_stat = insert(HotelsOrm).values(**hotel_data.model_dump())
    #     await self.session.execute(add_hotel_stmt)
