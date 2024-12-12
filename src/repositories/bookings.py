from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.database import engine
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

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

            return [self.schema.model_validate(booking, from_attributes=True) for booking in result.scalars().all()]





