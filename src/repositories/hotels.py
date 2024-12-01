from sqlalchemy import select



from src.database import engine
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel


    async def get_all(
            self,
            location:str,
            title:str,
            limit:int,
            offset:int
    ) -> list[Hotel]:


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

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]


