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

            print(query.compile(engine, compile_kwargs={"literal_binds": True}))

            result = await self.session.execute(query)

            return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]



    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]



    async def add_booking(self, data: BookingAdd, hotel_id: int, **filter_by):

        # проверка на наличие свободных комнат
        rooms_ids_to_get = rooms_ids_for_booking(date_from= data.date_from,date_to=data.date_to, hotel_id=hotel_id)

        query = (
            select(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)

        rooms = [Room.model_validate(model) for model in result.unique().scalars().all()]


        print(f"{rooms=}")

        if rooms==[]:
            raise HTTPException(status_code=404, detail="Не найдены свободные номера")


        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalars().one()

        return self.mapper.map_to_domain_entity(model)