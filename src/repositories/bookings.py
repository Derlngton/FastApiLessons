from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.database import engine
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking


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
