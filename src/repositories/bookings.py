from datetime import date

from sqlalchemy import select, insert
from fastapi import HTTPException

from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.database import engine
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import Booking, BookingAdd
from src.schemas.rooms import Room


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    # schema = Booking
    mapper = BookingDataMapper

    async def get_filtered(
                self,
                limit: int,
                offset: int,
                **filter_by
    ) -> list[Booking]:

            query = select(self.model).filter_by(**filter_by)

            query = (
                query
                .limit(limit)
                .offset(offset)
            )

            # print(query.compile(engine, compile_kwargs={"literal_binds": True}))

            result = await self.session.execute(query)

            return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]



    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]



    async def add_booking(self, data: BookingAdd, hotel_id: int):

        # проверка на наличие свободных комнат
        rooms_ids_to_get = rooms_ids_for_booking(date_from= data.date_from,date_to=data.date_to, hotel_id=hotel_id)

        result = await self.session.execute(rooms_ids_to_get)
        room_ids = result.scalars().all()

        if data.room_id in room_ids:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise HTTPException(status_code=404, detail="Не найдены свободные номера")