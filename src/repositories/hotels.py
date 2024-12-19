from datetime import date

from sqlalchemy import select



from src.database import engine
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    # schema = Hotel
    mapper = HotelDataMapper

    # async def get_all(
    #         self,
    #         location:str,
    #         title:str,
    #         limit:int,
    #         offset:int
    # ) -> list[Hotel]:
    #
    #
    #     query = select(HotelsOrm)
    #
    #     if title:
    #         query=query.filter(HotelsOrm.title.icontains(title))
    #     if location:
    #         query=query.filter(HotelsOrm.location.icontains(location))
    #
    #     query=(
    #         query
    #         .limit(limit)
    #         .offset(offset)
    #     )
    #
    #     print(query.compile(engine, compile_kwargs={"literal_binds": True}))
    #
    #     result = await self.session.execute(query)
    #
    #     return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location: str,
            title: str,
            limit: int,
            offset: int
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )


        query = select(HotelsOrm)

        if title:
            query = query.filter(HotelsOrm.title.icontains(title))
        if location:
            query = query.filter(HotelsOrm.location.icontains(location))

        query = (
            query
            .filter(HotelsOrm.id.in_(hotels_ids))
            .limit(limit)
            .offset(offset)
        )

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)

        # return await self.get_filtered(HotelsOrm.id.in_(hotels_ids))
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
