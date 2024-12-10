from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.database import engine
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    async def get_filtered(
            self,
            hotel_id: int,
            title:str,
            min_price:int,
            max_price:int
    ) -> list[Room]:

        query = (select(RoomsOrm).filter_by(hotel_id=hotel_id))

        if title:
            query=query.filter(RoomsOrm.title.icontains(title))
        if min_price:
            query=query.filter(RoomsOrm.price > min_price)
        if max_price:
            query=query.filter(RoomsOrm.price < max_price)


        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)

        return [Room.model_validate(room) for room in result.scalars().all()]