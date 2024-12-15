from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.database import engine
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    # async def get_filtered(
    #         self,
    #         hotel_id: int,
    #         title:str,
    #         min_price:int,
    #         max_price:int
    # ) -> list[Room]:
    #
    #     query = (select(RoomsOrm).filter_by(hotel_id=hotel_id))
    #
    #     if title:
    #         query=query.filter(RoomsOrm.title.icontains(title))
    #     if min_price:
    #         query=query.filter(RoomsOrm.price > min_price)
    #     if max_price:
    #         query=query.filter(RoomsOrm.price < max_price)
    #
    #
    #     print(query.compile(engine, compile_kwargs={"literal_binds": True}))
    #
    #     result = await self.session.execute(query)
    #
    #     return [Room.model_validate(room) for room in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):

        # with rooms_count as (
        #         select room_id, count( *) as rooms_booked from bookings
        #           where date_from <= '2025-01-08' and date_to >= '2025-01-01'
        #           group by room_id
        # ),
        # rooms_left_table as (
        #     select rooms.id as room_id, quantity - coalesce (rooms_booked, 0) as rooms_left
        #       from rooms
        #     left join rooms_count on rooms.id = rooms_count.room_id
        # )
        # select *
        # from rooms_left_table
        # where
        # rooms_left > 0

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        # print(rooms_ids_to_get.compile(engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))